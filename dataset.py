from instance import *

class Dataset(object):
	def __init__(self, attributes, class_index, instances=None, name='New dataset'):
		self.__attributes = attributes
		self.__class_index = class_index
		self.__instances = instances
		if self.__instances is not None:
			for inst in self.__instances:
				inst.set_dataset(self)
		else:
			self.__instances = []
		self.__name = name

	def add(self, instance):
		instance.set_dataset(self)
		self.__instances.append(instance)

	def attribute(self, index=None, name=None):
		if index is not None:
			return self.__attributes[index]
		else:
			for att in self.__attributes:
				if name == att.name():
					return att
			return None

	def class_attribute(self):
		return self.attribute(self.__class_index)

	def class_index(self):
		return self.__class_index

	def instance(self, index):
		return self.__instances[index]

	def num_attributes(self):
		return len(self.__attributes)

	def num_classes(self):
		if self.class_attribute().type() is not 'Nominal':
			return 1
		else:
			return self.class_attribute().num_values()

	def num_instances(self):
		return len(self.__instances)

	def name(self):
		return self.__name

	def get_attributes(self):
		return self.__attributes

	def __str__(self):
		return 'Dataset \'{0}\'\n   Attributes: {1}\n   Class attribute: {2}\n   Total instances: {3}'.format(
			self.__name, [att.name() for att in self.__attributes], 
			self.attribute(self.__class_index).name(), len(self.__instances))