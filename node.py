from database import Database


class Node:
    def __init__(self, id, neighbors):
        self.id = id
        self.is_syncing = False
        self.neighbors = neighbors
        self.database = Database()
        self.log_state = list()

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
