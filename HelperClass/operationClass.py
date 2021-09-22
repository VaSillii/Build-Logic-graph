class OperationClass(object):
    _node_cnt = 1

    def __init__(self, name: str, label_el: str = '', comment_el: str = ''):
        self.node_name = 'node_' + str(OperationClass._node_cnt)
        self.name = name
        self.label_el = label_el
        self.comment_el = comment_el
        self.equivalent_class = []
        self.sub_class_of = []

        OperationClass._node_cnt += 1

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name
