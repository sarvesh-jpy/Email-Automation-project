import json
import os

DEFAULT_CONTACTS = [
    {
        "recipient_name": "Priya Sharma",
        "recipient_email": "priya@example.com",
        "company": "Acme AI",
        "role": "Backend Engineering Intern",
        "job_url": "https://example.com/job",
        "personalization_note": "I saw that Acme AI recently launched a new workflow automation feature.",
        "candidate_name": "Alex Mercer",
        "candidate_background": "Python developer passionate about constructing CLI automation agents",
        "portfolio_url": "https://github.com/alex-mercer"
    },
    {
        "recipient_name": "Marcus Vance",
        "recipient_email": "marcus@innovate.io",
        "company": "Innovate IO",
        "role": "Junior Software Engineer",
        "job_url": "https://innovate.io/careers",
        "personalization_note": "Your technical blog post on building scalable microservices was highly informative.",
        "candidate_name": "Alex Mercer",
        "candidate_background": "backend coder who enjoys optimization and system design",
        "portfolio_url": "https://github.com/alex-mercer"
    },
    {
        "recipient_name": "Sarah Connor",
        "recipient_email": "sarah.c@cyberdyne.tech",
        "company": "Cyberdyne Systems",
        "role": "AI Integrations Engineer",
        "job_url": "",
        "personalization_note": "Your recent funding round for autonomous agents is incredibly exciting.",
        "candidate_name": "Alex Mercer",
        "candidate_background": "Python automation specialist focused on agentic frameworks",
        "portfolio_url": "https://github.com/alex-mercer"
    }
]

def load_contacts(filepath="contacts.json"):
    """
    Loads outreach contacts from contacts.json.
    Falls back to a default list if the file is missing or corrupted.
    """
    if not os.path.exists(filepath):
        print(f"[*] Contacts file '{filepath}' not found. Loading default demonstration contacts.")
        return DEFAULT_CONTACTS
        
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                print(f"[!] Warning: '{filepath}' should be a JSON list. Loading defaults.")
                return DEFAULT_CONTACTS
            return data
    except Exception as e:
        print(f"[!] Warning: Error reading '{filepath}': {e}. Loading defaults.")
        return DEFAULT_CONTACTS
