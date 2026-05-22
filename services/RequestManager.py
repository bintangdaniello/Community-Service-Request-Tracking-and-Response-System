"""
Service layer that manages the lifecycle of all service requests.

Acts as the intermediary between the GUI (presentation layer) and the
database (data layer), keeping an in-memory list in sync with persistent
storage at all times.
"""

from data.db_handler import init_db, read_db, insert_request, delete_request

class RequestManager:
    """
    Manages CRUD operations for service requests.

    Maintains an in-memory list of request objects that mirrors the SQLite
    database, so the GUI can read data without repeated database queries.

    Attributes:
        requests : list In-memory list of ServiceRequest (and subclass) objects
    """

    # Initialize the database and load existing records into memory
    def __init__(self):
        self.requests = []
        init_db()
        self.load_data()

    # Populate the in-memory list from the database on startup
    def load_data(self):
        self.requests = read_db()

    # Add a new request to both the in-memory list and the database
    def add_request(self, request):
        self.requests.append(request)
        insert_request(request)

    # Return all service requests currently held in memory
    def get_all_requests(self):
        return self.requests

    # Find a single request by its unique ID (case-insensitive)
    def search_by_id(self, user_request_id):
        for i in self.requests:
            if i.request_id.upper() == user_request_id.upper():
                return i
        return None

    # Return all requests that match a given type (case-insensitive)
    def search_by_type(self, user_request_type):
        filter_type = []
        for i in self.requests:
            if i.request_type.lower() == user_request_type.lower():
                filter_type.append(i)
        return filter_type

    # Return all requests that match a given status (case-insensitive)
    def search_by_status(self, user_request_status):
        filter_status = []
        for i in self.requests:
            if i.status.lower() == user_request_status.lower():
                filter_status.append(i)
        return filter_status

    # Remove a request from memory and the database by ID (case-insensitive)
    def delete_request(self, user_request_id):
        for i in self.requests:
            if i.request_id.upper() == user_request_id.upper():
                self.requests.remove(i)
                delete_request(user_request_id)
                return
        return None