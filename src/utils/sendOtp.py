from email.message import EmailMessage
import os
import smtplib
from  python_random_strings.python_random_strings import random_strings 

def sendOtp(toEmail : str,OTPCode : str ) :
    fromEmail = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    em = EmailMessage()

    em['Subject'] = f'verify your account'
    em['From'] = fromEmail
    em['To'] = toEmail

    em.set_content(f"verify your account with the {OTPCode}")
    smtp = smtplib.SMTP('smtp.gmail.com',587)

    smtp.set_debuglevel(False)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(fromEmail,password)
    smtp.sendmail(fromEmail,toEmail,em.as_string())