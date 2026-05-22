from models.maintenancerequest import MaintenanceRequest
from models.eventrequest import EventRequest
from models.emergencyrequest import EmergencyRequest

def recommendation_request(user_request_type):
    if isinstance(user_request_type, MaintenanceRequest):
        if user_request_type.days_open > 14:
            return "     Urgent! Need repair immediately!"
        elif user_request_type.days_open > 7:
            return "     Medium, Please schedule repair"
        elif user_request_type.days_open <= 7:
            return "     Low, Add to maintenance queue"
    elif isinstance(user_request_type, EventRequest):
        if user_request_type.attendees >= 500:
            return "     Crowded, please direct a full support team"
        elif user_request_type.attendees >= 250:
            return "     Semi-Crowded, partial event support is a minimum"
        elif user_request_type.attendees < 250:
            return "     Quiet, low team support is a minimum"
    elif isinstance(user_request_type, EmergencyRequest):
        if user_request_type.hazard_level >= 5:
            return "     Critical! Please respond to the emergency immediately!"
        elif user_request_type.hazard_level >= 4:
            return "     Moderate, Please respond within 30 minutes"
        elif user_request_type.hazard_level < 4:
            return "     Marginal, Please respond within 24 hours"

def prioritize_requests(user_requests):
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