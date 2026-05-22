# This module initializes the application by creating a RequestManager instance
# (which handles data persistence and business logic) and launching the GUI

from services.RequestManager import RequestManager
from presentation.gui import App


def main():
    # Initialize the request manager and launch the application window
    manager = RequestManager()
    app = App(manager)
    app.mainloop()
main()