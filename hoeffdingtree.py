import math
from operator import attrgetter

from core import utils
from core.attribute import Attribute
from core.instance import Instance
from core.dataset import Dataset

from ht.activehnode import ActiveHNode
from ht.ginisplitmetric import GiniSplitMetric
from ht.hnode import HNode
from ht.inactivehnode import InactiveHNode
from ht.infogainsplitmetric import InfoGainSplitMetric
from ht.leafnode import LeafNode
from ht.splitcandidate import SplitCandidate
from ht.splitmetric import SplitMetric
from ht.splitnode import SplitNode

class HoeffdingTree(object):
	"""docstring for HoeffdingTree"""
	def __init__(self):
		self.__header = None
		self.__root = None
		self.__grace_period = 200
		self.__split_confidence = 0.0000001
		self.__hoeffding_tie_threshold = 0.05
		self.__min_frac_weight_for_two_branches_gain = 0.01

		# Split metric stuff goes here
		self.GINI_SPLIT = 0
		self.INFO_GAIN_SPLIT = 1

		self.__selected_split_metric = self.INFO_GAIN_SPLIT
		self.__split_metric = InfoGainSplitMetric(self.__min_frac_weight_for_two_branches_gain)
		#self.__selected_split_metric = self.GINI_SPLIT
		#self.__split_metric = GiniSplitMetric()

		# Leaf prediction strategy stuff goes here

		# Only related to naive bayes, probably not useful right now
		self.__nb_threshold = 0

		self.__active_leaf_count = 0
		self.__inactive_leaf_count = 0
		self.__decision_node_count = 0

		# Print out leaf models in the case of naive Bayes or naive Bayes adaptive leaves 
		self.__print_leaf_models = False

	def __str__(self):
		if self.__root is None:
			return 'No model built yet!'
		return self.__root.__str__(self.__print_leaf_models)

	def reset(self):
		self.__root = None
		self.__active_leaf_count = 0
		self.__inactive_leaf_count = 0
		self.__decision_node_count = 0

	def set_minimum_fraction_of_weight_info_gain(self, m):
		self.__min_frac_weight_for_two_branches_gain = m

	def get_minimum_fraction_of_weight_info_gain(self):
		return self.__min_frac_weight_for_two_branches_gain

	def set_grace_period(self, grace):
		self.__grace_period = grace

	def get_grace_period(self):
		return self.__grace_period

	def set_hoeffding_tie_threshold(self, ht):
		self.__hoeffding_tie_threshold = ht

	def get_hoeffding_tie_threshold(self):
		return self.__hoeffding_tie_threshold

	def set_split_confidence(self, sc):
		self.__split_confidence = sc

	def get_split_confidence(self):
		return self.__split_confidence

	def compute_hoeffding_bound(self, max_value, confidence, weight):
		return math.sqrt(((max_value * max_value) * math.log(1.0 / confidence)) / (2.0 * weight))

	def build_classifier(self, dataset):
		"""Build the classifier.

		Args:
			dataset (Dataset): The data to start training the classifier.
		"""
		self.reset()
		self.__header = dataset
		if self.__selected_split_metric is self.GINI_SPLIT:
			self.__split_metric = GiniSplitMetric()
		else:
			self.__split_metric = InfoGainSplitMetric(self.__min_frac_weight_for_two_branches_gain)

		for i in range(dataset.num_instances()):
			self.update_classifier(dataset.instance(i))

	def update_classifier(self, instance):
		"""Update the classifier with the given instance.

		Args:
			instance (Instance): The new instance to be used to train the classifier.
		"""
		if instance.class_is_missing():
			return

		if self.__root is None:
			self.__root = self.new_learning_node()

		l = self.__root.leaf_for_instance(instance, None, None)
		actual_node = l.the_node
		if actual_node is None:
			actual_node = ActiveHNode()
			l.parent_node.set_child(l.parent_branch, actual_node)

		
		# ActiveHNode should be changed to a LearningNode interface if Naive Bayes nodes are used
		if isinstance(actual_node, InactiveHNode):
			actual_node.update_node(instance)
		if isinstance(actual_node, ActiveHNode):
			actual_node.update_node(instance)
			total_weight = actual_node.total_weight()
			if total_weight - actual_node.weight_seen_at_last_split_eval > self.__grace_period:
				self.try_split(actual_node, l.parent_node, l.parent_branch)
				actual_node.weight_seen_at_last_split_eval = total_weight

	def distribution_for_instance(self, instance):
		"""Return the class probabilities for an instance.

		Args:
			instance (Instance): The instance to calculate the class probabilites for.

		Returns:
			list[float]: The class probabilities.
		"""
		class_attribute = instance.class_attribute()
		pred = [0 for i in range(class_attribute.num_values())]

		if self.__root is not None:
			l = self.__root.leaf_for_instance(instance, None, None)
			actual_node = l.the_node

			if actual_node is None:
				actual_node = l.parent_node

			pred = actual_node.get_distribution(instance, class_attribute)

		else:
			# All class values equally likely
			for i in range(class_attribute.num_values()):
				pred[i] = 1
			utils.normalize(pred)

		return pred


	def deactivate_node(self, to_deactivate, parent, parent_branch):
		"""Prevent supplied node of growing.

		Args:
			to_deactivate (ActiveHNode): The node to be deactivated.
			parent (SplitNode): The parent of the node.
			parent_branch (str): The branch leading from the parent to the node.
		"""
		leaf = InactiveHNode(to_deactivate.class_distribution)

		if parent is None:
			self.__root = leaf
		else:
			parent.set_child(parent_branch, leaf)

		self.__active_leaf_count -= 1
		self.__inactive_leaf_count += 1

	def activate_node(self, to_activate, parent, parent_branch):
		"""Allow supplied node to grow.

		Args:
			to_activate (InactiveHNode): The node to be activated.
			parent (SplitNode): The parent of the node.
			parent_branch (str): The branch leading from the parent to the node.
		"""
		leaf = ActiveHNode()
		leaf.class_distribution = to_activate.class_distribution

		if parent is None:
			self.__root = leaf
		else:
			parent.set_child(parent_branch, leaf)

		self.__active_leaf_count += 1
		self.__inactive_leaf_count -= 1

	def try_split(self, node, parent, parent_branch):
		"""Try a split from the supplied node.

		Args:
			node (ActiveHNode): The node to split.
			parent (SplitNode): The parent of the node.
			parent_branch (str): The branch leading from the parent to the node.
		"""
		# Non-pure?
		if node.num_entries_in_class_distribution() > 1:
			best_splits = node.get_possible_splits(self.__split_metric)
			best_splits.sort(key=attrgetter('split_merit'))

			do_split = False
			if len(best_splits) < 2:
				do_split = len(best_splits) > 0
			else:
				# Compute Hoeffding bound
				metric_max = self.__split_metric.get_metric_range(node.class_distribution)
				hoeffding_bound = self.compute_hoeffding_bound(
					metric_max, self.__split_confidence, node.total_weight())
				best = best_splits[len(best_splits) - 1]
				second_best = best_splits[len(best_splits) - 2]
				if best.split_merit - second_best.split_merit > hoeffding_bound or hoeffding_bound < self.__hoeffding_tie_threshold:
					do_split = True

			if do_split:
				best = best_splits[len(best_splits) - 1]
				if best.split_test is None:
					# preprune
					self.deactivate_node(node, parent, parent_branch)
				else:
					new_split = SplitNode(node.class_distribution, best.split_test)

					for i in range(best.num_splits()):
						new_child = self.new_learning_node()
						new_child.class_distribution = best.post_split_class_distributions[i]
						new_child.weight_seen_at_last_split_eval = new_child.total_weight()
						branch_name = ''
						if self.__header.attribute(name=best.split_test.split_attributes()[0]).is_numeric():
							if i is 0:
								branch_name = 'left'
							else:
								branch_name = 'right'
						else:
							split_attribute = self.__header.attribute(name=best.split_test.split_attributes()[0])
							branch_name = split_attribute.value(i)
						new_split.set_child(branch_name, new_child)

					self.__active_leaf_count -= 1
					self.__decision_node_count += 1
					self.__active_leaf_count += best.num_splits()

					if parent is None:
						self.__root = new_split
					else:
						parent.set_child(parent_branch, new_split)

	def new_learning_node(self):
		# Leaf strategy should be handled here if/when the Naive Bayes approach is implemented
		new_child = ActiveHNode()
		return new_child