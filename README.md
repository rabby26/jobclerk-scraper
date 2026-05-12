# JobClerk Auto-Scraper & Email Notifier

This repository contains an automated scraper that runs on GitHub Actions. It monitors [JobClerk.com](https://jobclerk.com) every 30 minutes from **7 PM to 11 PM Bangladesh Time** (UTC+6) for new "Medical doctor" (junior grade) jobs. If a new job is found, it sends an email notification.

## Features
- **No dependencies required**: Uses pure Python standard libraries (no need for `requests` or `BeautifulSoup`).
- **Serverless Automation**: Runs entirely via GitHub Actions.
- **State Persistence**: Remembers previously seen jobs by committing to a `seen_jobs.json` file so you don't get duplicate emails.
- **Automated Notifications**: Uses your Gmail account to send you an email.

## How to Set It Up

### Step 1: Push this code to GitHub
If you haven't already, initialize a git repository and push these files to a public or private repository on your GitHub account.

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 2: Allow GitHub Actions to commit changes
Since the script needs to remember which jobs it has already seen, it commits changes back to the repository.
1. Go to your GitHub repository in your browser.
2. Click on **Settings** > **Actions** > **General**.
3. Scroll down to **Workflow permissions**.
4. Select **Read and write permissions** and check **"Allow GitHub Actions to create and approve pull requests"**.
5. Click **Save**.

### Step 3: Create an App Password for your Gmail
To send emails, the script needs an App Password from your Gmail account (your regular password won't work for security reasons).
1. Go to your Google Account > **Security**.
2. Make sure **2-Step Verification** is enabled.
3. Search for **App passwords** in the top search bar (or find it under the 2-Step Verification section).
4. Create a new App password for "Mail" and select "Other (Custom name)" as the device. Name it "GitHub Actions".
5. Copy the generated 16-character password. Keep it secure.

### Step 4: Add GitHub Secrets
You need to provide your email credentials to GitHub Actions securely.
1. Go to your GitHub repository > **Settings** > **Secrets and variables** > **Actions**.
2. Click **New repository secret** and add the following three secrets:
   - **`SENDER_EMAIL`**: Your full Gmail address (e.g., `youremail@gmail.com`)
   - **`SENDER_PASSWORD`**: The 16-character App password you generated in Step 3.
   - **`RECEIVER_EMAIL`**: The email address where you want to receive the notifications (can be the same as your SENDER_EMAIL).

### Step 5: Test it Manually
You can test the scraper immediately to see if it works:
1. Go to the **Actions** tab in your GitHub repository.
2. Click on **JobClerk Scraper** on the left sidebar.
3. Click the **Run workflow** dropdown on the right side and click the green **Run workflow** button.
4. Wait a minute for it to finish. If everything is configured correctly, it will fetch the jobs, and send you an email with the currently available jobs.

After this initial run, it will automatically run on the predefined schedule!
