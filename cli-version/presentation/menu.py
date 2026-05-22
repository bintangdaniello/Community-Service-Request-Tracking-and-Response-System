from services.Recommendation import recommendation_request, prioritize_requests
from models.maintenancerequest import MaintenanceRequest
from models.eventrequest import EventRequest
from models.emergencyrequest import EmergencyRequest

def view_all(manager):
    requests = manager.get_all_requests()
    if len(requests) == 0:
        print("     Empty Request!")
    else:
        print("     %-6s | %-13s | %-30s | %-20s | %-3s | %-8s  | %-12s  | %-15s               | %-3s" % ("ID", "Type", "Name", "Location", "Urg", "Est Cost", "Status", "Detail 1", "Detail 2"))
        print("     ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        for i in requests:
            i.show_info()

def add_new_requests(manager):
    print("     Please choose one of the following request (1 / 2 / 3)")
    print("     1. Maintenance | 2. EventSupport | 3. Emergency")

    while True:
        user_input = input("     Enter request: ")
        if user_input.strip() != "1" and user_input.strip() != "2" and user_input.strip() != "3":
            print("     Please enter between 1-3!")
            continue
        else:
            break

    while True:
        user_request_id = input("     Enter request ID (3 Digit, e.g. 110): ")
        if user_request_id.strip().isdigit() and len(user_request_id) == 3:
            user_request_id = "SR" + user_request_id.strip()
            if manager.search_by_id(user_request_id.strip()) is not None:
                print("     ID already exist! Please use another number")
                continue
            break
        else:
            print("     Request ID must be 3 Digit")
            continue

    while True:
        requester_name = input("     Enter Requester Name: ")
        if requester_name.strip() == "":
            print("     Please enter name!")
            continue
        break

    while True:
        location_request = input("     Enter the location: ")
        if location_request.strip() == "":
            print("     Please enter location!")
            continue
        break

    while True:
        try:
            urgency_level = int(input("     Enter urgency level (1-5): "))
            if 1 <= urgency_level <= 5:
                break
            else:
                print("     Must be between 1-5!")
                continue
        except ValueError:
            print("     Must be integer!")

    while True:
        try:
            estimated_cost = float(input("     Enter Estimated Cost: "))
            break
        except ValueError:
            print("     Please enter float!")

    print("     Status: 1. Open | 2. In Progress | 3. Closed")
    while True:
        user_status = input("     Please Enter Request Status (1/2/3): ")
        if user_status.strip() == "1" or user_status.strip() == "2" or user_status.strip() == "3":
            if user_status.strip() == "1":
                user_status = "Open"
            elif user_status.strip() == "2":
                user_status = "In Progress"
            elif user_status.strip() == "3":
                user_status = "Closed"
            break
        else:
            print("     Please enter between 1-3!")
            continue

    if user_input == "1":
        user_issue_type = input("     Enter Issue Type: ")
        while True:
            try:
                user_days_open = int(input("     Days Open: "))
                break
            except ValueError:
                print("     Please enter an integer!")
        obj = MaintenanceRequest(user_request_id, "Maintenance", requester_name, location_request, urgency_level, estimated_cost, user_status, user_issue_type.strip(), user_days_open)
    elif user_input == "2":
        while True:
            try:
                attendees = int(input("     Please Enter Attendees: "))
                break
            except ValueError:
                print("     Please enter an integer!")

        while True:
            user_event_date = input("     Please Enter Event Date (YYYY-MM-DD): ")
            parts = user_event_date.strip().split("-")

            if len(parts) == 3 and len(parts[0]) == 4 and len(parts[1]) == 2 and len(parts[2]) == 2 and user_event_date.replace("-", "").isdigit():
                break
            else:
                print("     Please enter the date using YYYY-MM-DD format!")

        obj = EventRequest(user_request_id, "EventSupport", requester_name, location_request, urgency_level, estimated_cost, user_status, attendees, user_event_date.strip())
    elif user_input == "3":
        while True:
            try:
                user_hazard_level = int(input("     Enter Hazard Level: "))
                break
            except ValueError:
                print("     Please enter an integer!")

        while True:
            try:
                user_response_time_minutes = int(input("     Please Enter Response Time: "))
                break
            except ValueError:
                print("     Please enter an integer!")
        obj = EmergencyRequest(user_request_id, "Emergency", requester_name, location_request, urgency_level, estimated_cost, user_status, user_hazard_level, user_response_time_minutes)
    else:
        print("     Invalid!")
        return

    manager.add_request(obj)
    print("     Added Successfully!")


def search_requests(manager):
    print("     Search Type: 1. Search by ID | 2. Search by Type | 3. Status")

    while True:
        user_choice = input("     Please enter your choice (1/2/3): ")
        if user_choice.strip() == "1" or user_choice.strip() == "2" or user_choice.strip() == "3":
            break
        else:
            print("     Please enter between 1-3!")
            continue

    if user_choice == "1":
        user_id = input("     Please enter the ID: ")
        result = manager.search_by_id(user_id.strip())
        if result is None:
            print("     ID does not exist!")
        else:
            print()
            print("     %-6s | %-13s | %-30s | %-20s | %-3s | %-8s  | %-12s  | %-15s               | %-3s" % ("ID",
                                                                                                              "Type",
                                                                                                              "Name",
                                                                                                              "Location",
                                                                                                              "Urg",
                                                                                                              "Est Cost",
                                                                                                              "Status",
                                                                                                              "Detail 1",
                                                                                                              "Detail 2"))
            print(
                "     ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            result.show_info()
            print()
    elif user_choice == "2":
        print("     Request Type: Maintenance | EventSupport | Emergency ")
        user_type = input("     Please enter request type: ")

        result = manager.search_by_type(user_type.strip())
        if len(result) == 0:
            print("     Type does not exist!")
        else:
            print()
            print("     %-6s | %-13s | %-30s | %-20s | %-3s | %-8s  | %-12s  | %-15s               | %-3s" % ("ID",
                                                                                                              "Type",
                                                                                                              "Name",
                                                                                                              "Location",
                                                                                                              "Urg",
                                                                                                              "Est Cost",
                                                                                                              "Status",
                                                                                                              "Detail 1",
                                                                                                              "Detail 2"))
            print(
                "     ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            for i in result:
                i.show_info()
            print()
    elif user_choice == "3":
        print("     Status Type: Open | In Progress | Closed")
        user_status = input("     Please enter request status: ")

        result = manager.search_by_status(user_status.strip())
        if len(result) == 0:
            print("     Status does not exist!")
        else:
            print()
            print("     %-6s | %-13s | %-30s | %-20s | %-3s | %-8s  | %-12s  | %-15s               | %-3s" % ("ID",
                                                                                                              "Type",
                                                                                                              "Name",
                                                                                                              "Location",
                                                                                                              "Urg",
                                                                                                              "Est Cost",
                                                                                                              "Status",
                                                                                                              "Detail 1",
                                                                                                              "Detail 2"))
            print(
                "     ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            for i in result:
                i.show_info()
            print()

def delete_request_id(manager):
    user_id_request = input("     Please enter the ID to delete: ")

    result = manager.search_by_id(user_id_request.strip())
    if result is None:
        print("     ID does not exist!")
    else:
        manager.delete_request(user_id_request.strip())
        print("     Request deleted")

def prioritize(manager):
    result = prioritize_requests(manager.get_all_requests())

    if len(result) == 0:
        print("     Requests not found")
    else:
        print()
        print("     %-6s | %-13s | %-30s | %-20s | %-3s | %-8s  | %-12s  | %-15s               | %-3s" % ("ID", "Type",
                                                                                                          "Name",
                                                                                                          "Location",
                                                                                                          "Urg",
                                                                                                          "Est Cost",
                                                                                                          "Status",
                                                                                                          "Detail 1",
                                                                                                          "Detail 2"))
        print(
            "     ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        for i in result:
            i.show_info()
        print()

def get_recommendation(manager):
    user_request_id = input("     Enter Request ID: ")
    result = manager.search_by_id(user_request_id.strip())

    if result is None:
        print("     ID does not exist!")
    else:
        print()
        print("     Recommendation:")
        print(recommendation_request(result))
        print()



def menu(manager):
    check = False

    while not check:
        print("---- Community Service Request Tracking and Response System ----")
        print("     1. View All Requests")
        print("     2. Add New Requests")
        print("     3. Search Requests")
        print("     4. Delete Requests")
        print("     5. Prioritize Requests")
        print("     6. Get Recommendation")
        print("     7. Exit")

        user_input_choice = input("     Please select an option: ")

        if user_input_choice.strip() == "1":
            view_all(manager)
        elif user_input_choice.strip() == "2":
            add_new_requests(manager)
        elif user_input_choice.strip() == "3":
            search_requests(manager)
        elif user_input_choice.strip() == "4":
            delete_request_id(manager)
        elif user_input_choice.strip() == "5":
            prioritize(manager)
        elif user_input_choice.strip() == "6":
            get_recommendation(manager)
        elif user_input_choice.strip() == "7":
            print("     Thankyou for using Service Request!")
            check = True
        else:
            print("     Invalid Choice!")