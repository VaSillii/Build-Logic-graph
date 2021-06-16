from owlready2 import *
from pathlib import Path

# onto_path.append(Path(__file__))
path_ontology = Path(__file__).absolute().joinpath('File/pizza.owl')

onto = get_ontology("/Users/vk/Desktop/buildGraph/File/pizza.owl").load()
data = list(onto.general_axioms())

with open('axiom.txt', 'w') as f:
    for ax in data:
        f.write(str(ax) + "\n")

# print([el for el in onto.classes()])
# print(list(onto.Pizza.subclasses()))