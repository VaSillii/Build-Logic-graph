import os
from datetime import datetime
from pathlib import Path
from graphviz import Digraph, Source
from configuration import get_path_graphviz


os.environ["PATH"] += os.pathsep + get_path_graphviz()


class BuildGraph(object):
    def __init__(self, graph_dict: dict):
        """Constructor"""
        self.graph_dict = graph_dict
        self.NODE_NUMBER = 0
        self.elements = {
            'node': [],
            'cluster': []
        }

        self.graph = ''
        # self.path = Path(__file__).absolute().parent.joinpath(f'File\\dot_files\\{str(datetime.now())}.dot')
        self.path = Path(__file__).absolute().parent.joinpath(r'File\dot_files\test_new.dot')

    @staticmethod
    def _check_empty_val(val: str):
        return True if val != '' else False

    @staticmethod
    def _save_to_dot_file(path: str, graph: str):
        """
        Save to .dot file
        :param path: Path to file
        :param graph: Description graph
        :return:
        """
        with open(path, 'w', encoding='utf-8') as f:
            f.write(graph)

    def _generate_cluster_name(self):
        self.NODE_NUMBER += 1
        cluster_name = 'cluster_' + str(self.NODE_NUMBER)
        return cluster_name

    def _get_last_element(self, key: str):
        if len(self.elements[key]) != 0:
            return self.elements[key][-1]
        else:
            return ''

    def _get_last_node(self):
        """
        Get last node
        :return: Name node graph
        """
        return self._get_last_element('node')

    def _get_last_cluster(self):
        """
        Get last cluster
        :return: Name cluster graph
        """
        return self._get_last_element('cluster')

    def _add_element(self, node: str, cluster: str):
        """
        Add new element graph
        :param label: Label element
        :param node: Node name
        :param cluster: Cluster name
        :return:
        """
        if self._check_empty_val(node):
            self.elements['node'].append(node)
        if self._check_empty_val(cluster):
            self.elements['cluster'].append(cluster)

    def _node_elm(self, node: str, fill_color: str = 'white', border_color: str = 'black'):
        """
        Get wrap node element
        :param node: Name node element
        :param fill_color: Background color node element
        :param border_color: Color border node element
        :return: Graph node element
        """
        self.NODE_NUMBER += 1
        node_name = 'node' + str(self.NODE_NUMBER)

        graph = '\n\t' + node_name + f'[label=\"{node}\" style=filled, fillcolor={fill_color}, color={border_color}];'
        self._add_element(node_name, '')
        return graph

    def _negation(self, node):
        """
        Function negation node
        :param node: Node element
        :return: Negation node
        """
        return self._node_elm(node, 'lightgrey')

    def _generate_subgraph(self, nodes: str, label: str = '', fill_color: str = 'white', border_color: str = 'black'):
        """
        Generation subgraph element
        :param nodes: Nested graph elements
        :param label: Name operation
        :param fill_color: Background color node element
        :param border_color: Color border node element
        :return: Nested graph
        """
        cluster_name = self._generate_cluster_name()

        graph_label = f'\tlabel=\"'
        if label != '':
            graph_label += label
        graph_label += '\";\n'

        graph = f'\nsubgraph {cluster_name} ' + '{ \n' + \
                f'\tnode [shape=record];\n' + \
                '\tstyle=filled;\n' + \
                graph_label + \
                f'\tcolor={border_color};\n' + \
                f'\tfillcolor={fill_color};\n' + \
                '\t' + nodes + \
                '\n}'
        self._add_element('', cluster_name)
        return graph

    def _conjunction(self, graph):
        """
        Generate conjunction element
        :param nodes: Nodes graph
        :return: conjunction element
        """
        return self._generate_subgraph(graph)

    def _disjunction(self, graph):
        """
        Function get disjunction element
        :param nodes: Nodes graph
        :return: disjunction element
        """
        return self._generate_subgraph(graph, fill_color='lightgrey')

    def _generate_subgraph_arrow(self, name_arrow: str, domain_el: dict, addition_el: dict, fill_color: str = 'white',
                                 border_color: str = 'white'):
        """
        Function get graph arrow type
        :param name_arrow: Arrow name
        :param domain_el: Domain element graph
        :param addition_el: Addition element graph
        :param fill_color: Background color node element
        :param border_color: Color border node element
        :return: Arrow graph
        """
        graph = ''
        graph_domain = self._generate_subgraph(domain_el['graph'], fill_color=fill_color, border_color=border_color)
        cluster_domain = self._get_last_cluster()

        graph_addition = self._generate_subgraph(addition_el['graph'], fill_color=fill_color, border_color=border_color)
        cluster_addition = self._get_last_cluster()

        graph += graph_domain + '\n' + \
                 graph_addition + '\n' + \
                 domain_el['node'] + '->' + addition_el['node'] + \
                 f' [ltail={cluster_domain} lhead={cluster_addition} label="{name_arrow}"]\n'
        return graph

    def _subgraph_arrow(self, graph_dict: dict, fill_color: str = 'white', border_color: str = 'white'):
        """
        Generate subgraph arrow element
        :param graph_dict: Dictionary description graph
        :param fill_color: Background color node element
        :param border_color: Color border node element
        :return: subgraph object
        """
        domain_el = {
            'graph': self._handle_data_graph(graph_dict['graph'][0]) if len(
                graph_dict['graph'][0]) != 0 else self._node_elm('', fill_color=fill_color, border_color=fill_color),
            'node': self._get_last_node()
        }
        addition_el = {
            'graph': self._handle_data_graph(graph_dict['graph'][1]),
            'node': self._get_last_node()
        }
        return self._generate_subgraph_arrow(graph_dict['property'], domain_el, addition_el, fill_color=fill_color,
                                             border_color=border_color)

    def _assertion(self, a, c):
        return self._generate_subgraph(a, label=c)

    def _wrap_graph_in_diagram(self):
        """
        Function wrap graph in diagram block
        :param graph:
        :return: Wrapping a graph in block diagrams
        """
        self.NODE_NUMBER += 1

        self.graph = 'digraph diagram_' + str(self.NODE_NUMBER) + ' { \n' + \
                     'node [shape=record fontsize=10 fontname="Verdana"];' + \
                     '\tgraph [fontsize=10 fontname="Verdana" compound=true];\n' + \
                     '\tcolor=white;\n' + \
                     self.graph + \
                     '\n}'

    def _handle_data_graph(self, desc_dict: dict):
        """
        Handle data field graph dictionary
        :param desc_dict: Graph dictionary
        :rtype: str
        """
        graph = ''
        if 'op' in desc_dict:
            return self._get_graph(desc_dict)

        for el in desc_dict:
            graph += self._get_graph(el)
        return graph

    def _get_graph(self, graph_dict: dict):
        """
        Function get graph in dot format
        :param graph_dict: Graph description dictionary
        :return:
        """
        graph = ''
        if graph_dict['op'] == 'name':
            graph = graph_dict['data'] + graph
        elif graph_dict['op'] == 'list':
            graph = self._handle_data_graph(graph_dict['data']) + graph
        elif graph_dict['op'] == 'node':
            graph = self._node_elm(graph_dict['data']) + graph
        elif graph_dict['op'] == 'negation':
            graph = self._negation(graph_dict['data']) + graph
        elif graph_dict['op'] == 'equivalence':
            graph = self._node_elm(f"{graph_dict['data'][0]}({graph_dict['data'][1]})") + graph
        elif graph_dict['op'] == 'conjunction':
            graph = self._conjunction(self._handle_data_graph(graph_dict['data'])) + graph
        elif graph_dict['op'] == 'disjunction':
            graph = self._disjunction(self._handle_data_graph(graph_dict['data'])) + graph
        elif graph_dict['op'] == 'concept_assertion':
            graph = self._assertion(self._handle_data_graph(graph_dict['data']['graph']),
                                    graph_dict['data']['property']) + graph
        elif graph_dict['op'] == 'universal_restriction':
            graph = self._subgraph_arrow(graph_dict['data'], fill_color='lightgrey') + graph
        elif graph_dict['op'] == 'existential_restriction':
            graph = self._subgraph_arrow(graph_dict['data'], fill_color='white') + graph
        elif graph_dict['op'] == 'role_assertion':
            graph = self._subgraph_arrow(graph_dict['data'], fill_color='white') + graph
        elif graph_dict['op'] == 'sub_class_of':
            graph = self._subgraph_arrow(graph_dict['data']) + graph
        return graph

    def create_graph(self):
        """
        Function create graph
        :return:
        """
        self.graph = self._get_graph(self.graph_dict)
        self._wrap_graph_in_diagram()
        self._save_to_dot_file(self.path, self.graph)
        s = Source.from_file(self.path)
        s.view()


