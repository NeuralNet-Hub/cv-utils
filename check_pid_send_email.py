"""
This code send an email in case some PID are not running in the instance
python check_pid_send_email.py --pids 1

"""




import argparse
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
import email.utils
import psutil
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('check_pid_send_email.log'),
        logging.StreamHandler(sys.stdout)
    ]
)



parser = argparse.ArgumentParser()
parser.add_argument('--pids', nargs='+', type=int, help='pid for checking it can be --pids 1, or --pids 1 2 3')
parser.add_argument('--aws', action='store_true', help='if email is sending from aws instance')

opt = parser.parse_args()


from_email = "youremail@gmail.com" # the email where you sent the email
password = "yourpassword"
subject = "your message"
message_body = "There is/are process/es not running"
to_email = "destination@gmail.com"



def send_mail_from_gmail(from_email,password,to_email,subject,message_body):
    # First you have to disable less secure applications:
    # https://stackoverflow.com/questions/16512592/login-credentials-not-working-with-gmail-smtp
    
    # Interesting answer:
    # https://stackoverflow.com/questions/52292971/sending-single-email-with-3-different-attachments-python-3
    
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    
    msg.attach(MIMEText(message_body, 'plain'))
    
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        
        
        server.sendmail(from_email, to_email, text)
        server.quit()
    
    except Exception as e:
        logging.exception("Error: " + str(e))
    else:
        logging.info("Email sent!")




# Replace sender@example.com with your "From" address. 
# This address must be verified.
SENDER = 'info@yourcompany.ai'  
SENDERNAME = 'Info yourcompany.ai'

# Replace recipient@example.com with a "To" address. If your account 
# is still in the sandbox, this address must be verified.
RECIPIENT  = 'info@yourcompany.ai'

# Replace smtp_username with your Amazon SES SMTP user name.
USERNAME_SMTP = "your SMTP"

# Replace smtp_password with your Amazon SES SMTP password.
PASSWORD_SMTP = "your PASSWORD"

# (Optional) the name of a configuration set to use for this message.
# If you comment out this line, you also need to remove or comment out
# the "X-SES-CONFIGURATION-SET:" header below.
#CONFIGURATION_SET = "ConfigSet"

# If you're using Amazon SES in an AWS Region other than US West (Oregon), 
# replace email-smtp.us-west-2.amazonaws.com with the Amazon SES SMTP  
# endpoint in the appropriate region.
HOST = "email-smtp.eu-west-1.amazonaws.com"
PORT = 587

# The subject line of the email.
SUBJECT = 'Your process'

# The email body for recipients with non-HTML email clients.
BODY_TEXT = ("There is/are process/es not running"
            )

# The HTML body of the email.
#BODY_HTML = """<html>
#<head></head>
#<body>
#  <h1>Amazon SES SMTP Email Test</h1>
#  <p>This email was sent with Amazon SES using the
#    <a href='https://www.python.org/'>Python</a>
#    <a href='https://docs.python.org/3/library/smtplib.html'>
#    smtplib</a> library.</p>
#</body>
#</html>
#            """

def send_mail_from_aws(SENDER, SENDERNAME, RECIPIENT, USERNAME_SMTP, PASSWORD_SMTP):
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
    msg['To'] = RECIPIENT
    # Comment or delete the next line if you are not using a configuration set
    #msg.add_header('X-SES-CONFIGURATION-SET',CONFIGURATION_SET)
    
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(BODY_TEXT, 'plain')
    #part2 = MIMEText(BODY_HTML, 'html')
    
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    #msg.attach(part2)
    
    # Try to send the message.
    try:  
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()
        #stmplib docs recommend calling ehlo() before & after starttls()
        server.ehlo()
        server.login(USERNAME_SMTP, PASSWORD_SMTP)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())
        server.close()
    # Display an error message if something goes wrong.
    except Exception as e:
        logging.exception("Error: " + str(e))
    else:
        logging.info("Email sent!")








    
    
check_pid = opt.pids

while True:
    
    print("Process running...")
    
    pid_list = psutil.pids()
    
    true_list = []

    for val in check_pid:
        if val in psutil.pids():
            true_list.append(True)
        else:
            true_list.append(False)
    
    if not all(true_list):
        if opt.aws:
            send_mail_from_aws(SENDER, SENDERNAME, RECIPIENT, USERNAME_SMTP, PASSWORD_SMTP)
        else:
            send_mail_from_gmail(from_email,password,to_email,subject,message_body)
        logging.info("Waiting an hour before continue...")
        time.sleep(3600*4)
    
    print("Sleeping 1 minute ZZzzz...")
    time.sleep(60)
    
