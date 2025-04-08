import time

def log_error(message, log_file="error_log.txt"):
    """Log error messages with a timestamp."""
    with open(log_file, "a") as f:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")
