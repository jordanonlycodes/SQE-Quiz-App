import logging
import os
import sys
from datetime import datetime

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont

from modules.gui import MainWindow

logger = logging.getLogger(__name__)

def set_current_working_directory() -> None:
    # Set CWD to project root, so that relative paths work correctly
    os.chdir(os.path.dirname(__file__))

def cleanup_old_log_files(log_dir: str, keep: int = 3) -> None:
    """Remove old log files."""
    log_files = []

    for file_name in os.listdir(log_dir):
        file_path = os.path.join(log_dir, file_name)
        if (
            os.path.isfile(file_path)
            and file_name.startswith("quiz-app")
            and ".log" in file_name
        ):
            log_files.append(file_path)

    # Sort files in log_files by modification time
    log_files.sort(key=os.path.getmtime, reverse=True)

    for old_log_file in log_files[keep:]:
        try:
            os.remove(old_log_file)
            logger.info("Removed old log file: %s.", old_log_file)
        except OSError as error:
            logger.warning("Could not remove old log file %s. Error: %s", old_log_file, error)

def configure_logging() -> None:
    """
    Configure console and file logging. Log file is set to DEBUG level. 
    Console application logging level control from QUIZ_APP_LOG_LEVEL 
    environment variable.
    """
    # Load env var QUIZ_APP_LOG_LEVEL if exists, if not use INFO
    console_log_level = os.getenv("QUIZ_APP_LOG_LEVEL", "INFO").upper()
    # Checks if set attribute in console_log_level is present in logging module
    # If it is, assign it to console_level, if it's not return logging.INFO attribute
    console_level = getattr(logging, console_log_level, logging.INFO)
    
    log_dir = "logs"
    # If dir exist don't raise error - exist_ok=True
    os.makedirs(log_dir, exist_ok=True)

    session_timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    log_file = os.path.join(log_dir, f"quiz-app-{session_timestamp}.log")

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    # StreamHanlder send logs to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(
        log_file,
        mode="w",
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Logs are sent to console and saved in logs dir
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[console_handler, file_handler],
        force=True,
    )

    cleanup_old_log_files(log_dir)
    logger.debug("Logging configured. Session log file: %s", os.path.abspath(log_file))

def main() -> None:
    """Start Qt based application."""
    set_current_working_directory()
    configure_logging()
    logger.debug("Set CWD to %s", os.getcwd())
    
    logger.info("Starting Quiz-App")
    app = QApplication(sys.argv)

    # Set global font
    font = QFont("Inter", 12)
    app.setFont(font)

    # Load and apply styles from styles.css to the entire application
    stylesheet_path = "modules/gui/styles/styles.css"
    with open(stylesheet_path, "r", encoding="utf-8") as file:
        app.setStyleSheet(file.read())
    logger.debug("App stylesheet loaded from: %s", stylesheet_path)

    # Create and show main window
    window = MainWindow()
    window.show()
    exit_code = app.exec()
    logger.info("Quiz-App exited with code %s.", exit_code)
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
