from threading import Thread
from time import sleep

import node_manager
from database import Database


class Node(Thread):
    def __init__(self, id, neighbors):
        super(Node, self).__init__()
        self.id = id
        self.is_syncing = False
        self.neighbors = neighbors
        self.database = Database()
        self.log_state = dict((node, 0) for node in node_manager.nodes.keys())
        self.buffer = str()
        self.daemon = True
        self.stop = False

    def publish_log_to_neighbors(self, manager_id, log_state):
        pass

    def send_log_diffs(self, node_id, manager_id, log_state):
        pass

    def send_data_request(self, manager_id, node_id, log_state):
        pass

    def send_data_reply(self, node_id, manager_id, data):
        pass

    def publish_data_to_neighbors(self, manager_id, log_state, data):
        pass

    def send_sync_complete(self, node_id, manager_id):
        pass

    def publish_synchronized_nodes(self, manager_id, nodes_id):
        pass

    def run(self):
        while not self.stop:
            print("id:" + str(self.id) + " neighbors:" + str(self.neighbors) + " log_state:" + str(self.log_state))
            sleep(3)

    def stop_node(self):
        self.stop = True

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def remove_neighbor(self, neighbor):
        self.neighbors.remove(neighbor)

    def add_to_database(self, data):
        self.database.add_data(id, data)
        self.log_state[id] += 1

    def add_state(self, neighbor):
        self.log_state[neighbor] = 0

    def remove_state(self, neighbor):
        del self.log_state[neighbor]
