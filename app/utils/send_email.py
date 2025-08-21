import smtplib
from email.message import EmailMessage
from fastapi import HTTPException

from app.core import settings


def send_email(to_email: str, subject: str, body_text: str, body_html: str | None):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.email_user
    msg["To"] = to_email
    msg.set_content(body_text)
    if body_html:
        msg.add_alternative(body_html, subtype="html")
    try:
        with smtplib.SMTP(settings.email_host, settings.email_port) as server:
            server.starttls()
            server.login(settings.email_user, settings.email_pass)
            server.send_message(msg)
            print("Email sent!")
    except smtplib.SMTPAuthenticationError:
        raise HTTPException(status_code=500, detail="SMTP Authentication failed.")
    except smtplib.SMTPConnectError:
        raise HTTPException(
            status_code=500, detail="Failed to connect to the SMTP server."
        )
    except smtplib.SMTPRecipientsRefused:
        raise HTTPException(status_code=400, detail="Recipient address refused.")
    except smtplib.SMTPDataError:
        raise HTTPException(
            status_code=500, detail="SMTP server refused the email data."
        )
    except smtplib.SMTPServerDisconnected:
        raise HTTPException(
            status_code=500, detail="SMTP server disconnected unexpectedly."
        )
    except smtplib.SMTPException:
        raise HTTPException(status_code=500, detail="An SMTP error occurred.")
    except Exception:
        raise HTTPException(
            status_code=500, detail="An unknown error occurred while sending email."
        )
