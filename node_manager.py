from node import Node

nodes = dict()
last_id = 0


def add_node(neighbors):
    global last_id

    for neighbor in neighbors:
        if neighbor not in nodes:
            print("No such neighbors")
            return
        nodes[neighbor].add_neighbor(last_id)

    node = Node(last_id, neighbors)
    nodes[last_id] = node
    node.start()
    last_id += 1


def remove_node(id):
    [node.remove_neighbor(id) for node in nodes.values() if id in node.neighbors]
    nodes[id].stop_node()
    del nodes[id]


def send(id):
    pass


def multy_send(ids):
    pass
