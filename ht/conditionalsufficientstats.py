from abc import ABCMeta, abstractmethod

class ConditionalSufficientStats(metaclass=ABCMeta):
    """A class for keeping record of the sufficient statistics for an attribute."""
    def __init__(self):
        # Lookup by class value
        # Dict of tuples (class value, attribute estimator)
        self._class_lookup = {}

    @abstractmethod
    def update(self, att_val, class_val, weight):
        """Update the statistics with the supplied attribute and class values.

        Args:
            att_val (float): The value of the attribute.
            class_val (str): The value of the class.
            weight (float): The weight of this observation.
        """
        pass
    
    @abstractmethod
    def probability_of_att_val_conditioned_on_class(self, att_val, class_val):
        """Return the probability of an attribute value conditioned on a class value.

        Args:
            att_val (float): The attribute value to compute the conditional probability for.
            class_val (str): The class value.

        Returns:
            float: The probability of the attribute value being conditioned on the given class value.
        """
        pass

    @abstractmethod
    def best_split(self, split_metric, pre_split_dist, att_name):
        """Return the best split.

        Args:
            split_metric (SplitMetric): The split metric to use.
            pre_split_dist (dict): The distribution of class values before the split.
            att_name (str): The name of the attribute being considered for splitting.

        Returns:
            SplitCandidate: The best split for the attribute.
        """
        pass