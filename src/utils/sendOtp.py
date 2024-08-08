from email.message import EmailMessage
import os
import smtplib
from  python_random_strings.python_random_strings import random_strings 

async def sendOtp(toEmail : str,) :
    fromEmail = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    em = EmailMessage()

    OTPCode = random_strings.random_digits(6)
    em['Subject'] = f'verify your account'
    em['From'] = fromEmail
    em['To'] = toEmail
    em.set_content(f"verify your account with the {OTPCode}")
    smtp = smtplib.SMTP('smtp.gmail.com',587)
    smtp.set_debuglevel(1)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(fromEmail,password)
    smtp.sendmail(fromEmail,toEmail,em.as_string())