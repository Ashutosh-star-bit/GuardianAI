"""
GuardianAI Python Integration Sample Application
"""

import sys
import os

# Add SDK path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../sdks/python")))

from guardianai import GuardianAIClient

def main():
    print("=== GuardianAI Python Anti-Scam Inspection Demo ===")
    client = GuardianAIClient(api_key="gai_live_88f92a110099xza21_prod")

    # 1. URL Inspection
    url_result = client.scan_url("http://hdfc-verify.top")
    print(f"\n[URL Scan] Target: http://hdfc-verify.top")
    print(f"Threat Score: {url_result.threat_score}/100")
    print(f"Action: {url_result.recommended_action}")
    print(f"Explanation: {url_result.explanation}")

    # 2. Text Message Inspection
    text_result = client.scan_text("URGENT: Your bank account is suspended. Update KYC immediately.")
    print(f"\n[Text Scan] Target: SMS Payload")
    print(f"Threat Score: {text_result.threat_score}/100")
    print(f"Action: {text_result.recommended_action}")

if __name__ == "__main__":
    main()
