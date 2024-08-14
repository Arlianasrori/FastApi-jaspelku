from email.message import EmailMessage
import os
import smtplib
from  python_random_strings.python_random_strings import random_strings 

def sendOtp(toEmail : str,OTPCode : str ,isPassword : bool = False) :
    fromEmail = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    em = EmailMessage()

    if isPassword :
        em['Subject'] = f'verify your account'
        em.set_content(f"verify your account with the {OTPCode}")
    else :
        em['Subject'] = f'verify your account'
        em.set_content(f"verify your account for update password with the {OTPCode}")

    em['From'] = fromEmail
    em['To'] = toEmail
    smtp = smtplib.SMTP('smtp.gmail.com',587)

    em.set_content(f"verify your account with the {OTPCode}")
    smtp = smtplib.SMTP('smtp.gmail.com',587)

    smtp.set_debuglevel(False)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(fromEmail,password)
    smtp.sendmail(fromEmail,toEmail,em.as_string())