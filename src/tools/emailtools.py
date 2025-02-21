import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime as dt
import dotenv
import logging
import os

logger = logging.getLogger(__name__)

config = dotenv.dotenv_values(f'{os.path.dirname(os.path.abspath(__file__))}/../.env')

data_directory = config.get("DATA_DIRECTORY")
log_directory = config.get("LOG_DIRECTORY")
log_level = config.get("LOG_LEVEL")
password = config.get('GMAIL_APP_KEY')
sender = config.get('EMAIL_SENDER')
recipients = config.get('EMAIL_RECIPIENTS')

def send_email():
    now = dt.now()
    logging.basicConfig(filename=f"{log_directory}/{now.date()}.log",level=log_level)
    body = "This is the body of the text message"

    msg = MIMEMultipart()
    msg.attach(MIMEText(body, "plain"))
    msg['Subject'] = 'Test email for solrmax'
    msg['From'] = sender
    msg['To'] = recipients
    with open('figure.jpg', 'rb') as image_file:
      msg.attach(MIMEImage(image_file.read()))
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
      logger.info(f'LoginResponse: {smtp_server.login(sender, password)}')
      logger.info(f'SendEmailResponse: {smtp_server.sendmail(sender, recipients, msg.as_string())}')
