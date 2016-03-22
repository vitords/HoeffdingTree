from ht.conditionalsufficientstats import ConditionalSufficientStats
from univariatenormalestimator import UnivariateNormalEstimator
from sortedcontainers import SortedList
from core import utils
import math

class GaussianEstimator(UnivariateNormalEstimator):
	"""docstring for GaussianEstimator"""
	def __init__(self):
		super().__init__()

	def get_sum_of_weights(self):
		return self._sum_of_weights

	def probability_density(self, value):
		self.update_mean_and_variance()
		if self._sum_of_weights > 0:
			std_dev = math.sqrt(self._variance)
			if std_dev > 0:
				diff = value - self._mean
				return (1.0 / (self.CONST * std_dev)) * math.exp(-(diff * diff / (2.0 * self._variance)))
			if value is self._mean:
				return 1.0
			else:
				return 0.0
		return 0.0

	def weight_less_than_equal_and_greater_than(self, value):
		std_dev = math.sqrt(self._variance)
		equal_w = self.probability_density(value) * self._sum_of_weights
		less_w = None
		if std_dev > 0:
			less_w = utils.normal_probability(
				(value - self._mean) / std_dev) * self._sum_of_weights - equal_w
		elif value < self._mean:
			less_w = self._sum_of_weights - equal_w
		else:
			less_w = 0.0
		greater_w = self._sum_of_weights - equal_w - less_w
		return [less_w, equal_w, greater_w]

class GaussianConditionalSufficientStats(ConditionalSufficientStats):
	"""docstring for GaussianConditionalSufficientStats"""
	def __init__(self):
		super().__init__()
		self._min_val_observed_per_class = {}
		self._max_val_observed_per_class = {}
		self._num_bins = 10

	def set_num_bins(self, b):
		self._num_bins = b

	def get_num_bins(self):
		return self._num_bins

	def update(self, att_val, class_val, weight):
		if not utils.is_missing_value(att_val):
			norm = self._class_lookup.get(class_val, None)
			if norm is None:
				return 0
			return norm.probability_density(att_val)

	def probability_of_att_val_conditioned_on_class(self, att_val, class_val):
		norm = self._class_lookup.get(class_val, None)
		if norm is None:
			return 0
		return norm.probability_density(att_val)

	def _get_split_point_candidates(self):
		splits = SortedList()
		min_value = math.inf
		max_value = -math.inf

		for class_value, att_estimator in self._class_lookup.items():
			min_val_observed_for_class_val = self._min_val_observed_per_class.get(class_val, None)
			if  min_val_observed_for_class_val is not None:
				if min_val_observed_for_class_val < min_value:
					min_value = min_val_observed_for_class_val
				max_val_observed_for_class_val = self._max_val_observed_per_class.get(class_val, None)
				if max_val_observed_for_class_val > max_value:
					max_value = max_val_observed_for_class_val

		if min_value < math.inf:
			new_bin = max_value - min_value
			new_bin /= (self._num_bins + 1)
			for i in range(self._num_bins):
				split = min_value + (new_bin * i + 1)
				if split > min_value and split < max_value:
					splits.add(split)
		return splits

	def _class_dists_after_split(self, split_val):
		lhs_dist = {}
		rhs_dist = {}

		for class_val, att_estimator in self._class_lookup.items():
			if att_estimator is not None:
				if split_val < self._min_val_observed_per_class[class_val]:
					mass = rhs_dist.get(class_val, None)
					if mass is None:
						mass = WeightMass()
						rhs_dist[class_val] = mass
				mass.weight += att_estimator.get_sum_of_weights()
			elif split_val > self._max_val_observed_per_class[class_val]:
				mass = lhs_dist.get(class_val, None)
				if mass is None:
					mass = WeightMass()
					lhs_dist[class_val] = mass
				mass.weight += att_estimator.get_sum_of_weights()
			else:
				weights = att_estimator.weight_less_than_equal_and_greater_than(split_val)
				mass = lhs_dist.get(class_val, None)
				if mass is None:
					mass = WeightMass()
					lhs_dist[class_val] = mass
				mass.weight += weights[0] + weights[1]
				mass = rhs_dist.get(class_val, None)
				if mass is None:
					mass = WeightMass()
					rhs_dist[class_val] = mass
				mass.weight += weights[2]

		dists = []
		dists.append(lhs_dist, rhs_dist)

		return dists

	def best_split(self, split_metric, pre_split_dist, att_name):
		best = None
		candidates = self._get_split_point_candidates()
		for candidate in candidates:
			post_split_dists = self.class_dists_after_split(candidate)

			split_merit = split_metric.evaluate_split(pre_split_dist, post_split_dists)

			if best is None or split_merit > best.split_merit:
				split = UnivariateNumericBinarySplit(att_name, candidate)
				best = SplitCandidate(split, post_split_dists, split_merit)

		return best