from ht.leafnode import LeafNode
from ht.hnode import HNode
from ht.gaussianconditionalsufficientstats import GaussianConditionalSufficientStats
from ht.nominalconditionalsufficientstats import NominalConditionalSufficientStats
from ht.splitcandidate import SplitCandidate

class ActiveHNode(LeafNode):
	"""docstring for ActiveHNode"""
	def __init__(self):
		HNode.__init__(self)
		self.weight_seen_at_last_split_eval = 0
		# Dict of tuples (attribute name, ConditionalSufficientStats)
		self._node_stats = {}

	def update_node(self, instance):
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
					instance.class_attribute().value(instance.class_value()), instance.weight())

	def get_possible_splits(self, split_metric):
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