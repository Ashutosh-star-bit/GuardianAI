"""
GuardianAI Direct Gmail SMTP Email Dispatcher Service
Uses Direct Gmail SMTP via TLS (smtp.gmail.com:587) with App Password.
Dispatches real 6-digit verification emails to ANY recipient email address globally.
Requires 0 custom domain setup, 0 external API keys, and auto-retries up to 3 times.
"""

import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate, make_msgid
import os
import logging

logger = logging.getLogger("guardianai.email_service")

# Master Credentials (100% Free for ANY Email Address, No Domain Needed)
DEFAULT_GMAIL_USER = "ash.singh.991892@gmail.com"
DEFAULT_GMAIL_PASS = "gmeszrditxnmchaa"

def send_verification_email(to_email: str, otp_code: str, user_name: str = "") -> bool:
    """
    Dispatches 6-digit email verification code directly using Gmail SMTP.
    Includes 3 automatic retries and full anti-spam RFC headers.
    """
    subject = f"Your GuardianAI 6-Digit Verification Code: {otp_code}"
    
    text_body = f"""Hello {user_name or to_email},

Thank you for registering with GuardianAI.

Your 6-digit email verification code is: {otp_code}

This security code will expire in 10 minutes. If you did not request this account, please ignore this email.

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

    <div style="background: #1e293b; border-left: 3px solid #f59e0b; padding: 12px; border-radius: 6px; margin-bottom: 24px;">
      <p style="color: #fcd34d; font-size: 11px; margin: 0; font-weight: 600;">💡 Tip: If you do not see this email in your Primary inbox, please check your Spam / Junk folder.</p>
    </div>

    <hr style="border: 0; border-top: 1px solid #1e293b; margin: 20px 0;" />
    <p style="color: #475569; font-size: 11px; text-align: center; margin: 0;">© 2026 GuardianAI Zero-Knowledge Security Systems • All Rights Reserved</p>
  </div>
</body>
</html>
"""

    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USERNAME") or os.getenv("SMTP_USER") or DEFAULT_GMAIL_USER
    smtp_pass = (os.getenv("SMTP_PASSWORD") or os.getenv("SMTP_PASS") or DEFAULT_GMAIL_PASS).replace(" ", "")
    sender_email = os.getenv("SENDER_EMAIL", smtp_user)

    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            print(f"[GMAIL SMTP DISPATCH - Attempt {attempt}/{max_attempts}] Dispatching code {otp_code} to {to_email} via {smtp_user}...")
            
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"GuardianAI Security <{sender_email}>"
            msg["To"] = to_email
            msg["Date"] = formatdate(localtime=True)
            msg["Message-ID"] = make_msgid(domain="gmail.com")
            msg["X-Mailer"] = "GuardianAI-Security-Dispatcher/1.0"
            msg["Reply-To"] = sender_email

            msg.attach(MIMEText(text_body, "plain", "utf-8"))
            msg.attach(MIMEText(html_body, "html", "utf-8"))

            with smtplib.SMTP(smtp_server, smtp_port, timeout=12) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(smtp_user, smtp_pass)
                server.sendmail(sender_email, [to_email], msg.as_string())
            
            logger.info(f"Gmail SMTP verification email successfully delivered to {to_email}")
            print(f"[GMAIL SMTP DELIVERED SUCCESS]: 6-digit code sent directly to {to_email}!")
            return True
        except Exception as e:
            logger.error(f"Attempt {attempt} failed delivering to {to_email}: {str(e)}")
            print(f"[GMAIL SMTP ATTEMPT {attempt} FAILED]: {str(e)}")
            if attempt < max_attempts:
                time.sleep(1)

    return False
