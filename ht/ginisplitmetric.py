from ht.splitmetric import SplitMetric

class GiniSplitMetric(SplitMetric):
    """The Gini split metric."""
    def evaluate_split(self, pre_dist, post_dist):
        total_weight = 0.0
        dist_weights = []
        for i in range(len(post_dist)):
            dist_weights.append(self.sum(post_dist[i]))
            total_weight += dist_weights[i]
        gini_metric = 0
        for i in range(len(post_dist)):
            gini_metric += (dist_weights[i] / total_weight) * self.gini(
                post_dist[i], dist_weights[i])

        return 1.0 - gini_metric

    def gini(self, dist, sum_of_weights=None):
        if sum_of_weights is None:
            sum_of_weights = self.sum(dist)
        gini_metric = 1.0
        for class_value, mass in dist.items():
            frac = mass.weight / sum_of_weights
            gini_metric -= frac * frac
        return gini_metric

    def get_metric_range(self, pre_dist):
        return 1.0