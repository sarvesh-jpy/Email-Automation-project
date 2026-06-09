import sys
from src.config import Settings
from src.data_loader import load_contacts
from src.email_generator import generate_email
from src.email_sender import send_email, create_draft
from src.logger import log_outreach

def run_cli():
    print("=" * 60)
    print(" " * 18 + "THE CLOSER: OUTREACH BOT")
    print("=" * 60)
    
    if Settings.DRY_RUN:
        print("[NOTICE] DRY_RUN is enabled. Emails and drafts will only be simulated.")
        print("         To enable live delivery, set DRY_RUN=false in your .env file.")
        print("-" * 60)
        
    # Load targets
    contacts = load_contacts("contacts.json")
    total_contacts = len(contacts)
    print(f"[*] Loaded {total_contacts} outreach target(s).\n")
    
    stats = {"sent": 0, "drafted": 0, "skipped": 0, "failed": 0}
    
    for index, contact in enumerate(contacts, start=1):
        email_address = contact.get("recipient_email", "")
        company = contact.get("company", "Unknown Company")
        role = contact.get("role", "Unknown Role")
        
        if not email_address:
            print(f"[!] Target #{index} has no email address. Skipping.")
            log_outreach("", company, role, "", "failed", "Missing recipient email address")
            stats["failed"] += 1
            continue
            
        # Generate email
        subject, body = generate_email(contact)
        word_count = len(body.split())
        
        print("\n" + "=" * 50)
        print(f" Target #{index} of {total_contacts}")
        print(f" Recipient: {contact.get('recipient_name', 'Team')} <{email_address}>")
        print(f" Company  : {company} | Role: {role}")
        print("-" * 50)
        print(f" Subject  : {subject}")
        print(f" Body ({word_count} words):")
        print("-" * 50)
        print(body)
        print("=" * 50)
        
        # User confirmation loop
        while True:
            choice = input("\nAction -> [s]end email | [d]raft email | [k]ip target | [q]uit outreach: ").strip().lower()
            
            if choice == 'q':
                print("\n[*] Exiting outreach loop. Goodbye!")
                return
            elif choice == 'k':
                print("[*] Target skipped.")
                log_outreach(email_address, company, role, subject, "skipped")
                stats["skipped"] += 1
                break
            elif choice == 's':
                print("[*] Sending email...")
                success, status, error_msg = send_email(email_address, subject, body)
                if success:
                    print(f"[+] Success: Email {status}!")
                    log_outreach(email_address, company, role, subject, status)
                    stats["sent"] += 1
                else:
                    print(f"[x] Failed to send email: {error_msg}")
                    log_outreach(email_address, company, role, subject, "failed", error_msg)
                    stats["failed"] += 1
                break
            elif choice == 'd':
                print("[*] Creating draft...")
                success, status, error_msg = create_draft(email_address, subject, body)
                if success:
                    print(f"[+] Success: Email {status}!")
                    log_outreach(email_address, company, role, subject, status)
                    stats["drafted"] += 1
                else:
                    print(f"[x] Failed to create draft: {error_msg}")
                    log_outreach(email_address, company, role, subject, "failed", error_msg)
                    stats["failed"] += 1
                break
            else:
                print("[!] Invalid option. Please enter 's', 'd', 'k', or 'q'.")
                
    # Final summary reports
    print("\n" + "=" * 60)
    print(" " * 22 + "OUTREACH SUMMARY")
    print("=" * 60)
    print(f"  Sent: {stats['sent']} | Drafted: {stats['drafted']} | Skipped: {stats['skipped']} | Failed: {stats['failed']}")
    print(f"  All logs written to 'outreach_log.csv'.")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    try:
        run_cli()
    except KeyboardInterrupt:
        print("\n\n[!] Script interrupted by user. Exiting.")
        sys.exit(0)
