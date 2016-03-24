from abc import ABCMeta, abstractmethod

class SplitMetric(metaclass=ABCMeta):
    """Base for Info Gain and Gini split metrics."""
    def sum(self, dist):
        weight_sum = 0
        for class_value, mass in dist.items():
            weight_sum += dist[class_value].weight
        return weight_sum

    @abstractmethod
    def evaluate_split(self, pre_dist, post_dist):
        pass

    @abstractmethod
    def get_metric_range(self, pre_dist):
        pass