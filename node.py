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
        self.current_neighbors = None
        self.node_id = node_id
        self.neighbors = neighbors
        self.database = Database()
        self.log_state = dict((node, 0) for node in node_manager.nodes.keys())
        self.buffer = str()
        # self.daemon = True
        self.stop = False
        self.events = [threading.Event() for _ in range(4)]
        self.timeout = random.randint(3, 10)

    def publish_log_to_neighbors(self):
        node_manager.publish(self.current_neighbors, self.build_msg(self.log_state))
        print("id: {} publish {} to {}".format(self.node_id, self.build_msg(self.log_state), self.current_neighbors))

    def send_log_diffs(self):
        eval_buffer = ast.literal_eval(self.buffer[:-1])
        manager_id = eval_buffer[0]
        # print("id: {} received publish {} from {}".format(self.node_id, eval_buffer[1], eval_buffer[0]))
        diff = {id: self.log_state[id] for id in self.log_state if self.log_state[id] != eval_buffer[1][str(id)]}
        node_manager.send(manager_id, self.build_msg(diff), 1)
        # print("id: {} send log diffs {} to {}".format(self.node_id, self.build_msg(diff), manager_id))
        return manager_id

    def send_data_request(self):
        neighbors_log_state = ast.literal_eval(self.buffer)
        # print("id: {} received log diffs {}".format(self.node_id, neighbors_log_state))

        requests = dict()
        lowest_states = dict(self.log_state)
        highest_states = dict(self.log_state)

        self.current_neighbors = list()
        for neighbor_log_state in neighbors_log_state:
            if neighbor_log_state[1]:
                self.current_neighbors.append(neighbor_log_state[0])
            for state in neighbor_log_state[1]:
                int_state = int(state)
                if neighbor_log_state[1][state] > highest_states[int_state]:
                    highest_states[int_state] = neighbor_log_state[1][state]
                    requests[int_state] = neighbor_log_state[0]
                elif neighbor_log_state[1][state] < lowest_states[int_state]:
                    lowest_states[int_state] = neighbor_log_state[1][state]

        fixed_requests = dict()
        for request in requests.keys():
            fixed_requests.setdefault(requests[request], []).append(request)

        # print(requests)

        for sender_id in fixed_requests:
            data_request = {state_index: self.log_state[state_index] for state_index in fixed_requests[sender_id]}
            node_manager.send(sender_id, json.dumps(data_request), 1)
            # print("id: {} send data request {} to {}".format(self.node_id, json.dumps(data_request), sender_id))
        node_manager.multy_send(self.current_neighbors, "", 1)

        # print(lowest_states)
        return bool(requests), lowest_states

    def send_data_reply(self, manager_id):
        eval_buffer = ast.literal_eval(self.buffer)
        # print("id: {} received data request {}".format(self.node_id, eval_buffer))
        db_data = dict()
        for state in eval_buffer:
            db_data[state] = self.database.get_data(int(state), eval_buffer[state], self.log_state[int(state)])
        node_manager.send(manager_id, json.dumps(db_data) + ',', 2)
        # print("id: {} send data reply {} to {}".format(self.node_id, json.dumps(db_data), manager_id))

    def sync_data(self):
        eval_buffer = ast.literal_eval(self.buffer)
        # print("id: {} received data reply {}".format(self.node_id, eval_buffer))
        for data_dict in eval_buffer:
            for data_id in data_dict:
                self.log_state[int(data_id)] += len(data_dict[data_id])
                self.database.sync_data(int(data_id), data_dict[data_id])


    def publish_data_to_neighbors(self, lowest_states):
        db_data = dict()
        for state in self.log_state:
            if self.log_state[state] > lowest_states[state]:
                db_data[state] = (self.log_state[state], self.database.get_data(state, lowest_states[state], self.log_state[state]))
        node_manager.multy_send(self.current_neighbors, json.dumps(db_data), 2)
        # print("id: {} publish data to neighbors {} to {}".format(self.node_id, json.dumps(db_data), self.current_neighbors))

    def sync_all_data(self):
        data_dict = ast.literal_eval(self.buffer)
        # print("id: {} received data from manager {}".format(self.node_id, data_dict))
        for data_id in data_dict:
            missing_length = data_dict[data_id][0] - self.log_state[int(data_id)]
            if missing_length != 0:
                self.log_state[int(data_id)] += missing_length
                self.database.sync_data(int(data_id), data_dict[data_id][1][-missing_length:])
        print("id: {} new log_state: {}".format(self.node_id, self.log_state))


    def send_sync_complete(self, manager_id):
        node_manager.send(manager_id, str(self.node_id) + ",", 3)
        # print("id: {} send sync complete {} to {}".format(self.node_id, self.node_id, manager_id))

    def publish_synchronized_nodes(self):
        node_manager.multy_send(self.current_neighbors, self.buffer + str(self.node_id), 3)
        # print("id: {} send synchronized_nodes {} to {}".format(self.node_id, self.buffer + str(self.node_id), self.current_neighbors))

    def run(self):
        print("id: {} neighbors: {} log_state: {}".format(self.node_id, self.neighbors, self.log_state))
        while not self.stop:
            self.current_neighbors = self.neighbors
            sync = False
            self.events[0].wait(timeout=self.timeout)
            [event.clear() for event in self.events[1:]]

            if self.events[0].is_set():
                manager_id = self.send_log_diffs()
                self.buffer = ""

                self.events[1].wait(timeout=2)
                if self.events[1].is_set():
                    if self.buffer:
                        self.send_data_reply(manager_id)
                    self.buffer = ""

                    self.events[2].wait(timeout=2)
                    if self.events[2].is_set():
                        self.sync_all_data()
                        self.send_sync_complete(manager_id)
                        self.buffer = ""

                        self.events[3].wait(timeout=4)
                        if self.events[3].is_set():
                            synchronized_nodes = list(map(int, self.buffer.split(',')))
                            print("synced:" + str(synchronized_nodes))
                            self.current_neighbors = list(set(self.neighbors) - set(synchronized_nodes))
                            sync = bool(self.current_neighbors)
                            [event.clear() for event in self.events[1:]]
                            self.buffer = ""
            else:
                sync = True

            if sync:
                self.events[0].set()
                self.publish_log_to_neighbors()

                self.events[1].wait(timeout=2)
                if self.events[1].is_set():
                    sleep(1)
                    has_requests, lowest_states = self.send_data_request()

                    if len(self.current_neighbors) != 0:
                        self.buffer = ""
                        if has_requests:
                            self.events[2].wait(timeout=2)
                            if self.events[2].is_set():
                                sleep(1)
                                self.sync_data()
                        else:
                            sleep(1)
                        print("id: {} new log_state {}".format(self.node_id, self.log_state))

                        self.publish_data_to_neighbors(lowest_states)
                        self.buffer = ""

                        self.events[3].wait(timeout=4)
                        if self.events[3].is_set():
                            sleep(1)
                            self.publish_synchronized_nodes()

            self.buffer = ""
            self.timeout = random.randint(5, 10)
            self.events[0].clear()

    def stop_node(self):
        self.stop = True

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def remove_neighbor(self, neighbor):
        self.neighbors.remove(neighbor)

    def add_to_database(self, data):
        if not self.is_syncing():
            self.database.add_data(self.node_id, data)
            self.log_state[self.node_id] += 1
            print(data + " added to " + str(self.node_id))

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
