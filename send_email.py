import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Thread

# Load SMTP configuration
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

smtp_server = config['smtp_server']
smtp_port = config['smtp_port']
smtp_username = config['smtp_username']
smtp_password = config['smtp_password']
from_email = config['from_email']
subject = config['subject']
body = config['body']

# Load recipients
with open('recipients.txt', 'r') as recipients_file:
    recipients = [line.strip() for line in recipients_file]

# Function to send an email
def send_email(recipient):
    try:
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        
        # Manually handle the recipient and print response
        server.mail(from_email)
        code, response = server.rcpt(recipient)
        
        print(f'Response from RCPT TO command for {recipient}: Code {code}, Response {response.decode()}')
        
        if code != 250:
            print(f'Failed to send email to {recipient}: {response.decode()}')
            server.quit()
            return
        
        code, response = server.data(msg.as_string())
        
        print(f'Response from DATA command for {recipient}: Code {code}, Response {response.decode()}')
        
        if code != 250:
            print(f'Failed to send email to {recipient}: {response.decode()}')
        else:
            # Extract and print Message ID if available
            message_id = response.decode().split(' ')[1] if ' ' in response.decode() else 'Not Provided'
            print(f'Successfully sent email to {recipient}. Message ID: {message_id}')
        
        # Close the server connection
        server.quit()
        
    except smtplib.SMTPRecipientsRefused as e:
        print(f'SMTPRecipientsRefused: {e.recipients}. Recipient(s): {recipient}')
    except smtplib.SMTPHeloError as e:
        print(f'SMTPHeloError: {e}. Error details: {e.strerror}')
    except smtplib.SMTPSenderRefused as e:
        print(f'SMTPSenderRefused: {e.sender}. Error details: {e.strerror}')
    except smtplib.SMTPDataError as e:
        print(f'SMTPDataError: {e.smtp_code}, {e.smtp_error}. Response: {response.decode()}')
    except smtplib.SMTPException as e:
        print(f'SMTPException: {e}. Error details: {e.strerror}')
    except Exception as e:
        print(f'Failed to send email to {recipient}. Exception: {e}')

# Create and start threads
threads = []
for recipient in recipients:
    thread = Thread(target=send_email, args=(recipient,))
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for thread in threads:
    thread.join()
