# Outline: Sprint 3 — The Closer (Cold Email Writer + Send Bot)

This document provides a high-level outline of the problem statement and project requirements for building "The Closer".

## 1. Project Context & Objectives
- **Target:** Sprint 3 project to build a cold email writer and sending agent ("The Closer").
- **Core Micro-skills:**
  - Connecting code to email services (Gmail API/SMTP).
  - Understanding/applying cold outreach best practices.
  - Sending programmatic, personalized emails.
- **Goal:** Build a simple, explainable agent to generate and draft/send personalized emails for job postings.

## 2. Core Problem & Target Audience
- **Problem:** Job seekers struggle with outreach personalization at scale. Generic emails fail, while manual custom writing is too slow.
- **Audience:** Job seekers reaching out to recruiters, founders, or hiring managers.
- **Constraints:** Maximize personalization, mandate human review, and prevent spamming.

## 3. Workflow & Technical Requirements
- **Workflow Pipeline:**
  `Input Data` → `Personalization Hook Extraction` → `Email Generation` → `Human Review (Confirmation)` → `Draft/Send` → `Proof Log`
- **Data Inputs (Core Fields):**
  - Recipient email, Company name, Role title, Candidate name, and Candidate background.
- **Data Outputs:**
  - Subject line, email body, status (drafted/sent), and a local audit log entry in `outreach_log.csv`.

## 4. Cold Email Structure Rules
- **Length:** Under 150 words.
- **Sections:**
  1. Short, specific subject line.
  2. One-sentence personalization hook.
  3. Brief relevant intro.
  4. 1-2 line value statement linking background to the role.
  5. One clear, easy Call-To-Action (ask).
  6. Sign-off with portfolio/resume links.

## 5. Functional Requirements (FRs)
- **FR1 (Data loading):** Load target contacts from Python lists, `contacts.json`, or `jobs.csv`.
- **FR2 (Generation):** Template-based or LLM-driven personalized email generation.
- **FR3 (Preview & Confirmation):** Terminal/UI approval step before drafting/sending.
- **FR4 (Delivery):** Supports Draft mode (recommended) or Send mode (SMTP, Gmail API, SendGrid, Resend).
- **FR5 (Logging):** Write logs (timestamps, details, delivery status) to `outreach_log.csv`.

## 6. Safety & Ethics Guidelines
- Mandatory human review (no automated bulk-sending).
- Low volume targets.
- Authentic representation (no fake claims, must use own identity).
- Opt-out compliance.

## 7. Recommended Stack & Structure
- **Languages/Tools:** Python 3, `smtplib` or Gmail API, `.env` for secrets, CSV/JSON storage.
- **Folder Structure:**
  ```text
  the-closer/
  ├── main.py
  ├── email_generator.py
  ├── email_sender.py
  ├── logger.py
  ├── contacts.json
  ├── outreach_log.csv
  ├── .env.example
  ├── requirements.txt
  └── README.md
  ```

## 8. MVP Scope & Demo Steps
- **MVP Features:** Load 3-5 targets, generate templates, preview/confirm, send or draft, and log the outcome.
- **Demo Flow:** Step-by-step guidance from creating sample data to testing dry-run mode and finally confirming in Gmail's Sent/Drafts folders.
