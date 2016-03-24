from ht.conditionalsufficientstats import ConditionalSufficientStats
from ht.weightmass import WeightMass
from ht.splitcandidate import SplitCandidate
from ht.univariatenominalmultiwaysplit import UnivariateNominalMultiwaySplit
from core import utils

class ValueDistribution(object):
    """Discrete distribution for the NominalConditionalSufficientStats class."""
    def __init__(self):
        self._dist = {}
        self.__sum = 0

    def add(self, val, weight):
        count = self._dist.get(val, None)
        if count is None:
            count = WeightMass()
            count.weight = 1.0
            self.__sum += 1.0
            self._dist[val] = count
        count.weight += weight
        self.__sum += weight

    def delete(self, val, weight):
        count = self._dist.get(val, None)
        if count is not None:
            count.weight -= weight
            self.__sum -= weight

    def get_weight(self, val):
        count = self._dist.get(val, None)
        if count is not None:
            return count.weight
        return 0.0

    def sum(self):
        return self.__sum
        
class NominalConditionalSufficientStats(ConditionalSufficientStats):
    """A class for keeping record of the sufficient statistics for a nominal attribute."""
    def __init__(self):
        super().__init__()
        self._total_weight = 0
        self._missing_weight = 0

    def update(self, att_val, class_val, weight):
        if utils.is_missing_value(att_val):
            self._missing_weight += weight
        else:
            val_dist = self._class_lookup.get(class_val, None)
            if val_dist is None:
                val_dist = ValueDistribution()
                val_dist.add(att_val, weight)
                self._class_lookup[class_val] = val_dist
            else:
                val_dist.add(att_val, weight)
        self._total_weight += weight

    def probability_of_att_val_conditioned_on_class(self, att_val, class_val):
        val_dist = self._class_lookup.get(class_val, None)
        if val_dist is not None:
            return val_dist.get_weight(att_val) / val_dist.sum()
        return 0

    def _class_dists_after_split(self):
        split_dists = {}
        for class_val, att_dist in self._class_lookup.items():
            for att_val, att_count in att_dist._dist.items():
                cls_dist = split_dists.get(att_val, None)
                if cls_dist is None:
                    cls_dist = {}
                    split_dists[att_val] = cls_dist

                cls_count = cls_dist.get(class_val, None)
                if cls_count is None:
                    cls_count = WeightMass()
                    cls_dist[class_val] = cls_count
                cls_count.weight += att_count.weight

        result = []
        for att_index, dist in split_dists.items():
            result.append(dist)
        return result
        
    def best_split(self, split_metric, pre_split_dist, att_name):
        post_split_dists = self._class_dists_after_split()
        merit = split_metric.evaluate_split(pre_split_dist, post_split_dists)
        candidate = SplitCandidate(
            UnivariateNominalMultiwaySplit(att_name), post_split_dists, merit)
        return candidate