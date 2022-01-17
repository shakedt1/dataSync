from time import sleep

import node_manager

if __name__ == "__main__":
    node_manager.add_node([])
    node_manager.add_node([0])
    node_manager.add_node([0, 1])

    sleep(5)

    node_manager.remove_node(0)

    sleep(1)
    node_manager.add_node([1])
