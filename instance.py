from attribute import *

class Instance(object):
	def __init__(self, att_values=None, number_att=None):
		if att_values is not None:
			self.__att_values = att_values
		else:
			self.__att_values = [None for i in range(number_att)]
		self.__dataset = None

	def attribute(self, index):
		return self.__dataset.attribute(index)

	def value(self, index=None, attribute=None):
		if index is not None:
			return self.__att_values[index]
		else:
			return self.value(index=attribute.index())

	def class_attribute(self):
		return self.__dataset.class_attribute()

	def class_index(self):
		return self.__dataset.class_index()

	def class_value(self):
		return self.value(index=self.class_index())

	def dataset(self):
		return self.__dataset

	def num_attributes(self):
		return len(self.__att_values)

	def num_classes(self):
		return self.__dataset.num_classes()

	def num_values(self):
		""" Always the same as num_attributes() """
		return len(self.__att_values)

	def set_value(self, att_index, value):
		if isinstance(value, str):
			self.attribute(att_index).add_value(value)
			value_index = self.attribute(att_index).index_of_value(value)
			self.set_value(att_index, value_index)
		else:	
			self.__att_values[att_index] = value

	def set_class_value(self, value):
		self.set_value(self.class_index(), value)

	def set_dataset(self, dataset):
		self.__dataset = dataset

	def get_attributes(self):
		attributes = [None for i in range(self.num_attributes())]
		for i in range(self.num_attributes()):
			attributes[i] = self.attribute(i)
		return attributes

	def __str__(self):
		return 'Instance\n   From dataset: {0}\n   Attribute values: {1}\n   Class: {2}'.format(
			self.__dataset.name() if self.__dataset is not None else 'This instance is not associated with a dataset.',
			 self.__att_values, 'A dataset is required to set an attribute as class.' if self.__dataset is None else self.__att_values[self.__dataset.class_index()])