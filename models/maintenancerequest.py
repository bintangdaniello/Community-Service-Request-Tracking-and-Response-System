# Defines the MaintenanceRequest class for infrastructure and facility repair requests

from models.servicerequest import ServiceRequest

class MaintenanceRequest(ServiceRequest):
    """
    Child Class (MaintenanceRequest), inherits from ServiceRequest.
    Extends ServiceRequest with fields specific to facility issues.

    Additional Attributes:
        issue_type : str        | Short description of the problem (e.g. 'Broken Pipe')
        days_open : int         | Number of days the issue has been unresolved
    """
    def __init__(self, request_id, request_type, requester_name, location, urgency_level, estimated_cost, status, issue_type, days_open):
        super().__init__(request_id, request_type, requester_name, location, urgency_level, estimated_cost, status)
        self.issue_type = issue_type
        self.days_open = days_open

    # Print a formatted summary including maintenance-specific fields
    def show_info(self):
        super().show_info()
        print("| Issue Type  : %-15s | Days Open    : %-3d" % (self.issue_type, self.days_open))