"""
    Lab 9

    My idea of this app is that it is like an admin 
    portal where they can see teir inventory, as 
    well as place orders to suppliers for more stock 
    of a product that is currently in their system.
"""

from app.app_engine import AppEngine
from managers.io_manager import IOManager


def main():
    try:
        AppEngine().run()
    except (KeyboardInterrupt, EOFError):
        print()
        IOManager.show_exit_message()
    except (PermissionError, RuntimeError, OSError) as error:
        print(f"\nThe application could not start or continue: {error}")


if __name__ == "__main__":
    main()
