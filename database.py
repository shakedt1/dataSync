

class Database:
    def __init__(self):
        self.data = dict()

    def get_data(self, start_index, end_index):
        pass

    def add_data(self, id, data):
        self.data.setdefault(id, []).append(data)

    def sync_data(self, data):
        pass