from ht.leafnode import LeafNode
from ht.hnode import HNode
from ht.gaussianconditionalsufficientstats import GaussianConditionalSufficientStats
from ht.nominalconditionalsufficientstats import NominalConditionalSufficientStats
from ht.splitcandidate import SplitCandidate

class ActiveHNode(LeafNode):
    """A Hoeffding Tree node that supports growth."""
    def __init__(self):
        super().__init__()
        # The total weight of the instances seen at the last split evaluation. 
        self.weight_seen_at_last_split_eval = 0
        # Statistics for the attributes.
        # Dict of tuples (attribute name, ConditionalSufficientStats).
        self._node_stats = {}

    def update_node(self, instance):
        """Update the node with the supplied instance.

        Args:
            instance (Instance): The instance to be used for updating the node.
        """
        self.update_distribution(instance)
        for i in range(instance.num_attributes()):
            a = instance.attribute(i)
            if i is not instance.class_index():
                stats = self._node_stats.get(a.name(), None)
                if stats is None:
                    if a.is_numeric():
                        stats = GaussianConditionalSufficientStats()
                    else:
                        stats = NominalConditionalSufficientStats()
                    self._node_stats[a.name()] = stats

                stats.update(instance.value(attribute=a), 
                    instance.class_attribute().value(index=instance.class_value()),
                    instance.weight())

    def get_possible_splits(self, split_metric):
        """Return a list of the possible split candidates.

        Args:
            split_metric (SplitMetric): The splitting metric to be used.

        Returns:
            list[SplitCandidate]: A list of the possible split candidates.
        """
        splits = []
        null_dist = []
        null_dist.append(self.class_distribution)
        null_split = SplitCandidate(None, null_dist,
            split_metric.evaluate_split(self.class_distribution, null_dist))
        splits.append(null_split)

        for attribute_name, stat in self._node_stats.items():
            split_candidate = stat.best_split(split_metric, self.class_distribution, attribute_name)
            if split_candidate is not None:
                splits.append(split_candidate)

        return splits