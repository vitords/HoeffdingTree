from ht.split import Split
from core.instance import Instance

class UnivariateNumericBinarySplit(Split):
	"""docstring for UnivariateNumericBinarySplit"""
	def __init__(self, att_name, split_point):
		self._split_att_names.append(att_name)
		self._split_point = split_point

	def branch_for_instance(self, instance):
		att = instance.dataset().attribute(self._split_att_names[0])
		if att is None or instance.is_missing(att):
			# TODO
			return None
		if instance.value(att) <= self._split_point:
			return 'left'
		return 'right'

	def condition_for_branch(self, branch):
		result = self._split_att_names[0]
		if branch is 'left':
			result += ' <= '
		else:
			result += ' > '
		result += '{0}'.format(self._split_point)
		return result