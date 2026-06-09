import smtplib
import imaplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.config import Settings

def send_email(to_email: str, subject: str, body: str) -> tuple[bool, str, str]:
    """
    Sends an email over SMTP or simulates it if DRY_RUN is active.
    
    Returns:
        tuple: (success: bool, status: str, error_message: str)
    """
    if Settings.DRY_RUN:
        return True, "sent (dry run)", ""
        
    try:
        # Validate settings
        Settings.validate()
        
        # Prepare MIME Message
        msg = MIMEMultipart()
        msg["From"] = f"{Settings.SENDER_NAME} <{Settings.SMTP_USER}>"
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))
        
        # Establish SMTP Connection
        server = smtplib.SMTP(Settings.SMTP_HOST, Settings.SMTP_PORT, timeout=10)
        server.ehlo()
        
        # Enable STARTTLS if port is 587
        if Settings.SMTP_PORT == 587:
            server.starttls()
            server.ehlo()
            
        server.login(Settings.SMTP_USER, Settings.SMTP_PASSWORD)
        server.sendmail(Settings.SMTP_USER, to_email, msg.as_string())
        server.quit()
        return True, "sent", ""
    except Exception as e:
        return False, "failed", str(e)

def create_draft(to_email: str, subject: str, body: str) -> tuple[bool, str, str]:
    """
    Creates a draft in the user's IMAP Drafts folder or simulates it if DRY_RUN is active.
    
    Returns:
        tuple: (success: bool, status: str, error_message: str)
    """
    if Settings.DRY_RUN:
        return True, "drafted (dry run)", ""
        
    try:
        # Validate settings
        Settings.validate()
        
        # Prepare MIME Message
        msg = MIMEMultipart()
        msg["From"] = f"{Settings.SENDER_NAME} <{Settings.SMTP_USER}>"
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))
        
        # Determine IMAP server host based on SMTP server (SMTP -> IMAP conversion helper)
        imap_host = "imap.gmail.com"
        if "gmail" not in Settings.SMTP_HOST.lower():
            # Guess alternative IMAP hosts (e.g. mail.example.com, imap.example.com)
            imap_host = Settings.SMTP_HOST.replace("smtp", "imap").replace("mail", "imap")
            
        # Connect to IMAP
        imap = imaplib.IMAP4_SSL(imap_host, timeout=10)
        imap.login(Settings.SMTP_USER, Settings.SMTP_PASSWORD)
        
        # Scan folder list to identify Drafts folder name (e.g., "[Gmail]/Drafts" or "Drafts")
        drafts_folder = "Drafts"
        status, folders = imap.list()
        if status == "OK":
            for folder in folders:
                folder_str = folder.decode("utf-8")
                if "draft" in folder_str.lower():
                    # Parse double quotes to find exact path
                    parts = folder_str.split('"')
                    if len(parts) >= 5:
                        drafts_folder = parts[-2]
                        break
        
        # Append email as raw message to drafts folder
        imap.append(drafts_folder, '', imaplib.Time2Internaldate(time.time()), msg.as_bytes())
        imap.logout()
        return True, "drafted", ""
    except Exception as e:
        return False, "failed", str(e)
