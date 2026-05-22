class ServiceRequest:
    def __init__(self, request_id, request_type, requester_name, location, urgency_level, estimated_cost, status):
        self.request_id = request_id
        self.request_type = request_type
        self.requester_name = requester_name
        self.location = location
        self.urgency_level = urgency_level
        self.estimated_cost = estimated_cost
        self.status = status

    def show_info(self):
        print("     %-6s | %-13s | %-30s | %-20s | %-3d | $%-8.2f | %-12s " % (self.request_id, self.request_type, self.requester_name,
                                                     self.location, self.urgency_level, self.estimated_cost, self.status), end=" ")