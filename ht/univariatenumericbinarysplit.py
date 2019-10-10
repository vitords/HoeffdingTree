from ht.split import Split

class UnivariateNumericBinarySplit(Split):
    """Binary split based on a numeric attribute."""
    def __init__(self, att_name, split_point):
        super().__init__()
        self._split_att_names.append(att_name)
        self._split_point = split_point

    def branch_for_instance(self, instance):
        att = instance.dataset().attribute(name=self._split_att_names[0])
        if att is None or instance.is_missing(att.index):
            return None
        if instance.value(attribute=att) <= self._split_point:
            return 'left'
        return 'right'

    def condition_for_branch(self, branch):
        result = self._split_att_names[0]
        if branch is 'left':
            result += ' <= '
        else:
            result += ' > '
        result += '{0}'.format(self._split_point)
        return result