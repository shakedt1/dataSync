from node import Node

nodes = dict()
last_node_id = 0


def add_node(neighbors):
    global last_node_id

    if not set(neighbors).issubset(nodes.keys()):
        print("No such neighbors")
        return

    [nodes[neighbor].add_neighbor(last_node_id) for neighbor in neighbors]

    [node.add_state(last_node_id) for node in nodes.values()]

    nodes[last_node_id] = 0
    node = Node(last_node_id, neighbors)
    nodes[last_node_id] = node
    node.start()
    last_node_id += 1


def remove_node(node_id):
    if node_id not in nodes:
        print("No such node")
        return

    [node.remove_neighbor(node_id) for node in nodes.values() if node_id in node.neighbors]
    [node.remove_state(node_id) for node in nodes.values()]

    nodes[node_id].stop_node()
    del nodes[node_id]


def send(node_id, data, event):
    if not nodes[node_id].is_syncing() or not event:
        nodes[node_id].add_to_buffer(data)
        nodes[node_id].set_event(event)


def multy_send(node_ids, data, event):
    [send(node_id, data, event) for node_id in node_ids]

