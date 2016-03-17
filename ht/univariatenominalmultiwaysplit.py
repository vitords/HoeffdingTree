from ht.split import Split
from core.attribute import Attribute
from core.instance import Instance

class UnivariateNominalMultiwaySplit(Split):
	"""docstring for UnivariateNominalMultiwaySplit"""
	def __init__(self, att_name):
		self._split_att_names = []
		self._split_att_names.append(att_name)

	def branch_for_instance(self, instance):
		att = instance.dataset().attribute(self._split_att_names[0])
		# Implement instance.is_missing()
		if att is None or instance.is_missing(att):
			return None
		return att.value(instance.value(att))

	def condition_for_branch(self, branch):
		return '{0} = {1}'.format(self._split_att_names[0], branch)
		