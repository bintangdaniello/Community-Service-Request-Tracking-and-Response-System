from models.servicerequest import ServiceRequest

class EmergencyRequest(ServiceRequest):
    def __init__(self, request_id, request_type, requester_name, location, urgency_level, estimated_cost, status, hazard_level, response_time_minutes):
        super().__init__(request_id, request_type, requester_name, location, urgency_level, estimated_cost, status)
        self.hazard_level = hazard_level
        self.response_time_minutes = response_time_minutes

    def show_info(self):
        super().show_info()
        print("| Hazard Level: %-15d | Response Time: %d minutes" % (self.hazard_level, self.response_time_minutes))

