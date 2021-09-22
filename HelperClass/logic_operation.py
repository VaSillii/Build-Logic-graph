class EquivalentClass:
    def __init__(self, name=''):
        self.name = name
        self.elements = []

    def __str__(self):
        return '\nEquivalentClass ' + ' '.join(str(el) for el in self.elements)


class NestedElement:
    cluster_cnt = 1

    def __init__(self):
        self.elements = []
        self.flag_nested = False
        self.node = 'cluster_' + str(NestedElement.cluster_cnt)
        NestedElement.cluster_cnt += 1


class ArrowClass:
    def __init__(self, first_el, second_el, arrow_name: str):
        self.first_el = first_el
        self.second_el = second_el
        self.arrow_name = arrow_name
        self.flag_nested = True


class Node:
    _node_cnt = 1

    def __init__(self, name, flag_negation=False):
        self.name = name
        self.node = 'node_' + str(Node._node_cnt)
        Node._node_cnt += 1
        self.flag_nested = False
        self.flag_negation = flag_negation

    def __str__(self):
        return 'Node ' +self.name


class Negation(NestedElement):
    def __str__(self):
        return 'Negation '


class Intersection(NestedElement):
    def __str__(self):
        return 'Intersection' +str(self.elements)


class Union(NestedElement):
    def __str__(self):
        return 'Union ' + str(self.elements)


class UniversalRestriction(ArrowClass):
    def __str__(self):
        return 'UniversalRestriction ' + self.first_el + self.second_el + self.arrow_name


class ExistentionRestriction(ArrowClass):
    def __str__(self):
        return 'ExistentionRestriction ' + self.first_el + self.second_el + self.arrow_name


class SubclassOf(ArrowClass):
    def __str__(self):
        return self.first_el + self.second_el


class ElementOnto:
    def __init__(self, type_op, value_op):
        self.type_op = type_op
        self.value_op = value_op
        self.childs = []

    def add_child(self, elem):
        self.childs.append(elem)
