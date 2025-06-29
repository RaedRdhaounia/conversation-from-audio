import resend
from typing import Dict
from app.core.config import settings

def send_email(to_email: str, subject: str, body: str) -> bool:
    """
    Send an email using Resend API.
    
    Args:
        to_email (str): Recipient email address
        subject (str): Email subject
        body (str): Email body content (HTML or plain text)
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        resend.api_key = settings.resend_api_key
        
        admin_response = resend.Emails.send({
            "from": settings.email_from,
            "to": settings.admin_email,
            "subject": subject,
            "html": f"<p>{body}</p>"
        })
        
        user_response = resend.Emails.send({
            "from": settings.email_from,
            "to": to_email,
            "subject": "Thank you for contacting us",
            "html": "<p>Thank you for your message. We will get back to you soon.</p>"
        })
        
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False
