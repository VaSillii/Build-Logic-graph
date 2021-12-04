import os
import re
import shutil
import time
from pathlib import Path
from graphviz import Source

from HelperClass.parse_onto import ParseOntology
from HelperClass.logic_operation import Intersection, Node, Negation, UniversalRestriction, \
    ExistentionRestriction, Union


class BuildGraph:
    def __init__(self, data, name_onto):
        self.data = data
        self.name_onto = name_onto
        self.graph = ''
        self.path = Path(__file__).absolute().parent.parent.joinpath(r'File\dot_files\graph_onto_1.dot')
        self.path_folder_graph = Path(__file__).absolute().parent.parent.joinpath(f'File\onto_graph\{self.name_onto}')
        BuildGraph.delete_folder(self.path_folder_graph)
        BuildGraph.create_folder(self.path_folder_graph)

    @staticmethod
    def delete_folder(path):
        if os.path.exists(path):
            shutil.rmtree(path)

    @staticmethod
    def create_folder(path):
        if not os.path.exists(path):
            os.mkdir(path)

    @staticmethod
    def _wrap_graph_in_diagram(initial_graph, graph):
        """
        Function wrap graph in diagram block
        :param graph:
        :return: Wrapping a graph in block diagrams
        """

        graph = 'digraph diagram_1  { \n' + \
                'node [shape=record fontsize=10 fontname="Verdana"];' + \
                '\tgraph [fontsize=10 fontname="Verdana" compound=true];\n' + \
                '\tcolor=white;\n' + \
                initial_graph + '\n' + \
                graph + \
                '\n}'
        return graph

    @staticmethod
    def _save_to_dot_file(path, graph):
        """
        Save to .dot file
        :return:
        """
        with open(path, 'w', encoding='utf-8') as f:
            f.write(graph)

    @staticmethod
    def get_nested_graph(graph, subgraph_name, label='', border_color='black', background='White'):
        graph_label = f'\tlabel=\"'
        if label != '':
            graph_label += label
        graph_label += '\";\n'
        intersection_graph = f'\nsubgraph {subgraph_name} ' + '{ \n' + \
                             f'\tnode [shape=record];\n' + \
                             '\tstyle=filled;\n' + \
                             graph_label + \
                             f'\tcolor={border_color};\n' + \
                             f'\tfillcolor={background};\n' + \
                             '\t' + graph + \
                             '\n}'
        return intersection_graph

    @staticmethod
    def inverse_color(background):
        if background.lower() == 'white':
            return 'lightgrey'
        else:
            return 'white'

    @staticmethod
    def get_node_graph(node: Node, border_color='black', background='white', flag_negation=False):
        background_neg = background

        if flag_negation:
            background_neg = BuildGraph.inverse_color(background_neg)
        graph = '\n\t' + node.node + f'[label=\"{node.name}\" style=filled, fillcolor={background_neg}, color={border_color}];'
        return graph

    @staticmethod
    def get_negation_graph(negation: Negation, flag_negation=False):
        if len(negation.elements) == 0:
            return '', ''

        negation_graph = ''
        negation_initial_graph = ''
        for element in negation.elements:
            inner_elm, graph = BuildGraph.get_graph_element(element, flag_negation=not flag_negation)

            negation_graph += graph
            negation_initial_graph += inner_elm
        return negation_initial_graph, negation_graph

    @staticmethod
    def get_graph_arrow_element(element, flag_change_color=False, flag_negation=False):
        arrow_graph = ''
        arrow_initial_graph = ''

        inner_elm, graph = BuildGraph.get_graph_element(element.first_el[0], flag_negation)
        arrow_initial_graph += inner_elm
        arrow_graph += graph

        if len(element.second_el) == 1 and element.second_el is not list:
            if type(element.second_el[0]) is Union and not flag_change_color:
                inter = Intersection()
                neg = Negation()
                neg.elements = element.second_el[0].elements
                # print(neg.elements)
                inter.elements = [neg]
                element.second_el[0] = inter
                # flag_negation = not flag_negation

            inner_elm, graph = BuildGraph.get_graph_element(element.second_el[0], flag_negation)
            arrow_initial_graph += graph
            arrow_graph += inner_elm
            return arrow_initial_graph, arrow_graph, element.second_el[0].node

        elm = None
        if flag_change_color:
            elm = Intersection().elements = element.second_el
        else:
            elm = Union().elements = element.second_el
        inner_elm, graph = BuildGraph.get_graph_element(elm, flag_negation)
        arrow_initial_graph += inner_elm
        arrow_graph += graph

        return arrow_initial_graph, arrow_graph, elm.node

    @staticmethod
    def get_arrow_graph(element, flag_change_color=False, flag_negation=False):
        arrow_graph = ''
        arrow_initial_graph = ''

        inner_elm, graph, node_cluster = BuildGraph.get_graph_arrow_element(element, flag_change_color, flag_negation)
        arrow_initial_graph += inner_elm
        arrow_graph += graph

        node_first = BuildGraph.get_name_nested_node(inner_elm)
        nested_node_second = BuildGraph.get_name_nested_node(graph)

        arrow_initial_graph += '\t' + nested_node_second + '->' + node_first + \
                               f' [ltail={node_first} lhead={node_cluster} label="{element.arrow_name}"]\n'
        return arrow_initial_graph, arrow_graph

    @staticmethod
    def get_intersection_graph(elements, border_color='black', background='white', flag_negation=False, flag_union=False):
        intersection_graph = ''
        intersection_initial_graph = ''

        flag = not flag_union and flag_negation
        for element in elements.elements:
            if flag:
                inner_elm, graph = BuildGraph.get_graph_element(element, flag_negation=not flag)
            else:
                # print(elements)
                inner_elm, graph = BuildGraph.get_graph_element(element, flag_negation=flag_negation)

            intersection_graph += graph
            intersection_initial_graph += inner_elm
        background_new = background
        if flag:
            background_new = BuildGraph.inverse_color(background)
        intersection_graph = BuildGraph.get_nested_graph(intersection_graph, elements.node, border_color=border_color,
                                                         background=background_new)
        return intersection_initial_graph, intersection_graph

    @staticmethod
    def get_graph_element(element, flag_negation=False):
        type_element = type(element)
        print(element, type_element)
        if type_element is Node:
            if element.flag_negation:
                return '', BuildGraph.get_node_graph(element, background='lightgrey', flag_negation=flag_negation)
            return '', BuildGraph.get_node_graph(element, flag_negation=flag_negation)
        elif type_element is Negation:
            return BuildGraph.get_negation_graph(element, flag_negation=flag_negation)
        elif type_element is UniversalRestriction:
            return BuildGraph.get_arrow_graph(element, flag_change_color=True, flag_negation=flag_negation)
        elif type_element is ExistentionRestriction:
            return BuildGraph.get_arrow_graph(element, flag_change_color=False, flag_negation=flag_negation)
        elif type_element is Intersection:
            return BuildGraph.get_intersection_graph(element, flag_negation=flag_negation)
        elif type_element is Union:
            return BuildGraph.get_intersection_graph(element, background='lightgrey', flag_negation=not flag_negation, flag_union=True)
        else:
            return '', ''

    @staticmethod
    def _handle_equivalent(elements: list):
        equivalent_graph = ''
        equivalent_initial_graph = ''

        for element in elements:
            if element is not None:
                inner_elm, graph = BuildGraph.get_graph_element(element)
                equivalent_graph += graph
                equivalent_initial_graph += inner_elm
        return equivalent_initial_graph, equivalent_graph

    @staticmethod
    def build_name_class(class_name, line_equivalent_class):
        if len(line_equivalent_class) == 0:
            return class_name
        class_name += ' (' + ', '.join(line_equivalent_class) + ')'
        return class_name

    @staticmethod
    def get_name_nested_node(graph: str):
        node_name = re.search('node_[0-9]+', graph)
        if node_name is not None:
            return node_name.group()
        return None

    @staticmethod
    def get_sub_class_of_nested_graph(sub_class_of):
        sub_graph = ''
        initial_graph = ''
        for element in sub_class_of.elements:
            if element is not None:
                inner_elm, graph = BuildGraph.get_graph_element(element)
                sub_graph += graph
                initial_graph += inner_elm
        return initial_graph, sub_graph

    @staticmethod
    def get_graph_subclass_of(class_graph, class_name, sub_class_of_list):
        class_initial_graph = ''
        class_sub_graph = ''

        nested_node = BuildGraph.get_name_nested_node(class_graph)
        for node_sub_class_of in sub_class_of_list:
            try:
                if node_sub_class_of is not None:
                    inner_elm, graph = BuildGraph.get_sub_class_of_nested_graph(node_sub_class_of)
                    nested_node_gr = BuildGraph.get_name_nested_node(graph)
                    class_initial_graph += inner_elm
                    class_sub_graph += graph
                    if len(node_sub_class_of.elements) == 1 and type(node_sub_class_of.elements[0]) is Node:
                        class_initial_graph += '\n\t' + nested_node + '->' + nested_node_gr + f' [ltail={class_name} lhead={nested_node} label="SubClassOf"]'
                    else:
                        class_initial_graph += '\n\t' + nested_node + '->' + nested_node_gr + f' [ltail={class_name} lhead={nested_node} label="SubClassOf"]'
            except:
                continue

        return class_initial_graph, class_sub_graph

    @staticmethod
    def get_graph_equivalent_class(equivalent_class_list):
        class_graph = ''
        class_initial_graph = ''
        line_equivalent_class = []

        for equivalent_class in equivalent_class_list:
            if len(equivalent_class.elements) == 0:
                line_equivalent_class.append(equivalent_class.name)
                continue
            inner_elm, graph = BuildGraph._handle_equivalent(equivalent_class.elements)
            class_graph += graph
            class_initial_graph += inner_elm
        return class_initial_graph, class_graph, line_equivalent_class

    @staticmethod
    def _handle_onto_class(class_onto):
        line_equivalent_class = []

        class_graph = ''
        class_initial_graph = ''
        if len(class_onto.equivalent_class) == 0:
            graph = BuildGraph.get_node_graph(Node(name=''), border_color='white')
            class_graph += graph
        else:
            inner_elm, graph, line_equivalent_class = BuildGraph.get_graph_equivalent_class(class_onto.equivalent_class)
            class_graph += graph
            class_initial_graph += inner_elm

        class_name = 'cluster_' + class_onto.name
        class_graph = BuildGraph.get_nested_graph(class_graph, class_name,
                                                  label=BuildGraph.build_name_class(class_onto.name,
                                                                                    line_equivalent_class))

        if class_onto.sub_class_of:
            inner_elm, graph = BuildGraph.get_graph_subclass_of(class_graph, class_name, class_onto.sub_class_of)
            class_initial_graph += inner_elm
            class_graph += graph

        return class_initial_graph, class_graph

    def create_graph(self):
        graph_main = ''
        graph_main_initial = ''

        # inner_elm, graph = BuildGraph._handle_onto_class(self.data[1])
        # graph_main += graph
        # graph_main_initial += inner_elm

        for class_onto in self.data:
            inner_elm, graph = BuildGraph._handle_onto_class(class_onto)
            graph_main = graph
            graph_main_initial = inner_elm
            graph_main = BuildGraph._wrap_graph_in_diagram(graph_main_initial, graph_main)
            path_folder_onto = self.path_folder_graph.joinpath(f'{class_onto.name}\{class_onto.name}.dot')
            BuildGraph.create_folder(self.path_folder_graph.joinpath(f'{class_onto.name}'))

            self._save_to_dot_file(path_folder_onto, graph_main)
            s = Source.from_file(path_folder_onto)
            s.view()


if __name__ == '__main__':
    path = Path(__file__).absolute().parent.parent.joinpath(r'File\family.owl')
    path = Path(__file__).absolute().parent.parent.joinpath(r'File\ontology family_1.owl')
    parse_onto = ParseOntology(path)
    parse_onto.parse()
    data = parse_onto.class_onto
    BuildGraph(data).create_graph()
    # print(data.class_onto[0].equivalent_class[0].elements[0].name)
