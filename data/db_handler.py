"""
Data access layer for the Community Service Request Tracking System.

All direct SQLite interactions are centralised here so that the rest of the
application remains decoupled from the underlying database implementation.

Database : service_request_table.db (SQLite, created automatically on first run)
Table    : service_requests
"""

import sqlite3

from models.maintenancerequest import MaintenanceRequest
from models.eventrequest import EventRequest
from models.emergencyrequest import EmergencyRequest

def init_db():
    """
    Create the service_requests table if it does not already exist.

    All three request types share a single table (Maintenance, EventSupport, Emergency).
    Columns unused by a particular type are stored as NULL.
    """
    conn = sqlite3.connect("service_request_table.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS service_requests (
    request_id TEXT PRIMARY KEY,
    request_type TEXT,
    requester_name TEXT,
    location TEXT,
    urgency_level INTEGER,
    estimated_cost REAL,
    status TEXT,
    issue_type TEXT,
    days_open INTEGER,
    attendees INTEGER,
    event_date TEXT,
    hazard_level INTEGER,
    response_time_minutes INTEGER)""")
    conn.commit()
    conn.close()

def read_db():
    """
    Load all rows from the database and turn them into request objects.

    Rows with an unknown type are skipped to prevent
    crashes caused by corrupt or legacy data.
    :return : list : List of MaintenanceRequest, EventRequest, or EmergencyRequest objects
    """
    list_of_object = []

    conn = sqlite3.connect("service_request_table.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM service_requests")
    rows = cur.fetchall()
    conn.close()

    for row in rows:
        request_id, request_type, requester_name, location, urgency_level, estimated_cost, status, issue_type, days_open, attendees, event_date, hazard_level, response_time_minutes = row
        if request_type.lower() == "maintenance":
            obj = MaintenanceRequest(request_id, request_type, requester_name, location, int(urgency_level),
                                     float(estimated_cost), status, issue_type, int(days_open))
        elif request_type.lower() == "eventsupport":
            obj = EventRequest(request_id, request_type, requester_name, location, int(urgency_level),
                               float(estimated_cost), status, int(attendees), event_date)
        elif request_type.lower() == "emergency":
            obj = EmergencyRequest(request_id, request_type, requester_name, location, int(urgency_level),
                                   float(estimated_cost), status, int(hazard_level), int(response_time_minutes))
        else:
            continue
        list_of_object.append(obj)

    return list_of_object


def insert_request(request):
    """
    Save a new request to the database.

    Columns that don't belong to this request type are set to None (NULL),
    so every row always has the same structure.
    """
    conn = sqlite3.connect("service_request_table.db")
    cur = conn.cursor()

    if request.request_type.lower() == "maintenance":
        values = (request.request_id, request.request_type, request.requester_name,
                  request.location, request.urgency_level, request.estimated_cost,
                  request.status, request.issue_type, request.days_open, None, None, None, None)

    elif request.request_type.lower() == "eventsupport":
        values = (request.request_id, request.request_type, request.requester_name,
                  request.location, request.urgency_level, request.estimated_cost,
                  request.status, None, None, request.attendees, request.event_date, None, None)

    elif request.request_type.lower() == "emergency":
        values = (request.request_id, request.request_type, request.requester_name,
                  request.location, request.urgency_level, request.estimated_cost,
                  request.status, None, None, None, None,
                  request.hazard_level, request.response_time_minutes)

    cur.execute("""INSERT INTO  service_requests (request_id, request_type,
        requester_name, location, urgency_level, estimated_cost, status, issue_type, days_open, attendees,
        event_date, hazard_level, response_time_minutes) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", values)
    conn.commit()
    conn.close()

def delete_request(request_id):
    """
    Delete a request from the database by its ID.

    The ID is uppercased before matching to stay consistent with
    how IDs are stored (e.g. 'SR001').
    """
    conn = sqlite3.connect("service_request_table.db")
    cur = conn.cursor()
    cur.execute("""DELETE FROM service_requests WHERE request_id = ?""", (request_id.upper(),))
    conn.commit()
    conn.close()
