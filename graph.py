from datetime import datetime
from pathlib import Path
from graphviz import Digraph, Source

node_cnt = 0
def get_node_cluster(node_cluster: int = 0):
    node_cluster += 1
    return node_cluster


def get_path_onto(name_elm: str):
    '''
    Function get full path ontology element
    :param name_elm:
    :return:
    '''
    path = 'http://www.semanticweb.org/vasilii/ontologies/2021/3/book_onto'
    return path + '#' + name_elm


def get_op_cluster(op_cluster: int = 0):
    op_cluster += 1
    return op_cluster


def node_elm(node: str, color: str = 'white'):
    # node_cnt = get_node_cluster(node_cnt)
    node_number = str()
    cluster_name = 'cluster_' + node_number
    graph = f'\nsubgraph {cluster_name} ' + "{\n" +\
            f'\tnode[shape=record, width=0.5, style=filled, fillcolor={color}];\n\t' + \
            'color=black;' + \
            node  + f'[label=\"{node}\"]' \
            '; \n}'
    # return 1
    return {'cluster_name': cluster_name, 'node': node, 'graph': graph }


def nested_element(operation, color: str, nodes: str):
    cluster_name = f'cluster_{operation}{get_op_cluster()}'
    graph = f'\nsubgraph cluster_{operation}' + '{ \n' + \
            f'\tnode [shape=record,style=filled];color={color};\n' + \
            '\tstyle=filled;\n' + \
            f'\tcolor={color};\n' + \
            '\t' + nodes + \
            '\n}'
    return graph


def generate_subgraph_arrow(name_arrow: str, nodes: list):
    """
    Function get graph arrow type
    :param name_arrow: Arrow name
    :param nodes: List nodes graph
    :return: Arrow graph
    """
    graph = f'\nsubgraph cluster_{name_arrow}' + ' {\n' + \
            'node [shape=record,style=filled, fillcolor=white]; color=white;\n' + \
            f'\t{nodes[0]} -> {nodes[1]} [label="{name_arrow}"];' + \
            '\n}'
    return graph


def conjunction(nodes):
    """
    Function get conjunction element
    :param nodes: Nodes graph
    :return: conjunction element
    """
    return nested_element('conjunction', 'white', nodes)


def disjunction(nodes):
    """
    Function get disjunction element
    :param nodes: Nodes graph
    :return: disjunction element
    """
    return nested_element('disjunction', 'lightgrey', nodes)


def negation(node):
    """
    Function negation node
    :param node: Node element
    :return: Negation node
    """
    return node_elm(node, 'lightgrey')


def sub_class_of(nodes: list):
    """
    Function create subClassOf object
    :param nodes: Nodes for subClassOf
    :return: subgraph object
    """
    # nodes = ['n', 'n1']
    return generate_subgraph_arrow('SubClassOf', nodes)


def wrap_diagram(graph: str):
    """
    Function wrap graph in diagram block
    :param graph:
    :return: Wrapping a graph in block diagrams
    """
    graph = 'digraph diagram_1 { \n' + \
            '\tgraph [fontsize=10 fontname="Verdana" compound=true];\n' +\
            '\tnode [shape=record fontsize=10 fontname="Verdana"];\n' +\
            'color=white;' +\
            graph +\
            '\n}'
    return graph
    # return 'digraph diagram_1 { \n\tnode[shape=record]\n\t' + graph + '\n}'


def save_to_dot_file(path: str, graph: str):
    """
    Save to .dot file
    :param path: Path to file
    :param graph: Description graph
    :return:
    """
    with open(path, 'w') as f:
        f.write(graph)


def handle_data_graph(desc_dict: dict):
    graph = ''
    if 'op' in desc_dict:
         return get_graph(desc_dict)

    for el in desc_dict:
        graph += get_graph(el)
    return graph


