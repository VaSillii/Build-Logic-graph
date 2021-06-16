from datetime import datetime
from pathlib import Path
from graphviz import Digraph, Source


class BuildGraph(object):
    def __init__(self, graph: dict):
        """Constructor"""
        self.graph = graph
        self.NODE_NUMBER = 0


    def node_elm(self, node: str, color: str = 'white'):
        self.NODE_NUMBER += 1
        cluster_name = 'cluster_' + str(self.NODE_NUMBER)
        node_name = 'node' + str(self.NODE_NUMBER)
        graph = f'\nsubgraph {cluster_name} ' + "{\n" + \
                f'\tnode[shape=record, width=0.5, style=filled, fillcolor={color}];\n\t' + \
                'color=black;\n\t' + \
                node_name + f'[label=\"{node}\"]' \
                         '; \n}'
        return {'cluster_name': cluster_name, 'node': node, 'graph': graph}


    def save_to_dot_file(self, path: str, graph: str):
        """
        Save to .dot file
        :param path: Path to file
        :param graph: Description graph
        :return:
        """
        with open(path, 'w') as f:
            f.write(graph)

    def wrap_diagram(self, graph: str):
        """
        Function wrap graph in diagram block
        :param graph:
        :return: Wrapping a graph in block diagrams
        """
        graph = 'digraph diagram_1 { \n' + \
                '\tgraph [fontsize=10 fontname="Verdana" compound=true];\n' + \
                'color=white;' + \
                graph + \
                '\n}'
                # '\tnode [shape=record fontsize=10 fontname="Verdana"];\n' + \
        return graph

    def get_graph(self, graph_dict: dict):
        """
        Function get graph in dot format
        :param graph_dict: Graph description dictionary
        :return: Graph in dot format
        """
        data_graph = {'graph': '', 'nodes': [], 'clusters':[]}
        if graph_dict['op'] == 'name':
            data_graph['graph'] += graph_dict['data']
        elif graph_dict['op'] == 'node':
            data_node = self.node_elm(graph_dict['data'])
            print(data_node)
            data_graph['graph'] += data_node['graph']
            data_graph['nodes'].append(data_node['node'])
            data_graph['clusters'].append(data_node['cluster_name'])
        return data_graph

    def create_graph(self):
        """
        Function create graph
        :param desc_dict: Description dictionary graph
        :return: Graph in dot format
        """
        data_graph = self.get_graph(self.graph)
        # path = f'File/dot_files/{str(datetime.now())}.dot'
        path = f'File/dot_files/test2.dot'
        # self.save_to_dot_file(path, self.wrap_diagram(data_graph['graph']))
        s = Source.from_file(path)
        s.view()



if __name__ == '__main__':
    graph_dict = {
        # "op": "node",
        # "data": "Domain"
        "op": "",
        "data": [
            {
                "op": "node",
                "data": "Жанр"
            },
            {
                "op": "node",
                "data": "Domain1asd"
            }
        ]
    }
    BuildGraph(graph_dict).create_graph()