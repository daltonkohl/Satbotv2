#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os  # The OS module in Python provides functions for interacting with the operating system
import sys  # The sys module provides functions and variables that are used to manipulate different parts of the Python runtime environment

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'satbot.settings')  # Sets the environment variable 'DJANGO_SETTINGS_MODULE' to 'satbot.settings' if it isn't already set
    try:
        from django.core.management import execute_from_command_line  # Import the function to run Django commands
    except ImportError as exc:  # If importing Django failed
        raise ImportError(  # Raise a new error explaining that Django is needed
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc  # Attach the original exception
    execute_from_command_line(sys.argv)  # Execute the Django command-line utility

if __name__ == '__main__':  # If this script is run directly (as opposed to being imported)
    main()  # Run the main function