import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import decode_header
import threading
import time

# Email configuration (replace with your credentials)
EMAIL_ADDRESS = "wunder736@gmail.com"
EMAIL_PASSWORD = "ggqk hxlv eixv qnye"  # Use an app-specific password for Gmail
SMTP_SERVER = "smtp.gmail.com"
IMAP_SERVER = "imap.gmail.com"

# Function to send emails with attachments, CC, and BCC
def send_email(subject, body, to_email, cc=None, bcc=None, attachments=None):
    try:
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email

        # Add CC and BCC if provided
        if cc:
            msg['Cc'] = cc
        if bcc:
            msg['Bcc'] = bcc

        msg.attach(MIMEText(body, 'plain'))

        if attachments:
            for file_path in attachments:
                with open(file_path, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={file_path.split("/")[-1]}'
                )
                msg.attach(part)

        # Combine To, CC, and BCC recipients
        recipients = [to_email]
        if cc:
            recipients.extend(cc.split(','))  # Split CC recipients by comma
        if bcc:
            recipients.extend(bcc.split(','))  # Split BCC recipients by comma

        with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipients, msg.as_string())
        messagebox.showinfo("Success", "Email sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {e}")

# Function to fetch emails
def fetch_emails(limit=5, search_query=None):
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select('inbox')

        # Sanitize the search query
        if search_query:
            search_query = search_query.replace('"', '\\"')  # Escape double quotes
            search_query = search_query.replace("'", "\\'")  # Escape single quotes
            search_criteria = f'(OR SUBJECT "{search_query}" FROM "{search_query}")'
        else:
            search_criteria = 'ALL'  # Fetch all emails if no search query is provided

        # Perform the search
        status, messages = mail.search(None, search_criteria)
        if status != 'OK':
            raise Exception("Failed to search emails.")

        email_ids = messages[0].split()[-limit:]  # Fetch the latest `limit` emails

        emails = []
        for email_id in email_ids:
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg['Subject'])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or 'utf-8')
                    from_ = msg['From']
                    body = ""

                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type == 'text/plain':
                                body = part.get_payload(decode=True).decode()
                    else:
                        body = msg.get_payload(decode=True).decode()

                    emails.append({
                        'subject': subject,
                        'from': from_,
                        'body': body
                    })
        return emails
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch emails: {e}")
        return []

# Function to check for new emails and notify
def check_for_new_emails():
    last_count = 0
    while True:
        emails = fetch_emails()
        current_count = len(emails)
        if current_count > last_count:
            messagebox.showinfo("New Email", f"You have {current_count - last_count} new email(s)!")
        last_count = current_count
        time.sleep(60)  # Check every 60 seconds

# Function to open the "Send Email" window
def open_send_email_window():
    send_window = tk.Toplevel(root)
    send_window.title("Send Email")

    # To field
    tk.Label(send_window, text="To:").grid(row=0, column=0, padx=10, pady=10)
    to_entry = tk.Entry(send_window, width=50)
    to_entry.grid(row=0, column=1, padx=10, pady=10)

    # CC field
    tk.Label(send_window, text="CC:").grid(row=1, column=0, padx=10, pady=10)
    cc_entry = tk.Entry(send_window, width=50)
    cc_entry.grid(row=1, column=1, padx=10, pady=10)

    # BCC field
    tk.Label(send_window, text="BCC:").grid(row=2, column=0, padx=10, pady=10)
    bcc_entry = tk.Entry(send_window, width=50)
    bcc_entry.grid(row=2, column=1, padx=10, pady=10)

    # Subject field
    tk.Label(send_window, text="Subject:").grid(row=3, column=0, padx=10, pady=10)
    subject_entry = tk.Entry(send_window, width=50)
    subject_entry.grid(row=3, column=1, padx=10, pady=10)

    # Body field
    tk.Label(send_window, text="Body:").grid(row=4, column=0, padx=10, pady=10)
    body_text = scrolledtext.ScrolledText(send_window, width=50, height=10)
    body_text.grid(row=4, column=1, padx=10, pady=10)

    # Attachments
    attachments = []

    def add_attachment():
        file_path = filedialog.askopenfilename()
        if file_path:
            attachments.append(file_path)
            tk.Label(send_window, text=f"Attached: {file_path.split('/')[-1]}").grid(row=6, column=1, padx=10, pady=5, sticky='w')

    # Send button
    def on_send():
        to_email = to_entry.get()
        cc = cc_entry.get()
        bcc = bcc_entry.get()
        subject = subject_entry.get()
        body = body_text.get("1.0", tk.END)
        send_email(subject, body, to_email, cc, bcc, attachments)
        send_window.destroy()

    # Add Attachment button
    tk.Button(send_window, text="Add Attachment", command=add_attachment).grid(row=5, column=1, pady=10)

    # Send button
    tk.Button(send_window, text="Send", command=on_send).grid(row=7, column=1, pady=10)

# Function to open the "Check Emails" window
def open_check_emails_window():
    search_query = search_entry.get()
    emails = fetch_emails(limit=5, search_query=search_query)
    if not emails:
        messagebox.showinfo("No Emails", "No emails found.")
        return

    check_window = tk.Toplevel(root)
    check_window.title("Check Emails")

    for i, email in enumerate(emails):
        tk.Label(check_window, text=f"From: {email['from']}", font=('Arial', 10, 'bold')).grid(row=i, column=0, padx=10, pady=5, sticky='w')
        tk.Label(check_window, text=f"Subject: {email['subject']}", font=('Arial', 10)).grid(row=i, column=1, padx=10, pady=5, sticky='w')
        tk.Label(check_window, text=f"Body: {email['body'][:100]}...", font=('Arial', 10)).grid(row=i, column=2, padx=10, pady=5, sticky='w')

# Main Tkinter application
root = tk.Tk()
root.title("Staplr - Email Extension")

# Search bar
search_entry = tk.Entry(root, width=50)
search_entry.pack(pady=10)

# Buttons for email features
tk.Button(root, text="Send Email", command=open_send_email_window, width=20, height=2).pack(pady=10)
tk.Button(root, text="Check Emails", command=open_check_emails_window, width=20, height=2).pack(pady=10)

# Start email notification thread
threading.Thread(target=check_for_new_emails, daemon=True).start()

# Run the application
root.mainloop()