from data.file_handler import read_csv, write_csv

CSV = "service_requests.csv"

class RequestManager:
    def __init__(self):
        self.requests = []
        self.load_data()

    def load_data(self):
        self.requests = read_csv(CSV)

    def save_data(self):
        write_csv(CSV, self.requests)

    def add_request(self, request):
        self.requests.append(request)
        self.save_data()

    def get_all_requests(self):
        return self.requests

    def search_by_id(self, user_request_id):
        for i in self.requests:
            if i.request_id.upper() == user_request_id.upper():
                return i
        return None

    def search_by_type(self, user_request_type):
        filter_type = []
        for i in self.requests:
            if i.request_type.lower() == user_request_type.lower():
                filter_type.append(i)
        return filter_type

    def search_by_status(self, user_request_status):
        filter_status = []
        for i in self.requests:
            if i.status.lower() == user_request_status.lower():
                filter_status.append(i)
        return filter_status

    def delete_request(self, user_request_id):
        for i in self.requests:
            if i.request_id.upper() == user_request_id.upper():
                self.requests.remove(i)
                self.save_data()
                return
        return None