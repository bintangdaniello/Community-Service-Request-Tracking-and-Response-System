"""
Presentation layer for the Community Service Request Tracking and Response System.

Built with CustomTkinter for a modern and dark themed desktop UI.
The App class is the root window and owns all views; each 'show_*' method
clears the main area and renders the corresponding view in-place.

Views:
- View All Requests   : Tabular list of every request in the system.
- Add New Request     : Dynamic form that adapts to the selected request type.
- Search Request      : Filter requests by ID, type, or status.
- Delete Request      : Preview a request before confirming deletion.
- Prioritize Requests : Display requests sorted by urgency (highest first).
- Get Recommendation  : Show an actionable recommendation for a specific request.
"""

from PIL import Image
import os

import customtkinter as ctk
from tkinter import ttk

from models.emergencyrequest import EmergencyRequest
from models.eventrequest import EventRequest
from models.maintenancerequest import MaintenanceRequest

from services.Recommendation import recommendation_request, prioritize_requests

# Global Appearance / Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    """
    Root application window.

    Owns the persistent sidebar (navigation) and a main content area that
    is rebuilt each time the user switches views.
    """
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.title("Community Service Request Tracking and Response System")
        self.geometry("1100x600")

        # Sidebar (left panel)
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y", pady=10, padx=10)

        # Dark theme styling for all Treeview widgets used across the app
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", rowheight=50, font=("Arial", 11))
        style.configure("Treeview.Heading", background="#1f538d", foreground="white", font=("Arial", 11, "bold"))
        style.map("Treeview", background=[("selected", "#1f538d")])

        # Main content area (right panel)
        self.main_area = ctk.CTkFrame(self)
        self.main_area.pack(side="right", fill="both", expand=True, pady=10, padx=10)

        # Sidebar title
        self.title_label = ctk.CTkLabel(self.sidebar, text="Service Requests", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=(20, 0), padx=5)
        self.title_label_2 = ctk.CTkLabel(self.sidebar, text="System", font=("Arial", 18, "bold"))
        self.title_label_2.pack(pady=(0, 20), padx=5)

        # Navigation buttons
        self.view_all_btn = ctk.CTkButton(self.sidebar, text="View All Requests", font=("Arial", 15, "bold"), command=self.show_view_all)
        self.view_all_btn.pack(pady=5, padx=10, fill="x")
        self.add_request_btn = ctk.CTkButton(self.sidebar, text="Add New Request", font=("Arial", 15, "bold"), command=self.show_add_request)
        self.add_request_btn.pack(pady=5, padx=10, fill="x")
        self.search_request_btn = ctk.CTkButton(self.sidebar, text="Search Request", font=("Arial", 15, "bold"), command=self.show_search)
        self.search_request_btn.pack(pady=5, padx=10, fill="x")
        self.delete_request_btn = ctk.CTkButton(self.sidebar, text="Delete Request", font=("Arial", 15, "bold"), command=self.show_delete)
        self.delete_request_btn.pack(pady=5, padx=10, fill="x")
        self.prioritize_btn = ctk.CTkButton(self.sidebar, text="Prioritize Requests", font=("Arial", 15, "bold"), command=self.show_prioritize)
        self.prioritize_btn.pack(pady=5, padx=10, fill="x")
        self.recommendation_btn = ctk.CTkButton(self.sidebar, text="Get Recommendation", font=("Arial", 15, "bold"), command=self.show_recommendation)
        self.recommendation_btn.pack(pady=5, padx=10, fill="x")

    def clear_main_area(self):
        """
        Remove all widgets from the main content area before rendering a new view.
        """
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def show_view_all(self):
        """
        View: View All Requests.
        """
        self.clear_main_area()

        view_all_title = ctk.CTkLabel(self.main_area, text="Service Requests", font=("Arial", 20, "bold"))
        view_all_title.pack(pady=10)

        columns = ("ID", "Type", "Name", "Location", "Urgency", "Est Cost", "Status", "Detail 1", "Detail 2")
        tree = ttk.Treeview(self.main_area, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        requests_obj = self.manager.get_all_requests()
        for i in requests_obj:
            # Map type-specific fields to the two generic detail columns
            if i.request_type.lower() == "maintenance":
                detail1 = "Issue: %s" % i.issue_type
                detail2 = "Days Open: %d" % i.days_open
            elif i.request_type.lower() == "eventsupport":
                detail1 = "Attendees: %d" % i.attendees
                detail2 = "Date: %s" % i.event_date
            elif i.request_type.lower() == "emergency":
                detail1 = "Hazard: %d" % i.hazard_level
                detail2 = "Response: %d min" % i.response_time_minutes
            est_cost = "$%.2f" % i.estimated_cost
            tree.insert("", "end", values=(i.request_id, i.request_type, i.requester_name, i.location, i.urgency_level, est_cost, i.status, detail1, detail2))

        tree.pack(fill="both", expand=True, padx=10, pady=10)

    def show_add_request(self):
        """
        Add: Add New Request.
        """
        self.clear_main_area()

        title = ctk.CTkLabel(self.main_area, text="Add New Request", font=("Arial", 20, "bold"))
        title.pack(pady=10)

        # Dropdown to select the request type; triggers form rebuild on change
        type_var = ctk.StringVar(value="Maintenance")
        request_dropdown = ctk.CTkOptionMenu(self.main_area, values=["Maintenance", "Event Support", "Emergency"], variable=type_var)
        request_dropdown.pack(pady=10)

        form_frame = ctk.CTkScrollableFrame(self.main_area)
        form_frame.pack(padx=10, pady=10, fill="both", expand=True)

        submit_button = ctk.CTkButton(self.main_area, text="Submit")
        submit_button.pack(pady=10)

        error_label = ctk.CTkLabel(self.main_area, text="", font=("Arial", 14), text_color="red")
        error_label.pack()

        # Entry references: reassigned every time update_form() rebuilds the form
        id_entry = None
        name_entry = None
        location_entry = None
        urgency_entry = None
        est_cost_entry = None
        status_entry = None
        detail1_entry = None
        detail2_entry = None

        def update_form(choice):
            """
            Rebuild the form fields whenever the request type dropdown changes.
            """
            nonlocal id_entry, name_entry, location_entry, urgency_entry, est_cost_entry, status_entry, detail1_entry, detail2_entry

            for i in form_frame.winfo_children():
                i.destroy()

            # Common fields (shared by all request types)
            ctk.CTkLabel(form_frame, text="Request ID: ", font=("Arial", 14)).grid(column=0, row=0, padx=10, pady=15, sticky="w")
            id_entry = ctk.CTkEntry(form_frame, width=150)
            id_entry.grid(column=1, row=0, padx=10, pady=10)

            ctk.CTkLabel(form_frame, text="Requester Name: ", font=("Arial", 14)).grid(column=0, row=1, padx=10, pady=15, sticky="w")
            name_entry = ctk.CTkEntry(form_frame, width=150)
            name_entry.grid(column=1, row=1, padx=10)

            ctk.CTkLabel(form_frame, text="Location: ", font=("Arial", 14)).grid(column=0, row=2, padx=10, pady=15, sticky="w")
            location_entry = ctk.CTkEntry(form_frame, width=150)
            location_entry.grid(column=1, row=2, padx=10)

            ctk.CTkLabel(form_frame, text="Urgency Level: ", font=("Arial", 14)).grid(column=0, row=3, padx=10, pady=15, sticky="w")
            urgency_entry = ctk.CTkEntry(form_frame, width=150)
            urgency_entry.grid(column=1, row=3, padx=10)

            ctk.CTkLabel(form_frame, text="Estimated Cost: ", font=("Arial", 14)).grid(column=0, row=4, padx=10, pady=15, sticky="w")
            est_cost_entry = ctk.CTkEntry(form_frame, width=150)
            est_cost_entry.grid(column=1, row=4, padx=10)

            ctk.CTkLabel(form_frame, text="Status: ", font=("Arial", 14)).grid(column=0, row=5, padx=10, pady=15, sticky="w")
            status_entry = ctk.CTkEntry(form_frame, width=150)
            status_entry.grid(column=1, row=5, padx=10)

            if choice == "Maintenance":
                ctk.CTkLabel(form_frame, text="Issue Type: ", font=("Arial", 14)).grid(column=0, row=6, padx=10, pady=15,sticky="w")
                detail1_entry = ctk.CTkEntry(form_frame, width=150)
                detail1_entry.grid(column=1, row=6, padx=10)

                ctk.CTkLabel(form_frame, text="Days Open: ", font=("Arial", 14)).grid(column=0, row=7, padx=10, pady=15, sticky="w")
                detail2_entry = ctk.CTkEntry(form_frame, width=150)
                detail2_entry.grid(column=1, row=7, padx=10)
            elif choice == "Event Support":
                ctk.CTkLabel(form_frame, text="Attendees: ", font=("Arial", 14)).grid(column=0, row=6, padx=10, pady=15, sticky="w")
                detail1_entry = ctk.CTkEntry(form_frame, width=150)
                detail1_entry.grid(column=1, row=6, padx=10)

                ctk.CTkLabel(form_frame, text="Event Date: ", font=("Arial", 14)).grid(column=0, row=7, padx=10, pady=15, sticky="w")
                detail2_entry = ctk.CTkEntry(form_frame, width=150)
                detail2_entry.grid(column=1, row=7, padx=10)
            elif choice == "Emergency":
                ctk.CTkLabel(form_frame, text="Hazard Level: ", font=("Arial", 14)).grid(column=0, row=6, padx=10, pady=15, sticky="w")
                detail1_entry = ctk.CTkEntry(form_frame, width=150)
                detail1_entry.grid(column=1, row=6, padx=10)

                ctk.CTkLabel(form_frame, text="Response Time: ", font=("Arial", 14)).grid(column=0, row=7, padx=10, pady=15, sticky="w")
                detail2_entry = ctk.CTkEntry(form_frame, width=150)
                detail2_entry.grid(column=1, row=7, padx=10)

        def submit():
            """
            Validate all inputs, then build and save the appropriate request object.
            """
            if not id_entry.get() or not name_entry.get() or not location_entry.get() or not urgency_entry.get() or not est_cost_entry.get() or not status_entry.get() or not detail1_entry.get() or not detail2_entry.get():
                error_label.configure(text="Please enter all fields")
                return

            # Request ID must be numeric (the 'SR' prefix is added automatically)
            if not id_entry.get().strip().isdigit():
                error_label.configure(text="Request ID must be numbers only!")
                return

            # Urgency must be an integer; estimated cost must be a number
            try:
                urgency = int(urgency_entry.get())
                est_cost = float(est_cost_entry.get())
            except ValueError:
                error_label.configure(text="Urgency and Estimated Cost must be an integer and float, respectively")
                return

            # Prevent duplicate IDs
            if self.manager.search_by_id("SR" + id_entry.get().strip()) is not None:
                error_label.configure(text="Request ID already exists")
                return

            # Urgency must be between 1 and 5
            if urgency < 1 or urgency > 5:
                error_label.configure(text="Urgency must be between 1 and 5")
                return

            # Status must be one of the three accepted values
            if status_entry.get().strip().lower() != "open" and status_entry.get().strip().lower() != "in progress" and status_entry.get().strip().lower() != "closed":
                error_label.configure(text="Status must be either Open, In Progress, Closed")
                return

            # Type-specific field validation
            try:
                if type_var.get() == "Maintenance":
                    days_open = int(detail2_entry.get())
            except ValueError:
                error_label.configure(text="Day open must be an integer")
                return
            try:
                if type_var.get() == "Event Support":
                    attendees = int(detail1_entry.get())
            except ValueError:
                error_label.configure(text="Attendees must be an integer")
                return
            try:
                if type_var.get() == "Emergency":
                    hazard_level = int(detail1_entry.get())
                    response_time = int(detail2_entry.get())
            except ValueError:
                error_label.configure(text="Hazard level and response time must be an integer")
                return

            # Event date must follow YYYY-MM-DD format
            try:
                if type_var.get() == "Event Support":
                    parts = detail2_entry.get().strip().split("-")
                    if not (len(parts) == 3 and len(parts[0]) == 4 and len(parts[1]) == 2 and len(parts[2]) == 2 and detail2_entry.get().replace("-", "").isdigit()):
                        raise ValueError
            except ValueError:
                error_label.configure(text="Please enter the date using YYYY-MM-DD format!", text_color="red")
                return

            # Build the request object based on the selected type
            request_id = "SR" + id_entry.get().strip()
            request_name = name_entry.get().strip()
            request_location = location_entry.get().strip()
            request_urgency = urgency
            request_est_cost = est_cost
            if status_entry.get().strip().lower() == "open":
                request_status = "Open"
            elif status_entry.get().strip().lower() == "in progress":
                request_status = "In Progress"
            elif status_entry.get().strip().lower() == "closed":
                request_status = "Closed"


            if type_var.get() == "Maintenance":
                request_detail1 = detail1_entry.get()
                request_detail2 = days_open
                obj = MaintenanceRequest(request_id, "Maintenance", request_name, request_location, request_urgency, request_est_cost, request_status, request_detail1, request_detail2)
            elif type_var.get() == "Event Support":
                request_detail1 = attendees
                request_detail2 = detail2_entry.get()
                obj = EventRequest(request_id, "EventSupport", request_name, request_location, request_urgency, request_est_cost, request_status, request_detail1, request_detail2)
            elif type_var.get() == "Emergency":
                request_detail1 = hazard_level
                request_detail2 = response_time
                obj = EmergencyRequest(request_id, "Emergency", request_name, request_location, request_urgency, request_est_cost, request_status, request_detail1, request_detail2)

            self.manager.add_request(obj)
            error_label.configure(text="Request submitted successfully!", text_color="green")

        submit_button.configure(command=submit)
        request_dropdown.configure(command=update_form)
        update_form("Maintenance")


    def show_search(self):
        """
        View: Search Request
        """
        self.clear_main_area()

        search_title = ctk.CTkLabel(self.main_area, text="Search Results", font=("Arial", 20, "bold"))
        search_title.pack(pady=10)

        search_bar_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        search_bar_frame.pack(pady=10)

        # Dropdown to choose the search filter type
        type_var = ctk.StringVar(value="Search by ID")
        search_dropdown = ctk.CTkOptionMenu(search_bar_frame, values=["Search by ID", "Search by Type", "Search by Status"], variable=type_var, width=160)
        search_dropdown.pack(side="left", padx=5)

        search_entry = ctk.CTkEntry(search_bar_frame, width=400)
        search_entry.pack(side="left", padx=5)

        search_button = ctk.CTkButton(search_bar_frame, text="Search")
        search_button.pack(side="left", padx=5)

        columns = ("ID", "Type", "Name", "Location", "Urgency", "Est Cost", "Status", "Detail 1", "Detail 2")
        tree = ttk.Treeview(self.main_area, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        tree.pack(fill="both", expand=True, padx=10, pady=10)

        error_label = ctk.CTkLabel(self.main_area, text="", font=("Arial", 14))
        error_label.pack()

        def search():
            """
            Run the selected search and populate the treeview with results.
            """
            tree.delete(*tree.get_children())
            error_label.configure(text="")

            if type_var.get() == "Search by ID":
                if self.manager.search_by_id(search_entry.get().strip()) is None:
                    error_label.configure(text="ID does not exist", text_color="red")
                    return
                else:
                    i = self.manager.search_by_id(search_entry.get().strip())
                    if i.request_type.lower().strip() == "maintenance":
                        detail1 = "Issue: %s" % i.issue_type
                        detail2 = "Days Open: %d" % i.days_open
                    elif i.request_type.lower().strip() == "eventsupport":
                        detail1 = "Attendees: %d" % i.attendees
                        detail2 = "Date: %s" % i.event_date
                    elif i.request_type.lower() == "emergency":
                        detail1 = "Hazard: %d" % i.hazard_level
                        detail2 = "Response: %d min" % i.response_time_minutes
                    est_cost = "$%.2f" % i.estimated_cost
                    tree.insert("", "end", values=(i.request_id, i.request_type, i.requester_name, i.location, i.urgency_level, est_cost, i.status, detail1, detail2))
            elif type_var.get() == "Search by Type":
                if len(self.manager.search_by_type(search_entry.get().strip())) == 0:
                    error_label.configure(text="Type does not exist", text_color="red")
                    return
                else:
                    obj = self.manager.search_by_type(search_entry.get().strip())
                    for i in obj:
                        if i.request_type.lower().strip() == "maintenance":
                            detail1 = "Issue: %s" % i.issue_type
                            detail2 = "Days Open: %d" % i.days_open
                        elif i.request_type.lower().strip() == "eventsupport":
                            detail1 = "Attendees: %d" % i.attendees
                            detail2 = "Date: %s" % i.event_date
                        elif i.request_type.lower() == "emergency":
                            detail1 = "Hazard: %d" % i.hazard_level
                            detail2 = "Response: %d min" % i.response_time_minutes
                        est_cost = "$%.2f" % i.estimated_cost
                        tree.insert("", "end", values=(i.request_id, i.request_type, i.requester_name, i.location, i.urgency_level, est_cost, i.status, detail1, detail2))
            elif type_var.get() == "Search by Status":
                if len(self.manager.search_by_status(search_entry.get().strip())) == 0:
                    error_label.configure(text="Status does not exist", text_color="red")
                    return
                else:
                    obj = self.manager.search_by_status(search_entry.get().strip())
                    for i in obj:
                        if i.request_type.lower().strip() == "maintenance":
                            detail1 = "Issue: %s" % i.issue_type
                            detail2 = "Days Open: %d" % i.days_open
                        elif i.request_type.lower().strip() == "eventsupport":
                            detail1 = "Attendees: %d" % i.attendees
                            detail2 = "Date: %s" % i.event_date
                        elif i.request_type.lower() == "emergency":
                            detail1 = "Hazard: %d" % i.hazard_level
                            detail2 = "Response: %d min" % i.response_time_minutes
                        est_cost = "$%.2f" % i.estimated_cost
                        tree.insert("", "end", values=(i.request_id, i.request_type, i.requester_name, i.location, i.urgency_level, est_cost, i.status, detail1, detail2))

        search_button.configure(command=search)

    def show_delete(self):
        """
        View: Delete Request
        """
        self.clear_main_area()

        delete_title = ctk.CTkLabel(self.main_area, text="Delete Request", font=("Arial", 20, "bold"))
        delete_title.pack(pady=10)

        delete_search_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        delete_search_frame.pack(pady=10)

        ctk.CTkLabel(delete_search_frame, text="ID:", font=("Arial", 18, "bold")).pack(side="left", padx=5)

        search_entry = ctk.CTkEntry(delete_search_frame, width=400)
        search_entry.pack(side="left", padx=5)

        search_button = ctk.CTkButton(delete_search_frame, text="Search")
        search_button.pack(side="left", padx=5)

        # Preview panel: shows the request details before the user confirms deletion
        preview_frame = ctk.CTkFrame(self.main_area)
        preview_frame.pack(padx=20, pady=10, fill="both", expand=True)

        error_label = ctk.CTkLabel(self.main_area, text="", font=("Arial", 13), text_color="red")
        error_label.pack(pady=5)

        def delete():
            """
            Delete the currently previewed request and clear the preview panel.
            """
            self.manager.delete_request(search_entry.get().strip())
            error_label.configure(text="Request successfully deleted", text_color="green")
            for i in preview_frame.winfo_children():
                i.destroy()

        def search():
            """
            Look up the entered ID and populate the preview panel if found.
            """
            error_label.configure(text="")

            for widget in preview_frame.winfo_children():
                widget.destroy()

            result = self.manager.search_by_id(search_entry.get().strip())

            if result is None:
                error_label.configure(text="ID does not exist", text_color="red")
                return

            # Common fields
            ctk.CTkLabel(preview_frame, text="Request ID", font=("Arial", 13)).grid(row=0, column=0, padx=15, pady=5, sticky="w")
            ctk.CTkLabel(preview_frame, text=result.request_id, font=("Arial", 13)).grid(row=0, column=1, padx=100, pady=5, sticky="w")

            ctk.CTkLabel(preview_frame, text="Type", font=("Arial", 13)).grid(row=1, column=0, padx=15, pady=5, sticky="w")
            ctk.CTkLabel(preview_frame, text=result.request_type, font=("Arial", 13)).grid(row=1, column=1, padx=100, pady=5, sticky="w")

            ctk.CTkLabel(preview_frame, text="Requester", font=("Arial", 13)).grid(row=2, column=0, padx=15, pady=5, sticky="w")
            ctk.CTkLabel(preview_frame, text=result.requester_name, font=("Arial", 13)).grid(row=2, column=1, padx=100, pady=5, sticky="w")

            ctk.CTkLabel(preview_frame, text="Location", font=("Arial", 13)).grid(row=3, column=0, padx=15, pady=5, sticky="w")
            ctk.CTkLabel(preview_frame, text=result.location, font=("Arial", 13)).grid(row=3, column=1, padx=100, pady=5, sticky="w")

            ctk.CTkLabel(preview_frame, text="Urgency", font=("Arial", 13)).grid(row=4, column=0, padx=15, pady=5, sticky="w")
            ctk.CTkLabel(preview_frame, text=result.urgency_level, font=("Arial", 13)).grid(row=4, column=1, padx=100, pady=5, sticky="w")

            ctk.CTkLabel(preview_frame, text="Estimated Cost", font=("Arial", 13)).grid(row=5, column=0, padx=15, pady=5, sticky="w")
            ctk.CTkLabel(preview_frame, text="$" + str(result.estimated_cost), font=("Arial", 13)).grid(row=5, column=1, padx=100, pady=5, sticky="w")

            # Status badge with a colour that reflects the current state
            if result.status.lower() == "open":
                status_color = "#2a451c"
            elif result.status.lower() == "in progress":
                status_color = "#4a3000"
            elif result.status.lower() == "closed":
                status_color = "#4a1010"
            ctk.CTkLabel(preview_frame, text="Status", font=("Arial", 13)).grid(row=6, column=0, padx=15, pady=5, sticky="w")
            ctk.CTkLabel(preview_frame, text=result.status, font=("Arial", 13), fg_color=status_color, corner_radius=8, padx=3, pady=0).grid(row=6, column=1, padx=100, pady=5, sticky="w")

            # Type-specific fields
            if result.request_type.lower() == "maintenance":
                ctk.CTkLabel(preview_frame, text="Issue Type", font=("Arial", 13)).grid(row=7, column=0, padx=15, pady=5, sticky="w")
                ctk.CTkLabel(preview_frame, text=result.issue_type, font=("Arial", 13)).grid(row=7, column=1, padx=100, pady=5, sticky="w")

                ctk.CTkLabel(preview_frame, text="Days Open", font=("Arial", 13)).grid(row=8, column=0, padx=15, pady=5, sticky="w")
                ctk.CTkLabel(preview_frame, text=result.days_open, font=("Arial", 13)).grid(row=8, column=1, padx=100, pady=5, sticky="w")
            elif result.request_type.lower() == "eventsupport":
                ctk.CTkLabel(preview_frame, text="Attendees", font=("Arial", 13)).grid(row=7, column=0, padx=15, pady=5, sticky="w")
                ctk.CTkLabel(preview_frame, text=result.attendees, font=("Arial", 13)).grid(row=7, column=1, padx=100, pady=5, sticky="w")

                ctk.CTkLabel(preview_frame, text="Event Date", font=("Arial", 13)).grid(row=8, column=0, padx=15, pady=5, sticky="w")
                ctk.CTkLabel(preview_frame, text=result.event_date, font=("Arial", 13)).grid(row=8, column=1, padx=100, pady=5, sticky="w")
            elif result.request_type.lower() == "emergency":
                ctk.CTkLabel(preview_frame, text="Hazard Level", font=("Arial", 13)).grid(row=7, column=0, padx=15, pady=5, sticky="w")
                ctk.CTkLabel(preview_frame, text=result.hazard_level, font=("Arial", 13)).grid(row=7, column=1, padx=100, pady=5, sticky="w")

                ctk.CTkLabel(preview_frame, text="Response Time", font=("Arial", 13)).grid(row=8, column=0, padx=15, pady=5, sticky="w")
                ctk.CTkLabel(preview_frame, text=str(result.response_time_minutes) + " Minutes", font=("Arial", 13)).grid(row=8, column=1, padx=100, pady=5, sticky="w")

            delete_button = ctk.CTkButton(preview_frame, text="Delete", fg_color="#780606", hover_color="darkred", command=delete)
            delete_button.grid(row=9, column=0, padx=15, pady=15, sticky="w")


        search_button.configure(command=search)


    def show_prioritize(self):
        """
        View: Prioritize Requests
        """
        self.clear_main_area()

        prioritize_title = ctk.CTkLabel(self.main_area, text="Prioritize Requests", font=("Arial", 20, "bold"))
        prioritize_title.pack(pady=10)

        columns = ("ID", "Type", "Name", "Location", "Urgency", "Est Cost", "Status", "Detail 1", "Detail 2")
        tree = ttk.Treeview(self.main_area, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Requests are sorted highest urgency first before being inserted
        sorted_requests = prioritize_requests(self.manager.get_all_requests())
        for i in sorted_requests:
            if i.request_type.lower() == "maintenance":
                detail1 = "Issue: %s" % i.issue_type
                detail2 = "Days Open: %d" % i.days_open
            elif i.request_type.lower() == "eventsupport":
                detail1 = "Attendees: %d" % i.attendees
                detail2 = "Date: %s" % i.event_date
            elif i.request_type.lower() == "emergency":
                detail1 = "Hazard: %d" % i.hazard_level
                detail2 = "Response: %d min" % i.response_time_minutes
            est_cost = "$%.2f" % i.estimated_cost
            tree.insert("", "end", values=(i.request_id, i.request_type, i.requester_name, i.location, i.urgency_level, est_cost, i.status, detail1, detail2))

        tree.pack(fill="both", expand=True, padx=10, pady=10)

    def show_recommendation(self):
        """
        View: Get Recommendation
        """
        self.clear_main_area()

        recommendation_title = ctk.CTkLabel(self.main_area, text="Recommendation", font=("Arial", 20, "bold"))
        recommendation_title.pack(pady=10)

        recommendation_search_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        recommendation_search_frame.pack(pady=10)

        ctk.CTkLabel(recommendation_search_frame, text="ID:", font=("Arial", 18, "bold")).pack(side="left", padx=5)

        search_entry = ctk.CTkEntry(recommendation_search_frame, width=400)
        search_entry.pack(side="left", padx=5)

        get_recommendation_button = ctk.CTkButton(recommendation_search_frame, text="Get Recommendation")
        get_recommendation_button.pack(side="left", padx=5)

        content_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        content_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Left panel: full request details
        preview_frame = ctk.CTkFrame(content_frame)
        preview_frame.pack(padx=10, pady=10, fill="both", expand=True, side="left")

        # Right panel: colour-coded icon + recommendation text
        recommendation_frame = ctk.CTkFrame(content_frame)
        recommendation_frame.pack(padx=10, pady=10, fill="both", expand=True, side="left", anchor="n")

        error_label = ctk.CTkLabel(self.main_area, text="", font=("Arial", 13), text_color="red")
        error_label.pack(pady=5)


        def search():
            """
            Look up the request and render its details alongside a recommendation.
            """
            error_label.configure(text="")

            for widget in preview_frame.winfo_children():
                widget.destroy()

            for widget in recommendation_frame.winfo_children():
                widget.destroy()

            result = self.manager.search_by_id(search_entry.get().strip())

            if result is None:
                error_label.configure(text="ID does not exist", text_color="red")
                return

            # Left panel: request details
            ctk.CTkLabel(preview_frame, text="Request ID", font=("Arial", 13)).grid(row=0, column=0, padx=15, pady=5, sticky="w")
            ctk.CTkLabel(preview_frame, text=result.request_id, font=("Arial", 13)).grid(row=0, column=1, padx=100, pady=5, sticky="w")

            ctk.CTkLabel(preview_frame, text="Type", font=("Arial", 13)).grid(row=1, column=0, padx=15, pady=5, sticky="w")
            ctk.CTkLabel(preview_frame, text=result.request_type, font=("Arial", 13)).grid(row=1, column=1, padx=100, pady=5, sticky="w")

            ctk.CTkLabel(preview_frame, text="Requester", font=("Arial", 13)).grid(row=2, column=0, padx=15, pady=5, sticky="w")
            ctk.CTkLabel(preview_frame, text=result.requester_name, font=("Arial", 13)).grid(row=2, column=1, padx=100, pady=5, sticky="w")

            ctk.CTkLabel(preview_frame, text="Location", font=("Arial", 13)).grid(row=3, column=0, padx=15, pady=5, sticky="w")
            ctk.CTkLabel(preview_frame, text=result.location, font=("Arial", 13)).grid(row=3, column=1, padx=100, pady=5, sticky="w")

            ctk.CTkLabel(preview_frame, text="Urgency", font=("Arial", 13)).grid(row=4, column=0, padx=15, pady=5, sticky="w")
            ctk.CTkLabel(preview_frame, text=result.urgency_level, font=("Arial", 13)).grid(row=4, column=1, padx=100, pady=5, sticky="w")

            ctk.CTkLabel(preview_frame, text="Estimated Cost", font=("Arial", 13)).grid(row=5, column=0, padx=15, pady=5, sticky="w")
            ctk.CTkLabel(preview_frame, text="$" + str(result.estimated_cost), font=("Arial", 13)).grid(row=5, column=1, padx=100, pady=5, sticky="w")

            # Status badge with colour based on current state
            if result.status.lower() == "open":
                status_color = "#2a451c"
            elif result.status.lower() == "in progress":
                status_color = "#4a3000"
            elif result.status.lower() == "closed":
                status_color = "#4a1010"
            ctk.CTkLabel(preview_frame, text="Status", font=("Arial", 13)).grid(row=6, column=0, padx=15, pady=5, sticky="w")
            ctk.CTkLabel(preview_frame, text=result.status, font=("Arial", 13), fg_color=status_color, corner_radius=8, padx=3, pady=0).grid(row=6, column=1, padx=100, pady=5, sticky="w")

            # Type-specific fields
            if result.request_type.lower() == "maintenance":
                ctk.CTkLabel(preview_frame, text="Issue Type", font=("Arial", 13)).grid(row=7, column=0, padx=15, pady=5, sticky="w")
                ctk.CTkLabel(preview_frame, text=result.issue_type, font=("Arial", 13)).grid(row=7, column=1, padx=100, pady=5, sticky="w")

                ctk.CTkLabel(preview_frame, text="Days Open", font=("Arial", 13)).grid(row=8, column=0, padx=15, pady=5, sticky="w")
                ctk.CTkLabel(preview_frame, text=result.days_open, font=("Arial", 13)).grid(row=8, column=1, padx=100, pady=5, sticky="w")
            elif result.request_type.lower() == "eventsupport":
                ctk.CTkLabel(preview_frame, text="Attendees", font=("Arial", 13)).grid(row=7, column=0, padx=15, pady=5, sticky="w")
                ctk.CTkLabel(preview_frame, text=result.attendees, font=("Arial", 13)).grid(row=7, column=1, padx=100, pady=5, sticky="w")

                ctk.CTkLabel(preview_frame, text="Event Date", font=("Arial", 13)).grid(row=8, column=0, padx=15, pady=5, sticky="w")
                ctk.CTkLabel(preview_frame, text=result.event_date, font=("Arial", 13)).grid(row=8, column=1, padx=100, pady=5, sticky="w")
            elif result.request_type.lower() == "emergency":
                ctk.CTkLabel(preview_frame, text="Hazard Level", font=("Arial", 13)).grid(row=7, column=0, padx=15, pady=5, sticky="w")
                ctk.CTkLabel(preview_frame, text=result.hazard_level, font=("Arial", 13)).grid(row=7, column=1, padx=100, pady=5, sticky="w")

                ctk.CTkLabel(preview_frame, text="Response Time", font=("Arial", 13)).grid(row=8, column=0, padx=15, pady=5, sticky="w")
                ctk.CTkLabel(preview_frame, text=str(result.response_time_minutes) + " Minutes", font=("Arial", 13)).grid(row=8, column=1, padx=100, pady=5, sticky="w")

            base_dir = os.path.dirname(__file__)

            # Right panel: recommendation
            recommendation = recommendation_request(result)
            if recommendation is None:
                return

            # Split "SeverityLabel. Detailed explanation." into two display lines
            split = recommendation.split(".")

            # Pick icon colour based on severity keyword in the recommendation text
            if "Urgent" in recommendation or "Large" in recommendation or "Critical" in recommendation:
                icon = os.path.join(base_dir, "assets", "red.png")
            elif "Moderate" in recommendation or "Medium" in recommendation or "High!" in recommendation:
                icon = os.path.join(base_dir, "assets", "yellow.png")
            else:
                icon = os.path.join(base_dir, "assets", "green.png")

            icon_image = ctk.CTkImage(Image.open(icon), size=(150, 150))
            ctk.CTkLabel(recommendation_frame, image=icon_image, text="").grid(row=0, column=0, pady=(30, 0), sticky="n")

            ctk.CTkLabel(recommendation_frame, text=split[0].strip(), font=("Arial", 17, "bold")).grid(row=1, column=0, pady=(0, 5), sticky="n")
            ctk.CTkLabel(recommendation_frame, text=split[1].strip(), font=("Arial", 15, "bold"), wraplength=200).grid(row=2, column=0, pady=5, sticky="n")

        get_recommendation_button.configure(command=search)