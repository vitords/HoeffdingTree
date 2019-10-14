from abc import ABCMeta, abstractmethod
from ht.weightmass import WeightMass
from core import utils

class HNode(metaclass=ABCMeta):
    """Base for the Hoeffding Tree nodes.

    Args:
        class_distribution (dict): The class distribution used to create the node. (default None)
    """
    def __init__(self, class_distribution=None):
        if class_distribution is None:
            # Dict of tuples (class value, WeightMass)
            class_distribution = {}
        self.class_distribution = class_distribution
        self._leaf_num = None
        self._node_num = None

    def __str__(self, print_leaf=False):
        self.install_node_nums(0)
        # Wrapper for a string
        buff = ['']
        self._dump_tree(0, 0, buff)
        if print_leaf:
            buff[0] += "\n\n"
            self._print_leaf_models(buff)
        # Returns only the string
        return buff[0]

    def is_leaf(self):
        return True

    def num_entries_in_class_distribution(self):
        return len(self.class_distribution)

    def class_distribution_is_pure(self):
        count = 0
        for class_value, mass in self.class_distribution.items():
            if mass.weight > 0:
                count += 1
                if count > 1:
                    break
        return count < 2

    def update_distribution(self, instance):
        if instance.class_is_missing():
            return
        class_val = instance.string_value(attribute=instance.class_attribute())
        mass = self.class_distribution.get(class_val, None)
        if mass is None:
            mass = WeightMass()
            mass.weight = 1.0
            self.class_distribution[class_val] = mass

        self.class_distribution[class_val].weight += instance.weight()

    def get_distribution(self, instance, class_attribute):
        dist = [0.0 for i in range(class_attribute.num_values())]

        for i in range(class_attribute.num_values()):
            mass = self.class_distribution.get(class_attribute.value(i), None)
            if mass is not None:
                dist[i] = mass.weight
            else:
                dist[i] = 1.0

        dist = utils.normalize(dist)
        return dist

    def install_node_nums(self, node_num):
        node_num += 1
        self._node_num = node_num
        return node_num

    def _dump_tree(self, depth, leaf_count, buff):
        max_value = -1
        class_val = ''
        for class_value, mass in self.class_distribution.items():
            if mass.weight > max_value:
                max_value = mass.weight
                class_val = class_value
        buff[0] += '{0} ({1})'.format(class_val, max_value)
        leaf_count += 1
        self._leaf_num = leaf_count
        return leaf_count

    def _print_leaf_models(self, buff):
        pass

    def total_weight(self):
        tw = 0.0
        for class_value, mass in self.class_distribution.items():
            tw += mass.weight
        return tw

    def leaf_for_instance(self, instance, parent, parent_branch):
        from ht.leafnode import LeafNode
        return LeafNode(self, parent, parent_branch)

    @abstractmethod
    def update_node(self, instance):
        pass