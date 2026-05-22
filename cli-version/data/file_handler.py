from models.maintenancerequest import MaintenanceRequest
from models.eventrequest import EventRequest
from models.emergencyrequest import EmergencyRequest

CSV_FILE = "service_requests.csv"

def read_csv(CSV_FILE):
    list_of_object = []
    try:
        with open(CSV_FILE, "r") as inFile:
            data = inFile.readlines()
            if len(data) <= 1:
                return []

            for line in data[1:]:
                split_line = line.strip().split(",")

                request_id, request_type, requester_name, location, urgency_level, estimated_cost, status, issue_type, days_open, attendees, event_date, hazard_level, response_time_minutes = split_line

                if request_type.lower() == "maintenance":
                    obj = MaintenanceRequest(request_id, request_type, requester_name, location, int(urgency_level), float(estimated_cost), status, issue_type, int(days_open))
                    list_of_object.append(obj)
                elif request_type.lower() == "eventsupport":
                    obj = EventRequest(request_id, request_type, requester_name, location, int(urgency_level), float(estimated_cost), status, int(attendees), event_date)
                    list_of_object.append(obj)
                elif request_type.lower() == "emergency":
                    obj = EmergencyRequest(request_id, request_type, requester_name, location, int(urgency_level), float(estimated_cost), status, int(hazard_level), int(response_time_minutes))
                    list_of_object.append(obj)
    except FileNotFoundError as e:
        print("File not found!: %s" % str(e))
    return list_of_object

def write_csv(CSV, event_list):
    try:
        with open(CSV, "w") as outFile:
            outFile.write("request_id,request_type,requester_name,location,urgency_level,estimated_cost,status,issue_type,days_open,attendees,event_date,hazard_level,response_time_minutes\n")

            for i in event_list:
                if i.request_type.lower() == "maintenance":
                    outFile.write("%s,%s,%s,%s,%d,%.2f,%s,%s,%d,,,,\n" % (i.request_id, i.request_type, i.requester_name, i.location, i.urgency_level, i.estimated_cost, i.status, i.issue_type, i.days_open))
                elif i.request_type.lower() == "eventsupport":
                    outFile.write("%s,%s,%s,%s,%d,%.2f,%s,,,%d,%s,,\n" % (i.request_id, i.request_type, i.requester_name, i.location, i.urgency_level, i.estimated_cost, i.status, i.attendees, i.event_date))
                elif i.request_type.lower() == "emergency":
                    outFile.write("%s,%s,%s,%s,%d,%.2f,%s,,,,,%d,%d\n" % (i.request_id, i.request_type, i.requester_name, i.location, i.urgency_level, i.estimated_cost, i.status, i.hazard_level, i.response_time_minutes))
    except Exception as e:
        print("File cannot be saved!: %s" % str(e))