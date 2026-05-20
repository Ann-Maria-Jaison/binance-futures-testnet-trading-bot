import os
import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logging(log_file_path: str = "logs/trading.log") -> logging.Logger:
    """
    Configures application-wide logging to log to both a rotating file and the standard output.
    Automatically creates the logging directory if it does not exist.
    
    Args:
        log_file_path (str): Relative or absolute path to the log file.
        
    Returns:
        logging.Logger: The configured root logger instance.
    """
    # Extract directory from log file path and ensure it exists
    log_dir = os.path.dirname(log_file_path)
    if log_dir and not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir, exist_ok=True)
        except Exception as e:
            # Fallback to current directory if logs/ cannot be created
            print(f"Warning: Could not create log directory '{log_dir}' due to: {e}. Logging to current directory.", file=sys.stderr)
            log_file_path = "trading.log"

    # Define a clean, professional, and easy-to-read log format
    log_format = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Remove existing handlers to avoid duplicate log entries if called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    # 1. File Handler (Rotating log file: max 5MB per file, keeping up to 3 backups)
    try:
        file_handler = RotatingFileHandler(
            filename=log_file_path,
            maxBytes=5 * 1024 * 1024,  # 5 Megabytes
            backupCount=3,
            encoding="utf-8"
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Error: Failed to set up file logging: {e}", file=sys.stderr)

    # 2. Console Handler (Standard Output)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    # Return logger for convenience
    return logger
