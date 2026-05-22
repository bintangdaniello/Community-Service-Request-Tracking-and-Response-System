# Defines the base ServiceRequest class used across all request types.
# All specific request types (Maintenance, Event, Emergency) inherit from this class to share common attributes and behaviour

class ServiceRequest:
    """
    Base Class (ServiceRequest)

    Attributes:
        request_id : str        | Unique ID for the request
        request_type : str      | Type of the request ('Maintenance', 'EventSupport', 'Emergency')
        requester_name : str    | Name of the requester (the person who submitted the request)
        location : str          | Location associated with the request
        urgency_level : int     | Priority level on a scale of 1 (low) to 5 (critical/high)
        estimated_cost : float  | Estimated cost in USD
        status : str            | Current status: 'Open', 'In Progress', 'Closed'
    """
    def __init__(self, request_id, request_type, requester_name, location, urgency_level, estimated_cost, status):
        self.request_id = request_id
        self.request_type = request_type
        self.requester_name = requester_name
        self.location = location
        self.urgency_level = urgency_level
        self.estimated_cost = estimated_cost
        self.status = status

    # Print a formatted single-line summary of this request
    def show_info(self):
        print("     %-6s | %-13s | %-30s | %-20s | %-3d | $%-8.2f | %-12s " % (self.request_id, self.request_type, self.requester_name,
                                                     self.location, self.urgency_level, self.estimated_cost, self.status), end=" ")