from email.message import EmailMessage
import smtplib
from os import getenv
from dotenv import load_dotenv

class Message: 
    def __init__(self, address, text):
        self.address = address
        self.text = text

    def create_message(self):
        message = EmailMessage()
        message.set_content(self.text)
        message['Subject'] = 'Test Message'
        message['From'] = 'Me'
        message['To'] = self.address

        return message

class AutoEmail:
    def __init__(self):
        # Should use env variables, save them on your computer, then use load_dotenv(), then use these variables with getenv()
        self.mail_box = smtplib.SMTP('SERWER', 'PORT')
        self.mail_box.login('MAIL', 'PASSWORD')
    
    def __enter__(self):
        return self.mail_box
    
    def __exit__(self):
        self.mail_box.quit()