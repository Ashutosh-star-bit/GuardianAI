"""
GuardianAI Gmail SMTP Direct Email Dispatcher Service
Uses 100% Direct Gmail SMTP via TLS (smtp.gmail.com:587) with App Password.
Dispatches real 6-digit verification emails to ANY recipient email address in the world.
Includes full Anti-Spam headers to ensure delivery to Primary Inbox.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate, make_msgid
import os
import logging

logger = logging.getLogger("guardianai.email_service")

def send_verification_email(to_email: str, otp_code: str, user_name: str = "") -> bool:
    """
    Dispatches 6-digit email verification code directly using Gmail SMTP with strict anti-spam headers.
    """
    subject = f"Your GuardianAI 6-Digit Verification Code: {otp_code}"
    
    text_body = f"""Hello {user_name or to_email},

Thank you for creating an account with GuardianAI.

Your 6-digit email verification code is: {otp_code}

This code will expire in 10 minutes. If you did not request this email, please ignore it.

© 2026 GuardianAI Zero-Knowledge Security Systems
"""

    html_body = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #090d16; color: #f1f5f9; padding: 20px; margin: 0;">
  <div style="max-width: 520px; margin: 0 auto; background: #0f172a; border: 1px solid #1e293b; padding: 32px; border-radius: 16px;">
    <div style="display: flex; items-center; gap: 8px; margin-bottom: 20px;">
      <h2 style="color: #38bdf8; margin: 0; font-size: 20px; font-weight: 800;">GuardianAI Threat Protection</h2>
    </div>
    <p style="color: #94a3b8; font-size: 14px; margin-bottom: 12px;">Hello <strong style="color: #f8fafc;">{user_name or to_email}</strong>,</p>
    <p style="color: #cbd5e1; font-size: 14px; line-height: 1.5;">Thank you for registering with GuardianAI. Enter the 6-digit verification code below to activate your account:</p>
    
    <div style="background: #020617; border: 2px solid #38bdf8; padding: 20px; border-radius: 12px; text-align: center; margin: 24px 0;">
      <span style="font-size: 36px; font-weight: 900; letter-spacing: 10px; color: #38bdf8; font-family: monospace; display: block;">{otp_code}</span>
    </div>
    
    <p style="color: #64748b; font-size: 12px; margin-bottom: 20px;">This security code will expire in 10 minutes. If you did not request this account, you can safely ignore this email.</p>
    
    <div style="background: #1e293b/40; border-left: 3px solid #f59e0b; padding: 12px; border-radius: 6px; margin-bottom: 24px;">
      <p style="color: #fcd34d; font-size: 11px; margin: 0; font-weight: 600;">💡 Tip: If you do not see future security alerts in your Primary inbox, please mark this email as "Not Spam".</p>
    </div>

    <hr style="border: 0; border-top: 1px solid #1e293b; margin: 20px 0;" />
    <p style="color: #475569; font-size: 11px; text-align: center; margin: 0;">© 2026 GuardianAI Zero-Knowledge Security Systems • All Rights Reserved</p>
  </div>
</body>
</html>
"""

    print(f"[GMAIL SMTP DISPATCH] Preparing 6-digit verification code {otp_code} for {to_email}")

    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USERNAME") or os.getenv("SMTP_USER") or "ash.singh.991892@gmail.com"
    smtp_pass = (os.getenv("SMTP_PASSWORD") or os.getenv("SMTP_PASS") or "gmeszrditxnmchaa").replace(" ", "")
    sender_email = os.getenv("SENDER_EMAIL", smtp_user)

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"GuardianAI Security <{sender_email}>"
        msg["To"] = to_email
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid(domain="guardianai.io")
        msg["X-Mailer"] = "GuardianAI-Security-Dispatcher/1.0"
        msg["Reply-To"] = sender_email

        # Attach Plain Text first, then HTML as alternative
        msg.attach(MIMEText(text_body, "plain", "utf-8"))
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(smtp_user, smtp_pass)
            server.sendmail(sender_email, [to_email], msg.as_string())
        
        logger.info(f"Gmail SMTP verification email successfully delivered to {to_email}")
        print(f"[GMAIL SMTP DELIVERED SUCCESS]: 6-digit code sent directly to {to_email}!")
        return True
    except Exception as e:
        logger.error(f"SMTP error delivering to {to_email}: {str(e)}")
        print(f"[GMAIL SMTP FAILURE]: {str(e)}")
        return False
