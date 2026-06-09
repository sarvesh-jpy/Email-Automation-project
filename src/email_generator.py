import urllib.request
import json
from src.config import Settings

def _generate_template_email(contact: dict) -> tuple[str, str]:
    """
    Standard template fallback if Groq API key is missing or fails.
    """
    recipient_name = contact.get("recipient_name", "Team")
    company = contact.get("company", "your team")
    role = contact.get("role", "Open Role")
    personalization_note = contact.get("personalization_note", "")
    candidate_name = contact.get("candidate_name", "Candidate")
    candidate_background = contact.get("candidate_background", "software developer")
    portfolio_url = contact.get("portfolio_url", "")
    
    # 1. Subject Line
    subject = f"Outreach: {role} role at {company}"
    
    # 2. Personalization Hook
    hook_sentence = f"I noticed {company} is looking for a {role}. {personalization_note}" if personalization_note else f"I noticed {company} is hiring for a {role}."
    
    # 3. Body Construction
    body = f"Hi {recipient_name},\n\n"
    body += f"{hook_sentence}\n\n"
    body += f"I'm {candidate_name}, and I have been building projects around {candidate_background}.\n"
    body += f"This role caught my eye because my experience aligns well with the skills needed to make an impact on your engineering goals.\n\n"
    body += f"Would you be open to a brief chat, or could you point me to the right person on the team?\n\n"
    body += f"Best regards,\n"
    body += f"{candidate_name}"
    
    if portfolio_url:
        body += f"\n{portfolio_url}"
        
    return subject, body

def generate_email(contact: dict) -> tuple[str, str]:
    """
    Generates a personalized cold email. Uses the Groq API if a key is available,
    falling back to a local string template on error or missing key.
    
    Returns:
        tuple: (subject, body)
    """
    if not Settings.GROQ_API_KEY:
        return _generate_template_email(contact)
        
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {Settings.GROQ_API_KEY}",
        "User-Agent": "Mozilla/5.0"
    }
    
    prompt = f"""
    Write a personalized, professional cold email outreach for:
    Recipient Name: {contact.get('recipient_name', 'Hiring Manager')}
    Recipient Email: {contact.get('recipient_email', '')}
    Target Company: {contact.get('company', 'your team')}
    Target Role: {contact.get('role', 'Open Role')}
    Personalization Context: {contact.get('personalization_note', '')}
    Sender Name: {contact.get('candidate_name', 'Candidate')}
    Sender Background: {contact.get('candidate_background', 'software developer')}
    Sender Portfolio/GitHub URL: {contact.get('portfolio_url', '')}
    
    Constraints:
    1. The body MUST be under 150 words.
    2. Professional, conversational, and personalized.
    3. Exactly one call-to-action (ask for brief chat or pointing to the right person).
    4. Free of fake claims or generic fluff.
    5. Output must be a valid JSON object with the keys "subject" and "body".
    """
    
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": "You are a professional outreach generator. You must respond ONLY with a raw JSON object containing the keys 'subject' and 'body'. Do not output any preamble, markdown formatting (do not wrap in ```json), or trailing text."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "response_format": {"type": "json_object"}
    }
    
    try:
        req = urllib.request.Request(
            url, 
            data=json.dumps(data).encode("utf-8"), 
            headers=headers, 
            method="POST"
        )
        
        # Request with a 10s timeout
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            content = res_data["choices"][0]["message"]["content"]
            parsed = json.loads(content)
            subject = parsed.get("subject", f"Outreach: {contact.get('role')} role at {contact.get('company')}")
            body = parsed.get("body", "")
            
            if body:
                # Word count validation constraint check
                word_count = len(body.split())
                if word_count > 150:
                    print(f"[!] Warning: Groq generated email is {word_count} words (Limit: 150).")
                return subject, body
    except Exception as e:
        print(f"[!] Warning: Groq API request failed ({e}). Falling back to local template.")
        
    return _generate_template_email(contact)