if __name__ == '__main__':
    graph_dict = {
        "op": "list",
        "data": [
            {
                "op": "list",
                "data": [
                    {
                        "op": "node",
                        "data": "Жанр1"
                    },
                    {
                        "op": "negation",
                        "data": "Domain1asd1"
                    }
                ]
            },
            {"op": "conjunction",
             "data": [
                 {
                     "op": "node",
                     "data": "node4"
                 },
                 {
                     "op": "negation",
                     "data": "node5"
                 }]
             },
            {
                "op": "node",
                "data": "Жанр"
            },
            {
                "op": "negation",
                "data": "Domain1asd"
            }
        ]
    }
    graph_dict = {"op": "list",
                  "data": [
                      {"op": "conjunction",
                       "data": [
                           {
                               "op": "node",
                               "data": "node4"
                           },
                           {
                               "op": "equivalence",
                               "data": ["c1", "c2"]
                           },
                           {
                               "op": "negation",
                               "data": "node5"
                           }]
                       },
                      {
                          "op": "negation",
                          "data": "node2"
                      },
                      {
                          "op": "negation",
                          "data": "node2"
                      },
                      {"op": "sub_class_of",
                       "data": {
                           'graph': [
                               [
                                   {"op": "disjunction",
                                    "data": [
                                        {
                                            "op": "node",
                                            "data": "node4"
                                        },
                                        {
                                            "op": "negation",
                                            "data": "node5"
                                        }]
                                    }
                               ],
                               [{
                                   "op": "negation",
                                   "data": "node6"
                               }],
                           ],
                           'property': 'SubClassOf'
                       }}
                  ]}
    # graph_dict = {"op": "universal_restriction",
    #               "data": {
    #                   'graph': [
    #                       [],
    #                       [{
    #                           "op": "negation",
    #                           "data": "node6"
    #                       }
    #                       ]],
    #                   'property': 'test'}
    #               }
    BuildGraph(graph_dict).create_graph()

