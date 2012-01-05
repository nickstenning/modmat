import networkx as nx

__all__ = ['sccs_in_array']

def sccs_in_array(ary):
    g = nx.DiGraph()

    for i, j in zip(*ary.nonzero()):
        g.add_edge(i, j)

    return nx.strongly_connected_components(g)
