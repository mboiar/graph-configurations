"""
Module provides functionality for simplifying 
undirected graphs for the purpose of counting
directional configurations. 

Requirements: NetworkX 2.5
"""

from json.decoder import JSONDecodeError
import networkx as nx, sys, json

class Graph:
    def __init__(self, edges=[], count=1):
        self.edges = edges
        self.nodes = []
        for e in edges:
            if e[0]<=0 or e[1]<=0:
                raise ValueError('Only non-negative indices are valid.')
            if not (e[0] in self.nodes):
                self.nodes.append(e[0])
            if not (e[1] in self.nodes):
                self.nodes.append(e[1])
        self.count = count

    def __repr__(self):
        return f"Nodes: {str(self.nodes)}\n Edges: {str(self.edges)}\n Count: {self.count}."

    def remove_node(self,n):
        """
        Removes node n and every corresponding edge in a graph.
        """
        self.nodes.remove(n)
        edges = self.edges.copy()
        for e in edges:
            if n in e:
                self.edges.remove(e)

    def node_to_edge(self,n):
        """
        Removes node n and corresponding edges, adds edge 
        between neighbours of n.
        """
        self.nodes.remove(n)
        nei = []
        edges = self.edges.copy()
        for e in edges:
            if n in e:
                self.edges.remove(e)
                if not (e[0] == e[1]):
                    nei.append(e[not e.index(n)])
        self.edges.append(nei)

    def list_nei(self,n):
        """
        Returns a list of neighbours of a node n.
        """
        c = []
        for e in self.edges:
            if n in e:
                c.append(e[not e.index(n)])
        return c

    def all_nei(self):
        """
        Returns a list of neighbours of every node.
        """
        nei = []
        for n in self.nodes:
            nei.append([self.list_nei(n)])
        return nei

def iso_check(g1:Graph, g2:Graph) -> bool:
    """
    Performs an isomorphism check on two given Graph instances.
    Relies on NetworkX's 'is_isomorphic' function.
    """
    # minimal requirements for the isomorphic relation
    if (len(g1.nodes) == len(g2.nodes)) and (len(g1.edges)==len(g2.edges)) and (sorted([len(g1.list_nei(n)) for n in g1.nodes])==sorted([len(g2.list_nei(n)) for n in g2.nodes])): 
            ff = nx.MultiGraph()
            ff.add_nodes_from(g1.nodes)
            ff.add_edges_from(g1.edges)
            fg = nx.MultiGraph()
            fg.add_nodes_from(g2.nodes)
            fg.add_edges_from(g2.edges)
            if nx.is_isomorphic(ff,fg):
                return True 
    return False

def add_graph_to_list(g:Graph, lst:list, add_iso=False) -> None:
    """
    Adds a Graph instance to a list. If 'add_iso' parameter is True,
    instead increases count of corresponding isomorphic graph (if exists).
    """
    if add_iso:
        for p in lst:
            if iso_check(g, p):
                p.count+=g.count
                return   
    lst.append(g)

def simplify(g:Graph) -> tuple:
    """
    Performs a single iteration of simplification
    of Graph instance according to a set or rules.

    Returns: tuple: list of Graph instances and 
    boolean: whether the graph was successfully simplified
    """
    choices = {(1,1):4,(2,2):4,(0,0):6,(1,0):3,(2,1):2}
    m = False # True if graph was modified
    nodes = g.nodes.copy()
    for n in nodes:
        nei = g.list_nei(n)
        c = len(nei)
        l = nei.count(n)
        if (c,l) in choices.keys():
            g.count *= choices[(c,l)]
            g.remove_node(n)
            m = True
        elif c==3 and l==1:
            g.node_to_edge(n)
            m = True

    nodes = g.nodes.copy()
    for n in nodes:
        nei = g.list_nei(n)
        c = len(nei)
        l = nei.count(n)
        if c == 2 and l == 0:
            g1 = Graph(g.edges.copy(), g.count)
            g1.nodes = nodes.copy()
            g2 = Graph(g.edges.copy(), g.count)
            g2.nodes = nodes.copy()
            g1.remove_node(n)
            g2.node_to_edge(n)
            return ([g1,g2], True)
    return ([g],m)

def convert_irreducible(lst:list, irr:dict) -> list:
    """
    Converts Graph instances that could not be simplified
    according to their specified value.
    """
    m = False
    count = 1
    if not irr:
        return lst
    for g in lst:
        for p in irr:
            if iso_check(g,p):
                count *= p.count * g.count
                lst.remove(g)
                m = True
                break
    if m:
        add_graph_to_list(Graph([],count=count),lst, add_iso=True)
    return lst

def main(init:list) -> list:
    """
    Performs full simplification of a given graph, returning list
    of irreducible Graph instances.
    
    Somewhat artificial method for making use of isomorphic graphs:
    by restricting simplification to higher-order graphs, graphs will be more likely to be of the same order (and potentially isomorphic).
    """
    ig = Graph(init)
    queue = [ig]
    final = []
    k = None
    while queue:
        dimensions = [len(g.nodes) for g in queue]
        k = min(dimensions) if len(set(dimensions))>1 else None
        for g in queue:
            if not k or len(g.nodes)>k:
                queue.remove(g)
                graph_list, success = simplify(g)
                if not success:
                    add_graph_to_list(graph_list[0],final, True)
                else:
                    for gr in graph_list:
                        add_graph_to_list(gr, queue, True)
    return final

if __name__ == "__main__":

    #dict with irreducible graphs and their values
    irr = [Graph([[1,2],[2,3],[3,1],[1,4],[2,4],[3,4]], count=24),
           Graph([[1,2],[1,2],[1,2]], count=6)]

    #set True to simplify output with values from 'irr'
    convert_irr = False

    init_str = input("Enter edge list of a graph:")
    try:
        init = json.loads(init_str)
    except JSONDecodeError:
        sys.exit("Invalid input value.")
    
    lst = convert_irreducible(main(init), irr) if convert_irr else main(init)

    #result in canonical form
    final = [[g.count,g.edges] for g in lst]
    print(final)