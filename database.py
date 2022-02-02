

class Database:
    def __init__(self):
        self.data = dict()

    def get_data(self, node_id, start_index, end_index):
        return self.data[node_id][start_index:end_index]

    def add_data(self, node_id, data):
        self.data.setdefault(node_id, []).extend(data)
