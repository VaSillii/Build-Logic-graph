import os
from dotenv import load_dotenv


def get_path_graphviz():
    return str(os.environ.get('PATH_GRAPHVIZ'))