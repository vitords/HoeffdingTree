from ht.hnode import HNode
from ht.leafnode import LeafNode

class SplitNode(HNode):
    """A Hoeffding Tree node used for splits."""
    def __init__(self, class_distrib, split):
        super().__init__(class_distrib)
        self.split = split
        # Dict of tuples (branch, child)
        self.children = {}

    def branch_for_instance(self, instance):
        return self.split.branch_for_instance(instance)

    def is_leaf(self):
        return False

    def num_children(self):
        return len(self.children)

    def set_child(self, branch, child):
        self.children[branch] = child

    def leaf_for_instance(self, instance, parent, parent_branch):
        branch = self.branch_for_instance(instance)
        if branch is not None:
            child = self.children.get(branch, None)
            if child is not None:
                return child.leaf_for_instance(instance, self, branch)
            return LeafNode(None, self, branch)
        return LeafNode(self, parent, parent_branch)

    def update_node(self, instance):
        # Don't update the distribution
        pass 

    def _dump_tree(self, depth, leaf_count, buff):
        for branch, child in self.children.items():
            if child is not None:
                buff[0] += '\n'
                for i in range(depth):
                    buff[0] += '|   '
                buff[0] += '{0}: '.format(self.split.condition_for_branch(branch))
                leaf_count = child._dump_tree(depth + 1, leaf_count, buff)
        return leaf_count

    def install_node_nums(self, node_num):
        node_num = super().install_node_nums(node_num)

        for branch, child in self.children.items():
            if child is not None:
                node_num = child.install_node_nums(node_num)
        return node_num

    def _print_leaf_models(self, buff):
        for branch, child in self.children.items():
            if child is not None:
                child._print_leaf_models(buff)