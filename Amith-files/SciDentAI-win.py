import subprocess
import time
import psutil
import os
import signal
import sys
import logging
from logging.handlers import RotatingFileHandler

# Base paths
def find_app_root():
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return os.path.dirname(sys.executable)
    else:
        # Running as script
        return os.path.dirname(os.path.abspath(__file__))

# Base paths
BASE_DIR=find_app_root()
APP_DIR =os.path.dirname(BASE_DIR)

# Paths and commands
DJANGO_EXECUTABLE = os.path.join(APP_DIR, "server", "SciDentAI-server.exe")
REACT_EXECUTABLE = os.path.join(APP_DIR, "client", "win-unpacked", "client.exe")
LOG_DIR = log_dir = os.path.join(os.getenv('LOCALAPPDATA'), "SciDentAI", "logs")
SERVER_LOG_FILE = os.path.join(LOG_DIR, "ScidentAI-server.log")
APP_LOG = os.path.join(LOG_DIR, "SciApplication.log")
READY_MESSAGE = "Starting development server at"  # Adjust this based on your Django output
#READY_MESSAGE = "WARNING:tensorflow"

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger():
    logger = logging.getLogger('AppLogger')
    logger.setLevel(logging.DEBUG)
    handler = RotatingFileHandler(APP_LOG, maxBytes=5*1024*1024, backupCount=3)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = setup_logger()
#logs being recorded
logger.info(f"BASE_DIR: {BASE_DIR}")
logger.info(f"APP_DIR: {APP_DIR}")
logger.info(f"DJANGO_EXECUTABLE: {DJANGO_EXECUTABLE}")
logger.info(f"REACT_EXECUTABLE: {REACT_EXECUTABLE}")

# def run_django_backend():
#     logger.info("Starting Django backend...")
#     with open(SERVER_LOG_FILE, 'w') as log_file:
#         logger.info(f"Attempting to run Django executable: {DJANGO_EXECUTABLE}")
#
#     if not os.path.exists(DJANGO_EXECUTABLE):
#         logger.error(f"Django executable not found at: {DJANGO_EXECUTABLE}")
#         return None
#         if sys.platform == 'win32':
#             process = subprocess.Popen(
#                 [DJANGO_EXECUTABLE],
#                 stdout=log_file,
#                 #stdout=subprocess.PIPE,
#                 stderr=subprocess.STDOUT,
#                 text=True,
#                 creationflags=subprocess.CREATE_NO_WINDOW
#         )
#         else:
#             process = subprocess.Popen(
#                 [DJANGO_EXECUTABLE],
#                 stdout=log_file,
#                 #stdout=subprocess.PIPE,
#                 stderr=subprocess.STDOUT,
#                 text=True
#         )

#to find the error while executing the application
def run_django_backend():
    logger.info("Starting Django backend...")
    logger.info(f"Attempting to run Django executable: {DJANGO_EXECUTABLE}")

    if not os.path.exists(DJANGO_EXECUTABLE):
        logger.error(f"Django executable not found at: {DJANGO_EXECUTABLE}")
        return None

    with open(SERVER_LOG_FILE, 'w') as log_file:
        try:
            if sys.platform == 'win32':
                process = subprocess.Popen(
                    [DJANGO_EXECUTABLE],
                    stdout=log_file,
                    stderr=subprocess.STDOUT,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                process = subprocess.Popen(
                    [DJANGO_EXECUTABLE],
                    stdout=log_file,
                    stderr=subprocess.STDOUT,
                    text=True
                )
            return process
        except FileNotFoundError:
            logger.error(f"Failed to start Django backend. Executable not found: {DJANGO_EXECUTABLE}")
            return None
        except Exception as e:
            logger.error(f"Failed to start Django backend. Error: {str(e)}")
            return None
def check_django_ready(process):
    with open(SERVER_LOG_FILE, 'r') as log_file:
        while True:
            line = log_file.readline()
            if not line:
                time.sleep(0.1)  # Wait a bit before reading again
                continue
            if READY_MESSAGE in line:
                return True
        if process.poll() is not None:
            logger.error("Django process terminated unexpectedly")
            return False

def run_react_frontend():
    logger.info("Starting React frontend...")
    if sys.platform == 'win32':
        process = subprocess.Popen([REACT_EXECUTABLE], creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        process = subprocess.Popen([REACT_EXECUTABLE])
    return process

def terminate_process_tree(pid):
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        for child in children:
            child.terminate()
        parent.terminate()
        logger.info(f"Terminated process tree with root PID: {pid}")
    except psutil.NoSuchProcess:
        logger.warning(f"Process with PID {pid} not found (might have already terminated)")

# Main execution
if __name__ == "__main__":
    logger.info("Application starting...")

    # Check if executables exist
    if not os.path.exists(DJANGO_EXECUTABLE):
        logger.error(f"Django executable not found at: {DJANGO_EXECUTABLE}")
        sys.exit(1)

    if not os.path.exists(REACT_EXECUTABLE):
        logger.error(f"React executable not found at: {REACT_EXECUTABLE}")
        sys.exit(1)

    # Start Django backend
    django_process = run_django_backend()

    # Wait for Django to be ready
    if check_django_ready(django_process):
        logger.info("Django backend is ready")

        # Start React frontend
        react_process = run_react_frontend()

        logger.info("React frontend started. Waiting for it to close...")

        # Wait for React process to finish
        react_process.wait()

        logger.info("React frontend closed. Terminating all processes...")

        # Terminate Django process
        terminate_process_tree(django_process.pid)

        logger.info("All processes terminated. Application shutting down.")
    else:
        logger.error("Failed to start Django backend. Application shutting down.")

    logging.shutdown()
