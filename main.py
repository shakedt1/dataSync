from time import sleep

import node_manager

if __name__ == "__main__":
    node_manager.add_node([])
    node_manager.add_node([0])
    node_manager.add_node([0, 1])
    # node_manager.add_node([0, 1, 2])
    node_manager.add_node([0])
    # node_manager.add_node([4])
    node_manager.nodes[0].add_to_database("hello")
    # sleep()
