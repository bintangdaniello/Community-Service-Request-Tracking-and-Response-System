# Defines the EmergencyRequest class for urgent or hazard related service requests.

from models.servicerequest import ServiceRequest

class EmergencyRequest(ServiceRequest):
    """
    Child Class (EmergencyRequest), inherits from ServiceRequest.
    Extends ServiceRequest with fields specific to hazardous situations.

    Additional Attributes:
        hazard_level : int              | Severity of the hazard
        response_time_minutes : int     | Required response time in minutes
    """
    def __init__(self, request_id, request_type, requester_name, location, urgency_level, estimated_cost, status, hazard_level, response_time_minutes):
        super().__init__(request_id, request_type, requester_name, location, urgency_level, estimated_cost, status)
        self.hazard_level = hazard_level
        self.response_time_minutes = response_time_minutes

    # Print a formatted summary including emergency-specific fields
    def show_info(self):
        super().show_info()
        print("| Hazard Level: %-15d | Response Time: %d minutes" % (self.hazard_level, self.response_time_minutes))
