"""
GuardianAI Enterprise High-Concurrency Load Testing Script
Simulates: 100, 500, and 1,000 Concurrent Users hitting Public API Gateway Endpoints.
"""

try:
    from locust import HttpUser, task, between
    
    class GuardianAILoadUser(HttpUser):
        """Simulates active API developer & application user hitting scanning endpoints."""
        wait_time = between(0.1, 0.5)

        def on_start(self):
            self.client.headers = {
                "Authorization": "Bearer gai_live_88f92a110099xza21_prod",
                "Content-Type": "application/json"
            }

        @task(4)
        def scan_text_smishing(self):
            self.client.post("/api/v1/public/scan/text", json={
                "text": "URGENT: Your account is suspended. Verify KYC at http://hdfc-verify.top"
            })

        @task(3)
        def scan_url_phishing(self):
            self.client.post("/api/v1/public/scan/url", json={
                "url": "http://hdfc-bank-login.top"
            })

        @task(2)
        def scan_ocr_document(self):
            self.client.post("/api/v1/public/scan/ocr", json={
                "document_text": "POLICE NOTICE: Digital arrest warrant issued. Pay fine via UPI."
            })

        @task(1)
        def get_system_telemetry_metrics(self):
            self.client.get("/api/v1/system/metrics")

except ImportError:
    class GuardianAILoadUser:
        """Fallback lightweight load test class when locust is not installed."""
        tasks = ["scan_text_smishing", "scan_url_phishing", "scan_ocr_document", "get_system_telemetry_metrics"]