def get_graph(graph_dict: dict):
    """
    Function get graph in dot format
    :param graph_dict: Graph description dictionary
    :return: Graph in dot format
    """
    # data_graph = {'graph': '', 'nodes': [], 'clusters':[]}
    graph = ''
    # print(graph_dict)
    if graph_dict['op'] == 'name':
        graph += graph_dict['data']
    elif graph_dict['op'] == 'node':
        data_node = node_elm(graph_dict['data'])['graph']
        # data_graph['graph'] += data_node['graph']
        # data_graph['node'].append(data_node['node'])
        # data_graph['clusters'].append(data_node['cluster_name'])
        graph += node_elm(graph_dict['data'])['graph']
    elif graph_dict['op'] == 'negation':
        graph += negation(graph_dict['data'])['graph']
    elif graph_dict['op'] == 'conjunction':
        graph += conjunction(handle_data_graph(graph_dict['data']))
    elif graph_dict['op'] == 'disjunction':
        graph += disjunction(handle_data_graph(graph_dict['data']))
    elif graph_dict['op'] == 'sub_class_of':
        print(handle_data_graph(graph_dict['data'][0]))
        data_sub_class_of = [handle_data_graph(graph_dict['data'][0]), handle_data_graph(graph_dict['data'][1])]
        # print(data_sub_class_of)
        graph += sub_class_of(data_sub_class_of)
    elif graph_dict['op'] == 'classes':
        graph += handle_data_graph(graph_dict['data'])
    return graph


def create_graph(desc_dict: dict):
    """
    Function create graph
    :param desc_dict: Description dictionary graph
    :return: Graph in dot format
    """
    graph = ''
    # path = f'File/dot_files/{str(datetime.now())}.dot'
    path = f'File/dot_files/test6.dot'
    # save_to_dot_file(path, wrap_diagram(get_graph(desc_dict)))
    s = Source.from_file(path)
    s.view()


if __name__ == '__main__':
    graph_dict = {
        # 'op': 'sub_class_of',
        'op': 'disjunction',
        'data': [
            {
                "op": "sub_class_of",
                "data": [
                    {
                        "op": "node",
                        "data": "Domain"
                    },
                    {
                        "op": "name",
                        "data": "Domain1"
                    }
                ],
            },
            # {"op": "conjunction",
            #  "data": [
            #      {
            #          "op": "node",
            #          "data": "node1"
            #      },
            #      {
            #          "op": "node",
            #          "data": "node2"
            #      }
            #  ]}

                 # {
                 #     "op": "disjunction",
                 #     "data": [
                 #         {
                 #             "op": "node",
                 #             "data": "node1"
                 #         },
                 #         {
                 #             "op": "node",
                 #             "data": "node2"
                 #         },
                 #         {"op": "conjunction",
                 #          "data": [
                 #              {
                 #                  "op": "node",
                 #                  "data": "node3"
                 #              },
                 #              {
                 #                  "op": "negation",
                 #                  "data": "node4"
                 #              },
                 #          ]}
                 #     ]
                 # }
        ]
    }
    graph_dict = {
        "op": "sub_class_of",
        "data": [
            {
                "op": "name",
                "data": "Domain"
            },
            {
                "op": "name",
                "data": "Domain1"
            }
        ]}
    # graph_dict = {
    #                     "op": "name",
    #                     "data": "Domain"
    #                 }
    graph_dict = {
        "op": "disjunction",
        "data": [
            {
                "op": "node",
                "data": "node1"
            },
            {
                "op": "node",
                "data": "node2"
            },
            {"op": "conjunction",
             "data": [
                 {
                     "op": "node",
                     "data": "node3"
                 },
                 {
                     "op": "negation",
                     "data": "node4"
                 },
             ]}
        ]
    }

    graph_dict = {"op": "conjunction",
             "data": [
                 {
                     "op": "node",
                     "data": "node1"
                 },
                 {
                     "op": "negation",
                     "data": "node2"
                 },
             ]}
    create_graph(graph_dict)
