# Business logic for generating actionable recommendations and prioritizing
# service requests based on their type-specific attributes

from models.maintenancerequest import MaintenanceRequest
from models.eventrequest import EventRequest
from models.emergencyrequest import EmergencyRequest

def recommendation_request(user_request_type):
    """
    Generate a recommendation for a single service request.

    The recommendation is determined by type-specific thresholds:
    - MaintenanceRequest : based on how many days the issue has been open
    - EventRequest       : based on the expected number of attendees
    - EmergencyRequest   : based on the hazard severity level

    :parameter user_request_type : ServiceRequest (A MaintenanceRequest, EventRequest, or EmergencyRequest instance)
    :returns : str | None (A formatted recommendation string, or None if the type is unrecognised)
    """
    if isinstance(user_request_type, MaintenanceRequest):
        if user_request_type.days_open > 14:
            return "     Urgent!. This issue has been open too long. Immediate repair is required!"
        elif user_request_type.days_open > 7:
            return "     Moderate. Please schedule a repair as soon as possible"
        elif user_request_type.days_open <= 7:
            return "     Low. Add this to the maintenance queue for routine handling"
    elif isinstance(user_request_type, EventRequest):
        if user_request_type.attendees >= 500:
            return "     Large Event!. A full support team must be deployed immediately"
        elif user_request_type.attendees >= 250:
            return "     Medium Event. Partial event support is required at minimum"
        elif user_request_type.attendees < 250:
            return "     Small Event. Minimal team support is sufficient"
    elif isinstance(user_request_type, EmergencyRequest):
        if user_request_type.hazard_level >= 5:
            return "     Critical!. Respond immediately without any delay!"
        elif user_request_type.hazard_level >= 4:
            return "     High!. Please respond within 30 minutes."
        elif user_request_type.hazard_level < 4:
            return "     Low. Response within 24 hours is acceptable."

def prioritize_requests(user_requests):
    """
    Sort a list of service requests in descending order of urgency level (5 → 1)

    :parameter user_requests : List of ServiceRequest (or subclass) objects
    :return : List (sorted from highest to lowest urgency_level)
    """
    five = []
    four = []
    three = []
    two = []
    one = []

    for i in user_requests:
        if i.urgency_level == 5:
            five.append(i)
        elif i.urgency_level == 4:
            four.append(i)
        elif i.urgency_level == 3:
            three.append(i)
        elif i.urgency_level == 2:
            two.append(i)
        elif i.urgency_level == 1:
            one.append(i)

    sorted_version = []
    sorted_version.extend(five)
    sorted_version.extend(four)
    sorted_version.extend(three)
    sorted_version.extend(two)
    sorted_version.extend(one)

    return sorted_version