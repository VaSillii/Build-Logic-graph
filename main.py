from pathlib import Path
from HelperClass.parse_onto import ParseOntology
from HelperClass.build_graph import BuildGraph
from configuration import get_path_graphviz

if __name__ == '__main__':
    get_path_graphviz()
    path = Path(__file__).absolute().parent.joinpath(r'File\family.owl')
    # path = Path(__file__).absolute().parent.joinpath(r'File\ontology family_1.owl')
    parse_onto = ParseOntology(path)
    parse_onto.parse()
    data = parse_onto.class_onto
    BuildGraph(data).create_graph()
    # print(data.class_onto[0].equivalent_class[0].elements[0].name)