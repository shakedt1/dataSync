from time import sleep
import networkx as nx
from pyvis.network import Network

import node_manager

if __name__ == "__main__":

    node_manager.add_node([])
    node_manager.add_node([0])
    node_manager.add_node([0, 1])
    # node_manager.add_node([0, 1, 2])
    node_manager.add_node([0])
    # node_manager.add_node([4])
    node_manager.nodes[0].add_to_database("hello")
    node_manager.nodes[1].add_to_database("hello")
    node_manager.nodes[1].add_to_database("yello")
    # node_manager.nodes[2].add_to_database("hello")
    node_manager.nodes[0].add_to_database("yello")
    node_manager.nodes[3].add_to_database("hello")
    # sleep()
    while True:
        inp = input()
        if inp:
            if inp == 'r':
                r_inp = input()
                if r_inp:
                    if int(r_inp) in node_manager.nodes:
                        node_manager.remove_node(int(r_inp))
            elif inp == 'a':
                a_inp = input()
                if a_inp:
                    node_manager.add_node(list(map(int, list(a_inp))))
            elif int(inp) in node_manager.nodes:
                node_manager.nodes[int(inp)].add_to_database(inp + "ello")
    # G = nx.Graph()
    # edges = list()
    # for id, node in node_manager.nodes.items():
    #     edges.extend([id, neighbor] for neighbor in node.neighbors)
    # G.add_edges_from(edges)
    # net = Network(notebook=True)
    # net.from_nx(G)
    # net.show("network.html")
