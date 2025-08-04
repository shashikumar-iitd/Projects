from datetime import datetime

def log_message(message):
    """Appends a message with timestamp to the application log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("application.log", "a") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")

def format_text(text):
    """Strips and replaces newlines with spaces in the given text."""
    return text.strip().replace('\n', ' ')

def read_file(file_path):
    """Reads and returns the content of a file."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        log_message(f"Error reading {file_path}: {e}")
        return None

def write_file(file_path, content):
    """Writes content to a file."""
    try:
        with open(file_path, 'w') as file:
            file.write(content)
    except Exception as e:
        log_message(f"Error writing to {file_path}: {e}")