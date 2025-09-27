# logger.py
import datetime

class Logger:
    @staticmethod
    def log(message: str):
        """Prints a structured log with timestamp."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
