import threading
from threading import Thread
import random
from time import sleep

import node_manager
from database import Database
import json
import ast


class Node(Thread):
    def __init__(self, node_id, neighbors):
        super(Node, self).__init__()
        self.node_id = node_id
        self.neighbors = neighbors
        self.database = Database()
        self.log_state = dict((node, 0) for node in node_manager.nodes.keys())
        self.buffer = str()
        # self.daemon = True
        self.stop = False
        self.events = [threading.Event() for i in range(5)]
        self.timeout = random.randint(3, 10)

    def publish_log_to_neighbors(self):
        node_manager.multy_send(self.neighbors, self.build_msg(self.log_state), 0)

    def send_log_diffs(self):
        split_buffer = ast.literal_eval(self.buffer[:-1])
        print("id: {} received {} from {}".format(self.node_id, split_buffer[1], split_buffer[0]))
        diff = {id: self.log_state[id] for id in self.log_state if self.log_state[id] != split_buffer[1][str(id)]}
        node_manager.send(split_buffer[0], self.build_msg(diff), 1)

    def send_data_request(self):
        all_log_states = ast.literal_eval(self.buffer)
        print("id: {} received {}".format(self.node_id, all_log_states))

    def send_data_reply(self):
        pass

    def publish_data_to_neighbors(self):
        pass

    def send_sync_complete(self):
        pass

    def publish_synchronized_nodes(self):
        pass

    def run(self):
        print("id: {} neighbors: {} log_state: {}".format(self.node_id, self.neighbors, self.log_state))
        while not self.stop:
            self.events[0].wait(timeout=self.timeout)

            if self.buffer:
                self.send_log_diffs()
                self.events[2].wait()
            else:
                self.publish_log_to_neighbors()
                self.events[1].wait()
                sleep(2)
                self.send_data_request()

            self.buffer = ""
            self.timeout = random.randint(3, 10)
            [event.clear() for event in self.events]

    def stop_node(self):
        self.stop = True

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def remove_neighbor(self, neighbor):
        self.neighbors.remove(neighbor)

    def add_to_database(self, data):
        self.database.add_data(self.node_id, data)
        self.log_state[self.node_id] += 1

    def add_state(self, neighbor):
        self.log_state[neighbor] = 0

    def remove_state(self, neighbor):
        del self.log_state[neighbor]

    def add_to_buffer(self, data):
        self.buffer += data

    def set_event(self, index):
        self.events[index].set()

    def is_syncing(self):
        return self.events[0].is_set()

    def build_msg(self, data):
        return "({}, {}),".format(self.node_id, json.dumps(data))
