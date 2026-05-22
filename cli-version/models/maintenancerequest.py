from models.servicerequest import ServiceRequest

class MaintenanceRequest(ServiceRequest):
    def __init__(self, request_id, request_type, requester_name, location, urgency_level, estimated_cost, status, issue_type, days_open):
        super().__init__(request_id, request_type, requester_name, location, urgency_level, estimated_cost, status)
        self.issue_type = issue_type
        self.days_open = days_open

    def show_info(self):
        super().show_info()
        print("| Issue Type  : %-15s | Days Open    : %-3d" % (self.issue_type, self.days_open))