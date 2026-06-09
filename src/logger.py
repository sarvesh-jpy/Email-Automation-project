import csv
import os
from datetime import datetime

LOG_FILE = "outreach_log.csv"

def log_outreach(recipient_email: str, company: str, role: str, subject: str, status: str, error_message: str = ""):
    """
    Appends an entry to the outreach_log.csv audit file. Creates the file with headers if missing.
    """
    file_exists = os.path.exists(LOG_FILE)
    
    headers = ["timestamp", "recipient_email", "company", "role", "subject", "status", "error_message"]
    
    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "recipient_email": recipient_email,
        "company": company,
        "role": role,
        "subject": subject,
        "status": status,
        "error_message": error_message
    }
    
    try:
        # Open in append mode with UTF-8 encoding
        with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)
    except Exception as e:
        print(f"[!] Error writing to log file: {e}")
