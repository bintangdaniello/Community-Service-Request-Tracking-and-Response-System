from services.RequestManager import RequestManager
from presentation.menu import menu

def main():
    manager = RequestManager()
    menu(manager)
main()