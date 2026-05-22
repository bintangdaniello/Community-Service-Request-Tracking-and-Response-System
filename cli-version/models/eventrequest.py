from models.servicerequest import ServiceRequest

class EventRequest(ServiceRequest):
    def __init__(self, request_id, request_type, requester_name, location, urgency_level, estimated_cost, status, attendees, event_date):
        super().__init__(request_id, request_type, requester_name, location, urgency_level, estimated_cost, status)
        self.attendees = attendees
        self.event_date = event_date

    def show_info(self):
        super().show_info()
        print("| Attendees   : %-15d | Event Date   : %-3s" % (self.attendees, self.event_date))