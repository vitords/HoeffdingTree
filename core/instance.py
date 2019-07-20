from core.attribute import Attribute
import math

class Instance(object):
    """A class for handling an instance. 
    All the values of the instance's attributes are stored as floating-point numbers.
    If the attribute is Nominal, the value corresponds to its index in the attribute's definition.

    Note:
        This class is based on the Weka implementation (weka.core.Instance) to make porting existing 
        Java algorithms an easier task.
        Weka developers chose this approach of storing only Numeric values inside the instance,
        while Nominal values are stored in an Attribute object and only the index for its value is
        stored in an instance. Although confusing at first, it makes instance handling less messy
        since it only needs to take care of numbers (instead of numbers and strings).

    Args:
        att_values (list[float]): The instances's attribute values. (default None)

    Raises:
        TypeError: If att_values is None.
    """

    def __init__(self, att_values):
        if att_values is None:
            raise TypeError('Instance should be created with a list of attribute values.')
        # The list of attribute values for the instance.
        self.__att_values = att_values
        # The dataset with which this instance is associated (has access to its properties and/or attributes).
        self.__dataset = None
        self.__weight = 1

    def __str__(self):
        return 'Instance\n   From dataset: {0}\n   Attribute values: {1}\n   Class: {2}'.format(
            self.__dataset.name() if self.__dataset is not None else 'This instance is not associated with a dataset.',
             self.__att_values, 'A dataset is required to set an attribute as class.' if self.__dataset is None else self.__att_values[self.__dataset.class_index()])

    def attribute(self, index):
        """Return the attribute with the given index.

        Args:
            index (int): The index of the attribute to be returned.

        Returns:
            Attribute: The attribute at the given index.
        """
        #TODO: Should check if the instance is associated to a dataset.
        return self.__dataset.attribute(index)

    def class_attribute(self):
        """Return the instance's class attribute. It is always its dataset's class attribute.

        Returns:
            Attribute: The class attribute of the instance.
        """
        return self.__dataset.class_attribute()

    def class_index(self):
        """Return the instance's index of the class attribute.

        Returns:
            int: The class attribute's index of the instance.
        """
        #TODO: Should check if the instance is associated to a dataset.
        return self.__dataset.class_index()

    def class_is_missing(self):
        """Test if the instance is missing a class.

        Returns:
            bool: True if the instance's class is missing, False otherwise.

        Raises:
            ValueError: If class is not set for the instance.
        """
        if self.class_index() < 0:
            raise ValueError("Class is not set.")
        return self.is_missing(self.class_index())

    def class_value(self):
        """Return the class value of the instance. 
        If class attribute is Nominal, return the index of its value in the attribute's definition.

        Returns:
            int: The class attribute's index of the instance.

        Raises:
            ValueError: If the class attribute is not set in the dataset with which the instance is associated.
        """
        if self.class_index() < 0:
            raise ValueError('Class attribute is not set.')
        return self.value(index=self.class_index())

    def dataset(self):
        """Return the dataset this instance is associated with.

        Returns:
            Dataset: The dataset this instance is associated with.
        """
        return self.__dataset

    def is_missing(self, att_index):
        """Test if a value is missing.

        Args:
            att_index (int): The index of the attribute to be tested.

        Returns:
            bool: True if value is missing, False otherwise.
        """
        if math.isnan(self.__att_values[att_index]):
            return True
        else:
            return False 

    def num_attributes(self):
        """Return the number of attributes of the instance.

        Returns:
            int: The number of attributes of the instance.
        """
        return len(self.__att_values)

    def num_classes(self):
        """Return the number of possible class values if class attribute is Nominal.
        If class attribute is Numeric it always returns 1.

        Returns:
            int: The number of possible class values if class attribute is Nominal.
            int: 1 if class attribute is Numeric.
        """
        return self.__dataset.num_classes()

    def num_values(self):
        """Return the number of the instance's values for its attributes.
        Always the same as self.num_attributes() since each instance has only one value set for each attribute.
        
        Returns:
            int: The number of the instance's values for its attributes.
        """
        return len(self.__att_values)

    def set_class_value(self, value):
        """Set the class value of the instance to the given value.

        Args:
            value (float): The value to be set as the instance's class value.
        """
        self.set_value(self.class_index(), value)

    def set_dataset(self, dataset):
        """Set the dataset to which the instance is associated.
        The dataset will not know about this instance so any changes in the dataset affecting its instances will not account for this instance.

        Args:
            Dataset: The dataset to which the instance is associated.
        """
        self.__dataset = dataset

    def set_value(self, att_index, value):
        """Set the instance's attribute at att_index to the given value.

        Note:
            Arg value can be either a float (for Numeric attributes) or a str (for Nominal attributes).

        Args:
            att_index (int): The index of the attribute to be set.
            value (float): A Numeric value to be set to the attribute at the given index.
            value (str): A Nominal value to be set to the attribute at the given index.
        """
        if isinstance(value, str):
            # Attribute is Nominal
            value_index = self.attribute(att_index).index_of_value(value)
        else:
            #Attribute is Numeric
            value_index = att_index
        self.__att_values[value_index] = value

    def set_weight(self, weight):
        """Set the weight of the instance.

        Args:
            weight (float): The weight.
        """
        self.__weight = weight

    def string_value(self, att_index=None, attribute=None):
        """Return the value of the attribute as a string.

        Args:
            att_index (int): The index of the attribute. (default None)
            attribute (Attribute): The attribute for which the value is to be returned. (default None)

        Returns:
            str: The value of the attribute as a string.
        """
        if attribute is None:
            attribute = self.__dataset.attribute(att_index)
        if att_index is None:
            att_index = attribute.index()
        if self.is_missing(att_index):
            return '?'
        return attribute.value(self.value(index=att_index))

    def value(self, index=None, attribute=None):
        """Return the value of an intance's attribute.

        Args:
            index (int): The index of the attribute which its value is to be returned.
            attribute (Attribute): The attribute which its value is to be returned.

        Returns:
            float: The instance's attribute value.
        """
        if index is not None:
            return self.__att_values[index]
        else:
            return self.__att_values[attribute.index()] 

    def weight(self):
        """Return the weight of the instance.

        Returns:
            float: The weight of the instance.
        """
        return self.__weight

    def get_attributes(self):
        """Return all attributes of the instance.

        Returns:
            list[Attribute]: A list containing all the attributes of the instance.
        """
        attributes = [None for i in range(self.num_attributes())]
        for i in range(self.num_attributes()):
            attributes[i] = self.attribute(i)
        return attributes