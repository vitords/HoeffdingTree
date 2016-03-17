from ht.hnode import HNode

class LeafNode(HNode):
	"""
	"""
	def __init__(self, node=None, parent_node=None, parent_branch=None):
		self.the_node = node
		self.parent_node = parent_node
		self.parent_branch = parent_branch

	def update_node(self, instance):
		if self.the_node is not None:
			self.the_node.update_distribution(instance)
		else:
			super.update_distribution(instance)

	#def update_distribution(self, instance):
	#	super.update_distribution(instance)