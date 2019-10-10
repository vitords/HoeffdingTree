from ht.split import Split

class UnivariateNominalMultiwaySplit(Split):
    """Multiway split based on a nominal attribute."""
    def __init__(self, att_name):
        super().__init__()
        self._split_att_names.append(att_name)

    def branch_for_instance(self, instance):
        att = instance.dataset().attribute(name=self._split_att_names[0])
        if att is None or instance.is_missing(att.index):
            return None
        return att.value(instance.value(attribute=att))

    def condition_for_branch(self, branch):
        return '{0} = {1}'.format(self._split_att_names[0], branch)