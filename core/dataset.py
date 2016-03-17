from core.instance import Instance

class Dataset(object):
	"""A class for handling a dataset (set of instances).

	Note:
		This class is based on the Weka implementation (weka.core.Instances) to make porting existing 
		Java algorithms an easier task.

	Args:
		attributes (list[Attributes]): The attributes of the dataset's instances.
		class_index (int): The index of the dataset's class attribute. (default -1)
		instances (list[Instance]): A list of instances of the dataset. 
			If not specified an empty dataset is created. (default None)
		name (str): The name of the dataset. (default 'New dataset')
	"""

	def __init__(self, attributes, class_index=-1, instances=None, name='New dataset'):
		# The attributes of the dataset's instances.
		self.__attributes = attributes
		# Set the indexes of the attributes in the dataset.
		for i in range(len(self.__attributes)):
			self.__attributes[i].set_index(i)
		# The index of the class attribute.
		self.__class_index = class_index
		# The set of instances of the dataset.
		self.__instances = instances
		# Associate all instances with the dataset.
		if self.__instances is not None:
			for inst in self.__instances:
				inst.set_dataset(self)
		else:
			# If no instances were given, set it to an empty list.
			self.__instances = []
		# The name of the dataset.
		self.__name = name

	def __str__(self):
		return 'Dataset \'{0}\'\n   Attributes: {1}\n   Class attribute: {2}\n   Total instances: {3}'.format(
			self.__name, [att.name() for att in self.__attributes], 
			self.attribute(self.__class_index).name(), len(self.__instances))

	def add(self, instance):
		"""Add an instance to the dataset. Instances are always added to the end of the list.

		Args:
			instance (Instance): The instance to be added.
		"""
		instance.set_dataset(self)
		self.__instances.append(instance)

	def attribute(self, index=None, name=None):
		"""Return the attribute at the given index or with the given name.

		Args:
			index (int): The index of the attribute to be returned.
			name (str): The name of the attribute to be returned.

		Returns:
			Attribute: The requested attribute.
			None: If the specified attribute name does not exist.
		"""
		if index is not None:
			return self.__attributes[index]
		else:
			for att in self.__attributes:
				if name == att.name():
					return att
			return None

	def class_attribute(self):
		"""Return the class attribute.

		Returns:
			Attribute: The class attribute.
		"""
		return self.attribute(self.__class_index)

	def class_index(self):
		"""Return the index of the class attribute.

		Return:
			int: The index of the class attribute.
			-1: If the class attribute is not defined.
		"""
		return self.__class_index

	def instance(self, index):
		"""Return the instance at the given index.

		Args:
			index (int): The index of the instance to be returned.

		Returns:
			Instance: The instance at the given index.
		"""
		return self.__instances[index]

	def num_attributes(self):
		"""Return the number of attributes of the dataset's instances.

		Return:
			int: The number of attributes of the dataset's instances.
		"""
		return len(self.__attributes)

	def num_classes(self):
		"""Return the number of possible values for the class attribute.

		Return:
			int: The number of class values, if class attribute is Nominal.
			1: If the class attribute is Numeric.
		"""
		if self.class_attribute().type() is 'Numeric':
			return 1
		else:
			return self.class_attribute().num_values()

	def num_instances(self):
		"""Return the number of instances in the dataset.

		Returns:
			int: The number of instances in the dataset.
		"""
		return len(self.__instances)

	def name(self):
		"""Return the name of the dataset.

		Return:
			str: The name of the dataset.
		"""
		return self.__name

	def set_class(self, attribute):
		"""Set the class attribute.

		Args:
			Attribute: The attribute to be set as class.
		"""
		self.__class_index = attribute.index()

	def set_class_index(self, class_index):
		"""Set the index of the class attribute.

		Args:
			int: The index of the attribute to be set as class.
		"""
		self.__class_index = class_index

	def set_name(self, name):
		"""Set the name of the dataset.

		Args:
			str: The new name of the dataset.
		"""
		self.__name = name

	def get_attributes(self):
		"""Return all attributes of the dataset's instances.

		Returns:
			list[Attribute]: A list containing all the attributes of the dataset's instances.
		"""
		return self.__attributes
