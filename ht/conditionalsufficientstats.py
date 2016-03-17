from abc import ABCMeta, abstractmethod

class ConditionalSufficientStats(metaclass=ABCMeta):
	"""docstring for ConditionalSufficientStats"""
	def __init__(self):
		# Tuples (class value, attribute estimator)
		self._class_lookup = {}

	@abstractmethod
	def update(self, att_val, class_val, weight):
		pass
	
	@abstractmethod
	def probability_of_att_val_conditioned_on_class(self, att_val, class_val):
		pass

	@abstractmethod
	def best_split(self, split_metric, pre_split_dist, att_name):
		pass