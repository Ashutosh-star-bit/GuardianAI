"""
GuardianAI Gmail SMTP Direct Email Dispatcher Service
Uses 100% Direct Gmail SMTP via TLS (smtp.gmail.com:587) with App Password.
Dispatches real 6-digit verification emails to ANY recipient email address in the world.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

logger = logging.getLogger("guardianai.email_service")

def send_verification_email(to_email: str, otp_code: str, user_name: str = "") -> bool:
    """
    Dispatches 6-digit email verification code directly using Gmail SMTP with a strict 10-second timeout.
    """
    subject = f"Your GuardianAI 6-Digit Verification Code: {otp_code}"
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #090d16; color: #f1f5f9; padding: 20px;">
      <div style="max-width: 500px; margin: 0 auto; background: #0f172a; border: 1px solid #1e293b; padding: 30px; border-radius: 16px;">
        <h2 style="color: #38bdf8; margin-top: 0;">GuardianAI Threat Protection</h2>
        <p style="color: #94a3b8; font-size: 14px;">Hello {user_name or to_email},</p>
        <p style="color: #cbd5e1; font-size: 14px;">Thank you for creating an account. Enter the 6-digit verification code below to activate your account:</p>
        <div style="background: #020617; border: 1px solid #38bdf8; padding: 15px; border-radius: 12px; text-align: center; margin: 20px 0;">
          <span style="font-size: 32px; font-weight: 900; letter-spacing: 8px; color: #38bdf8; font-family: monospace;">{otp_code}</span>
        </div>
        <p style="color: #64748b; font-size: 12px;">This code will expire in 10 minutes. If you did not request this email, please ignore it.</p>
        <hr style="border: 0; border-top: 1px solid #1e293b; margin: 20px 0;" />
        <p style="color: #475569; font-size: 11px; text-align: center;">© 2026 GuardianAI Zero-Knowledge Security Systems</p>
      </div>
    </body>
    </html>
    """

    print(f"[GMAIL SMTP DISPATCH] Dispatching 6-digit code {otp_code} to recipient: {to_email}")

    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USERNAME", "ash.singh.991892@gmail.com")
    smtp_pass = os.getenv("SMTP_PASSWORD", "gmeszrditxnmchaa").replace(" ", "")
    sender_email = os.getenv("SENDER_EMAIL", smtp_user)

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"GuardianAI Security <{sender_email}>"
        msg["To"] = to_email
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(sender_email, [to_email], msg.as_string())
        
        logger.info(f"Gmail SMTP verification email successfully delivered to {to_email}")
        print(f"[GMAIL SMTP DELIVERED SUCCESS]: 6-digit code sent directly to {to_email}!")
        return True
    except Exception as e:
        logger.error(f"SMTP error delivering to {to_email}: {str(e)}")
        print(f"[GMAIL SMTP FAILURE]: {str(e)}")
        return False
