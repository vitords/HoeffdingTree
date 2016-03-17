from ht.splitmetric import SplitMetric
#from core.contingencytables import ContingencyTables
import math
from core import utils

class InfoGainSplitMetric(SplitMetric):
	"""docstring for InfoGainSplitMetric"""
	def __init__(self, min_frac_weight_for_two_branches):
		self._min_frac_weight_for_two_branches = min_frac_weight_for_two_branches
	
	def evaluate_split(self, pre_dist, post_dist):
		pre = []
		for class_value, mass in pre_dist.items():
			pre.append(pre_dist[class_value].weight)

		pre_entropy = utils.entropy(pre)

		dist_weights = []
		total_weight = 0.0

		for i in range(len(post_dist)):
			dist_weights.append(self.sum(post_dist[i]))
			total_weight += dist_weights[i]

		frac_count = 0
		for d in dist_weights:
			if d / total_weight > self._min_frac_weight_for_two_branches:
				frac_count += 1

		if frac_count < 2:
			return -math.inf

		post_entropy = 0
		for i in range(len(post_dist)):
			d = post_dist[i]
			post = []
			for class_value, mass in d.items():
				post.append(d[class_value].weight)
			post_entropy += dist_weights[i] * utils.entropy(post)

		if total_weight > 0:
			post_entropy /= total_weight

		return pre_entropy - post_entropy

	def get_metric_range(self, pre_dist):
		num_classes = len(pre_dist)
		if num_classes < 2:
			num_classes = 2

		return utils.log2(num_classes)