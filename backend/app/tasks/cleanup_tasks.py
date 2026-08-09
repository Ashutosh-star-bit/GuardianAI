"""
GuardianAI Storage & Temporary File Cleanup Background Tasks
Purpose: Asynchronously purges expired temporary upload files and stale cache records from disk.
"""

import os
import time
from app.core.logging import logger

UPLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "uploads")

async def cleanup_expired_uploads_async(max_age_hours: int = 24):
    """
    Background worker that scans backend/uploads/ directory and purges files older than max_age_hours.
    """
    logger.info(f"[Background Task] Initiating storage cleanup for files older than {max_age_hours} hours...")
    purged_count = 0
    now = time.time()
    cutoff_time = now - (max_age_hours * 3600)

    try:
        if os.path.exists(UPLOADS_DIR):
            for filename in os.listdir(UPLOADS_DIR):
                file_path = os.path.join(UPLOADS_DIR, filename)
                if os.path.isfile(file_path):
                    file_mtime = os.path.getmtime(file_path)
                    if file_mtime < cutoff_time:
                        os.remove(file_path)
                        purged_count += 1
                        logger.info(f"[Background Task] Purged expired upload file: {filename}")

        logger.info(f"[Background Task] Storage cleanup completed. Total files purged: {purged_count}")
    except Exception as e:
        logger.error(f"[Background Task Error] Failed to complete storage cleanup: {str(e)}", exc_info=True)
