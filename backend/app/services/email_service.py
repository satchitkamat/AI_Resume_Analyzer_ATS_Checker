import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM")

def send_account_email(
        to_email: str,
        username: str,
        password: str
):
    subject = "Your AI Resume Analyzer Account"

    body = f"""
                Hello {username},

                Your account has been created successfully.

                Login Credentials:
                Email: {to_email}
                Password: {password}

                Please login and change your password after first login.

                Regards,
                AI Resume Analyzer Team
            """
    message = MIMEMultipart()

    message["From"] = EMAIL_FROM
    message["TO"] = to_email
    message["Subject"] = subject

    message.attach(
        MIMEText(body, "plain")
        )
    
    try:
        server = smtplib.SMTP(
            EMAIL_HOST,
            EMAIL_PORT
        )

        server.starttls()

        server.login(
            EMAIL_USERNAME,
            EMAIL_PASSWORD
        )

        server.sendmail(
            EMAIL_FROM,
            to_email,
            message.as_string()
        )

        server.quit()

        return True
    
    except Exception as e:
        print("Email Error: ", e)
        return False
    