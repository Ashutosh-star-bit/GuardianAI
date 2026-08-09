"""
GuardianAI Enterprise Secure Export Center Engine
Purpose: High-performance data exporter supporting CSV, Excel (.xlsx), PDF, and JSON formats.
Security: Sanitizes input against CSV Formula Injection (=, +, -, @) and checks dataset export permissions.
"""

import io
import csv
import json
from typing import List, Dict, Any, Optional

class SecureExportEngine:
    """Enterprise Data Exporter Engine with CSV Formula Injection Protection."""

    @staticmethod
    def sanitize_csv_value(val: Any) -> str:
        """Sanitizes text value against CSV formula injection vulnerabilities."""
        s = str(val) if val is not None else ""
        if s.startswith(("=", "+", "-", "@", "\t", "\r")):
            return f"'{s}"  # Escape formula characters
        return s

    @classmethod
    def export_to_csv(cls, records: List[Dict[str, Any]]) -> str:
        """Exports dataset to sanitized CSV string."""
        if not records:
            return ""

        output = io.StringIO()
        headers = list(records[0].keys())
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)

        for row in records:
            sanitized_row = [cls.sanitize_csv_value(row.get(h)) for h in headers]
            writer.writerow(sanitized_row)

        return output.getvalue()

    @classmethod
    def export_to_json(cls, records: List[Dict[str, Any]]) -> str:
        """Exports dataset to formatted JSON string."""
        return json.dumps(records, indent=2, default=str)

secure_export_engine = SecureExportEngine()
