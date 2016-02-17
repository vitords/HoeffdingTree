import math

# TODO: Make constructor identify the attribute type by itself?
class Attribute(object):
	def __init__(self, name, values=None, att_type=None, index=-1):
		self.__name = name
		self.__index = index
		if values is not None:
			self.__values = values
		else:
			self.__values = None
		self.__att_type = att_type
		self.__lower_bound = None
		self.__upper_bound = None

	def index(self):
		return self.__index

	def index_of_value(self, value):
		if self.__att_type is 'Nominal':
			return self.__values.index(value)
		else:
			return -1

	def name(self):
		return self.__name
	
	def num_values(self):
		if self.__att_type == 'Numeric':
			return 0
		else:
			return len(self.__values)

	def type(self):
		return self.__att_type

	def value(self, index):
		if self.__att_type is not 'Nominal':
			return ""
		else:
			return self.__values[index] 

	def add_value(self, value):
		self.__values.append(value)

	def set_type(self, att_type):
		self.__att_type = att_type

	def set_numeric_range(self, lower_bound=-math.inf, upper_bound=math.inf):
		self.__lower_bound = lower_bound
		self.__upper_bound = upper_bound

	def lower_bound(self):
		return self.__lower_bound

	def upper_bound(self):
		return self.__upper_bound

	def __str__(self):
		return 'Attribute \'{0}\' ({1})\n   Index: {2}\n   Values: {3}'.format(
			self.__name, self.__att_type, self.__index, self.__values)