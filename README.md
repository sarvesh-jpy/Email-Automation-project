 What We Built For You
We built "The Closer", a modular Python bot that personalizes and drafts/sends cold emails. It is structured into separate components:

Configuration: The 

.env
 file holds your private credentials (Groq API key, Gmail address, App Password, and Name). The settings module 

config.py
 securely loads and validates these settings.
Lead Storage: Your outreach targets are stored in a simple JSON file: 

contacts.json
. The loader module 

data_loader.py
 automatically reads this list.
AI Writing Engine: The generator 

email_generator.py
 connects to the Groq API and uses the llama-3.1-8b-instant model to generate highly personalized subject lines and bodies under 150 words based on the target company and role. If the API is offline, it safely falls back to a clean local string template.
Email Client: The sender module 

email_sender.py
 handles communication with Gmail. It can securely connect to Gmail to add drafts to your Drafts folder (via IMAP) or send emails directly (via SMTP).
Audit Trail: The logging module 

logger.py
 records the date, target, subject, and delivery status of every email in a local database file: 

outreach_log.csv
.
Orchestrator: 

main.py
 runs the CLI interface, previewing each AI-generated email for you and letting you decide what action to take.
2. How to Automate & Run the Project
Step 1: Update Your Contacts
Whenever you find new jobs or companies to contact, open 

contacts.json
 and add their details. Make sure you fill in:

recipient_name and recipient_email
company and role
personalization_note (e.g. a recent company news item, product release, or detail that caught your eye).
candidate_name, candidate_background, and portfolio_url (your own details).
Step 2: Run the Bot
Open your terminal inside the d:\programs\email project directory and execute:

bash
python main.py
Step 3: Review & Process
For each target, the bot will show you a preview of the email body and subject line written by the AI, then wait for your command:

Type d to automatically save it as a draft in your Gmail. (This is the recommended way, letting you do a final check in Gmail before hitting send).
Type s to send it instantly.
Type k to skip the contact.
Type q to quit the loop.
Step 4: Verify Logs
Open 

outreach_log.csv
 at any time to see a history of all sent, drafted, or skipped outreach attempts.
