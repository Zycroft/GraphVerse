from .graph_generator.graph_generation import generate_interesting_graph
from .graph_generator.vertex_designation import designate_special_vertices
from .graph_generator.random_walks import random_walk
from .analysis import analyze_walks, analyze_llm_output
from .llm.training import train_llm
from .llm.inference import generate_sequence
from .main import run_simulation