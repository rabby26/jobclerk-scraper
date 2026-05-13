import urllib.request
import re
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import sys

URL = "https://jobclerk.com/jobs?q=Medical+doctor&grade=junior"
SEEN_JOBS_FILE = "seen_jobs.json"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")

def fetch_jobs():
    req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            
            # The jobs array is located inside Next.js flight payload
            pattern = r'\\"jobs\\":(\[\{.*?\}\]),\\"jobs_count\\"'
            match = re.search(pattern, html)
            if match:
                raw = match.group(1)
                # Unescape quotes
                unescaped = raw.replace('\\"', '"').replace('\\\\', '\\')
                try:
                    jobs = json.loads(unescaped)
                    return jobs
                except Exception as e:
                    print("JSON decode error:", e)
                    return []
            else:
                print("Could not find jobs array in the HTML.")
                return []
    except Exception as e:
        print(f"Error fetching jobs: {e}")
        return []

def load_seen_jobs():
    if os.path.exists(SEEN_JOBS_FILE):
        with open(SEEN_JOBS_FILE, 'r') as f:
            try:
                return set(json.load(f))
            except Exception:
                return set()
    return set()

def save_seen_jobs(seen_jobs):
    with open(SEEN_JOBS_FILE, 'w') as f:
        json.dump(list(seen_jobs), f)

def send_email(new_jobs):
    if not SENDER_EMAIL or not SENDER_PASSWORD or not RECEIVER_EMAIL:
        print("Email credentials not set. Skipping email notification.")
        return

    # Split the comma-separated string into a list of emails
    receivers = [email.strip() for email in RECEIVER_EMAIL.split(',') if email.strip()]

    subject = f"JobClerk Alert: {len(new_jobs)} New Medical Doctor (Junior) Jobs!"
    
    html_content = "<h2>New Jobs Found on JobClerk</h2><ul>"
    for job in new_jobs:
        title = job.get('title', 'Unknown Title')
        employer = job.get('employerName', 'Unknown Employer')
        location = job.get('town', 'Unknown Location')
        salary = job.get('salary', 'Salary not specified')
        job_url = job.get('jobUrl', URL)
        
        html_content += f"<li><a href='{job_url}'><b>{title}</b></a> at {employer} ({location}) - {salary}</li><br>"
    html_content += "</ul>"

    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = ", ".join(receivers) # Display all receivers in the 'To' field

    part = MIMEText(html_content, "html")
    msg.attach(part)

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receivers, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    print("Fetching jobs...")
    jobs = fetch_jobs()
    if not jobs:
        print("No jobs found or failed to parse. Exiting.")
        sys.exit(0)
    
    seen_jobs = load_seen_jobs()
    new_jobs = []
    
    for job in jobs:
        title = job.get('title', '').strip()
        employer = job.get('employerName', '').strip()
        # Create a stable identifier based on title and employer
        stable_id = f"{title}::{employer}"
        
        if stable_id and stable_id not in seen_jobs:
            new_jobs.append(job)
            seen_jobs.add(stable_id)
            
    if new_jobs:
        print(f"Found {len(new_jobs)} new jobs!")
        send_email(new_jobs)
        save_seen_jobs(seen_jobs)
        print("State updated.")
    else:
        print("No new jobs found.")

if __name__ == "__main__":
    main()
