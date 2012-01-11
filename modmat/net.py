import tempfile
import networkx as nx

__all__ = ['sccs_in_array']

def array_to_graph(ary):
    g = nx.DiGraph()

    for i, j in zip(*ary.nonzero()):
        g.add_edge(i, j, weight=ary[i,j])

    return g

def array_to_dot(ary):
    g = array_to_graph(ary)
    g.name = 'G'

    with tempfile.TemporaryFile() as tf:
        nx.write_dot(g, tf)
        tf.seek(0)
        return tf.read()

def sccs_in_array(ary):
    g = array_to_graph(ary)

    return nx.strongly_connected_components(g)
