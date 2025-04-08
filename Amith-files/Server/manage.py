#!/usr/bin/env python
import os
import sys

#the below is for logging - cureently with launcher script this is creating double logs
# import logging
# from logging.handlers import RotatingFileHandler
#
# def setup_logging():
#     logger = logging.getLogger()
#     logger.setLevel(logging.INFO)
#     handler = RotatingFileHandler('scidentai_server.log', maxBytes=5*1024*1024, backupCount=3)
#     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     handler.setFormatter(formatter)
#     logger.addHandler(handler)
#
#     # Redirect stdout and stderr to the logger
#     sys.stdout = LoggerWriter(logger.info)
#     sys.stderr = LoggerWriter(logger.error)
#
# class LoggerWriter:
#     def __init__(self, level):
#         self.level = level
#
#     def write(self, message):
#         if message != '\n':
#             self.level(message)
#
#     def flush(self):
#         pass
#
# if __name__ == "__main__":
#     setup_logging()

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?"
        ) from exc

    # Default to 'runserver' if no command-line arguments are provided
    if len(sys.argv) == 1:
        sys.argv.append('runserver')
        sys.argv.append('0.0.0.0:8000')  # Bind to 0.0.0.0 and port 8000
        sys.argv.append('--noreload')  # Add the --noreload flag

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
