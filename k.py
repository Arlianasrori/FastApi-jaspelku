from email.message import EmailMessage
import os
import ssl
import smtplib

fromEmail = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PASSWORD")
print(password)
toEmail = "aabiljr@gmail.com"
em = EmailMessage()

em['Subject'] = f'verify your account'
em['From'] = fromEmail
em['To'] = toEmail
em.set_content("verify yah")
message = "hay"
context = ssl.create_default_context()
smtp = smtplib.SMTP('smtp.gmail.com',587)
smtp.set_debuglevel(1)
smtp.ehlo()
smtp.starttls()
smtp.login(fromEmail,password)
smtp.sendmail(fromEmail,toEmail,em.as_string())

print(em.as_string())
# with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp :
#     smtp.login(fromEmail,password)
#     smtp.sendmail(fromEmail,toEmail,em.as_string())