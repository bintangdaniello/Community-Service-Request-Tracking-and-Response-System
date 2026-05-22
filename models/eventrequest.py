# Defines the EventRequest class for community event support requests

from models.servicerequest import ServiceRequest

class EventRequest(ServiceRequest):
    """
    Child Class (EventRequest), inherits from ServiceRequest.
    Extends ServiceRequest with fields specific to event logistics.

    Additional Attributes:
        attendee : int         | Number of attendees at the event
        event_date : str       | Scheduled date of the event in 'YYYY-MM-DD' format
    """
    def __init__(self, request_id, request_type, requester_name, location, urgency_level, estimated_cost, status, attendees, event_date):
        super().__init__(request_id, request_type, requester_name, location, urgency_level, estimated_cost, status)
        self.attendees = attendees
        self.event_date = event_date

    # Print a formatted summary including event-specific fields
    def show_info(self):
        super().show_info()
        print("| Attendees   : %-15d | Event Date   : %-3s" % (self.attendees, self.event_date))