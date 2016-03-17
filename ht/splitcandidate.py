from core import utils

class SplitCandidate(object):
	"""docstring for SplitCandidate"""
	def __init__(self, split_test, post_split_dists, merit):
		self.split_test = split_test
		self.post_split_class_distributions = post_split_dists
		self.split_merit = merit

	def num_splits(self):
		return len(self.post_split_class_distributions)

	def compare_to(sel, comp):
		return utils.compare(self.split_merit, comp.split_merit)