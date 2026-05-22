# Community Service Request Tracking and Response System

A desktop application for managing and tracking community service requests, supporting three request types: Maintenance, Event Support, and Emergency, with full CRUD operations, priority sorting, and automated recommendations.

---

## Background

This project started as a final assignment for **IST242 — Intermediate & Object-Oriented Application Development**. The original version was a console-based CLI application that covered object-oriented programming concepts such as inheritance, encapsulation, and polymorphism, with the same layered architecture used in the current version.

After completing the course, I continued developing the project independently to take my skills further. The improved version introduces a full desktop GUI built with CustomTkinter and persistent data storage using SQLite, while keeping the same overall architecture intact.

As a Cybersecurity student, I also made sure to apply security best practices during development. All database interactions use **parameterized queries** to prevent SQL injection attacks, rather than building raw query strings from user input.

---

## Features

- **View All Requests** — Browse every submitted request in a clean table view
- **Add New Request** — Dynamic form that adapts based on the selected request type
- **Search Request** — Filter requests by ID, type, or status
- **Delete Request** — Preview a request before confirming deletion
- **Prioritize Requests** — View requests sorted from highest to lowest urgency
- **Get Recommendation** — Receive an actionable recommendation based on request details

---

## Tech Stack

- **Python 3**
- **CustomTkinter** — Modern dark-themed GUI framework
- **SQLite** — Lightweight local database for persistent storage
- **Pillow** — Image handling for recommendation icons

---

## Security

All database queries are executed using **parameterized queries** (also known as prepared statements) via Python's `sqlite3` module. This ensures that user input is never interpolated directly into SQL strings. This is done to prevent SQL injection attacks.

```python
# Safe — user input is passed as a parameter, never concatenated into the query
cur.execute("DELETE FROM service_requests WHERE request_id = ?", (request_id.upper(),))

# Unsafe — never done in this project
cur.execute("DELETE FROM service_requests WHERE request_id = " + request_id)
```

---

## Project Structure

```
Community-Service-Request-Tracking-and-Response-System/
│
├── main.py                  # Entry point
│
├── data/
│   ├── __init__.py
│   └── db_handler.py        # All SQLite database operations
│
├── models/
│   ├── __init__.py
│   ├── servicerequest.py    # Base class for all request types
│   ├── maintenancerequest.py
│   ├── eventrequest.py
│   └── emergencyrequest.py
│
├── services/
│   ├── __init__.py
│   ├── RequestManager.py    # Business logic and CRUD operations
│   └── Recommendation.py   # Recommendation and prioritization logic
│
├── presentation/
│   ├── __init__.py
│   ├── assets/
│   │   ├── green.png
│   │   ├── yellow.png
│   │   └── red.png
│   └── gui.py               # All UI views built with CustomTkinter
│
├── cli-version/             # Original IST242 course submission (CLI, no database)
│
├── requirements.txt
└── README.md
```

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/bintangdaniello/Community-Service-Request-Tracking-and-Response-System.git
   cd Community-Service-Request-Tracking-and-Response-System
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # macOS / Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

> The SQLite database (`service_request_table.db`) is created automatically on first run.

---

## Usage

| Field | Details |
|---|---|
| Request ID | Numbers only. The `SR` prefix is added automatically (e.g. `001` → `SR001`) |
| Urgency Level | Integer from 1 (low) to 5 (critical) |
| Status | `Open`, `In Progress`, or `Closed` |
| Event Date | Format: `YYYY-MM-DD` |

---

## Version History

### v2 — GUI + Database (Current)
Built after completing IST242 as a personal improvement project. Adds a full desktop GUI using CustomTkinter and persistent storage with SQLite, while keeping the same layered architecture from v1.

### v1 — CLI Version (IST242 Course Submission)
The original console-based version submitted as a course project for IST242. Focused on OOP fundamentals: inheritance, encapsulation, and polymorphism. Source code is preserved in the `cli-version/` folder.
