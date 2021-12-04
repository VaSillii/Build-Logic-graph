class NumberElementStatic:
    cluster_cnt = 1
    node_cnt = 1


class EquivalentClass:
    def __init__(self, name=''):
        self.name = name
        self.elements = []

    def __str__(self):
        return '\nEquivalentClass ' + ' '.join(str(el) for el in self.elements)


class NestedElement:
    def __init__(self):
        self.elements = []
        self.flag_nested = False
        self.node = 'cluster_' + str(NumberElementStatic.cluster_cnt)
        NumberElementStatic.cluster_cnt += 1


class ArrowClass:
    def __init__(self):
        self.first_el = []
        self.second_el = []
        self.arrow_name = ''
        self.flag_nested = True
        self.node = 'cluster_' + str(NumberElementStatic.cluster_cnt)
        NumberElementStatic.cluster_cnt += 1


class Node:
    def __init__(self, name, flag_negation=False):
        self.name = name
        self.node = 'node_' + str(NumberElementStatic.node_cnt)
        NumberElementStatic.node_cnt += 1
        self.flag_nested = False
        self.flag_negation = flag_negation

    def __str__(self):
        return 'Node ' + self.name


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
        return 'UniversalRestriction ' + str(self.first_el) + str(self.second_el) + self.arrow_name


class ExistentionRestriction(ArrowClass):
    def __str__(self):
        return 'ExistentionRestriction ' + str(self.first_el) + str(self.second_el) + self.arrow_name


class SubclassOf(NestedElement):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'SubclassOf' +str(self.elements)


class ElementOnto:
    def __init__(self, type_op, value_op):
        self.type_op = type_op
        self.value_op = value_op
        self.childs = []

    def add_child(self, elem):
        self.childs.append(elem)
