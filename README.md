# Build Logic Graph

Ontology visualization service based on the Logic Graphs method.
 
1. Create virtual [environment](https://virtualenv.pypa.io/en/latest/) with python v3.8.
2. Clone this repositories.
4. Make file `.env` in project root based on `.env.example` and specify settings. Specify the path to graphviz.
5. install requirements: `pip install -r requirements.txt`.
6. Add ontology in `File\` if it is necessary.
7. Fix path to ontology or her name in variable 'path' in `main.py` 
8. Run program `python main.py`