class Attribute(object):
	"""A class for handling an attribute. 
	Attribute can be either numeric or nominal and should never be changed after creation.

	Note:
		This class is based on the Weka implementation (weka.core.Attribute) to make porting existing 
		Java algorithms an easier task.

	Args:
		name (str): The name of the attribute.
		values (list[str]): A list of possible attribute values. (default None)
		att_type (str): The type of the attribute. Should be 'Numeric' or 'Nominal'. (default None)
		index (int): The index of the attribute in the attribute set. 
			If the attribute is not yet part of a set, its index is -1. (default -1)

	Raises:
		ValueError: If att_type is not 'Numeric' or 'Nominal'.

	"""
	
	# TODO: Make constructor identify the attribute type by using the args received.
	def __init__(self, name, values=None, att_type=None, index=-1):
		# The name of the attribute
		self.name = name
		# The possible values of the attribute, if Nominal
		self.__values = values
		# The type of the attribute
		if att_type not in ['Numeric', 'Nominal']:
			raise ValueError(
				f'Attribute type should be \'Numeric\' or \'Nominal\'. {att_type} is not a supported attribute type.'
			)
		self.att_type = att_type
		# The index of the attribute
		self.index = index

	def __str__(self):
		return f'Attribute \'{self.name}\' ({self.att_type})\n   Index: {self.index}\n   Values: {self.__values}'

	def index_of_value(self, value):
		"""Return the index of the first occurrence of an attribute value.

		Note:
			Since no values are stored in the Attribute class for Numeric attributes,
			a valid index is only returned for Nominal attributes.

		Args:
			value (str): The value for which the index should be returned.

		Returns:
			int: The index of a given attribute value if attribute is Nominal.
			int: -1 if attribute is Numeric.
		"""
		if self.att_type is 'Nominal':
			if value not in self.__values:
				self.add_value(value)	    
			return self.__values.index(value)
		else:
			return -1

	def is_numeric(self):
		"""Test if attribute is Numeric.

		Returns:
			bool: True if the attribute is Numeric, False otherwise.
		"""
		return self.att_type is 'Numeric'

	def num_values(self):
		"""Return the number of possible values for the attribute.

		Returns:
			int: Number of possible values if attribute is Nominal.
			int: 0 if attribute is Numeric.
		"""
		if self.att_type == 'Nominal':
			return len(self.__values)
		else:
			return 0

	def value(self, index):
		"""Return the value of the attribute at the given index.

		Args:
			index (int): The index of the attribute value to return.

		Returns:
			str: The value of attribute at the given position, if the attribute is Nominal.
			str: An empty string if the attribute is Numeric.
		"""
		if self.att_type is not 'Nominal':
			return ''
		else:
			return self.__values[index]

	def add_value(self, value):
		"""Add a new value to the attribute. 
		The value is always added to the end of the list of possible attribute values.

		Args:
			value (str): The new attribute value to be added.
		"""
		self.__values.append(value)

