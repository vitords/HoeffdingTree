from ht.leafnode import LeafNode

class InactiveHNode(LeafNode):
	"""docstring for InactiveHNode"""
	def __init__(self, class_distribution):
		super().__init__(class_distribution)
		#self.class_distribution = class_distribution

	def update_node(self, instance):
		self.update_distribution(instance)
