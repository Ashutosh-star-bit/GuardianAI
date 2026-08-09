"""
GuardianAI VoiceProcessor Master Orchestrator
Purpose: Orchestrates the 6 Voice Intelligence processing stages:
         Cache Lookup -> Audio Preprocessing -> Language Detection -> STT Transcription -> Transcript Cleaning -> Speaker Metadata Extraction.
         Includes ThreadPoolExecutor parallel processing for bulk batch audio execution.
"""

import time
import uuid
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, List
from app.voice_intel.audio_preprocessor import AudioPreprocessor
from app.voice_intel.stt_provider import SpeechToTextProvider
from app.voice_intel.transcript_cleaner import TranscriptCleaner
from app.voice_intel.speaker_metadata import SpeakerMetadata
from app.voice_intel.language_detector import LanguageDetector
from app.voice_intel.cache import voice_cache_instance
from app.voice_intel.schemas import AudioPayload, VoiceAnalysisResult

class VoiceProcessor:
    """Master High-Performance Voice Intelligence Processing Engine."""

    def __init__(self, max_workers: int = 8):
        self.preprocessor = AudioPreprocessor()
        self.stt_provider = SpeechToTextProvider()
        self.transcript_cleaner = TranscriptCleaner()
        self.speaker_metadata_engine = SpeakerMetadata()
        self.language_detector = LanguageDetector()
        self.executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="VoiceProc")

    def process_audio(self, payload: AudioPayload, use_cache: bool = True) -> VoiceAnalysisResult:
        """
        Executes 6-stage audio processing pipeline with fast-path LRU caching (<1ms).
        """
        start_time = time.time()

        # 1. Thread-Safe LRU Cache Fast-Path Lookup (<1ms)
        if use_cache and payload.raw_bytes:
            cached_result = voice_cache_instance.get(payload.raw_bytes)
            if cached_result:
                return cached_result

        # 2. Audio Preprocessing (16kHz Resampling, Peak Normalization, VAD)
        preprocessed = self.preprocessor.preprocess(payload)

        # 3. Acoustic Language Identification
        detected_lang = self.language_detector.detect_language(payload)

        # 4. Speech-to-Text Transcription with Retries & SLA Timeout
        stt_res = self.stt_provider.transcribe(preprocessed, language_hint=detected_lang)

        # 5. Transcript Cleaning & Homoglyph Normalization
        stt_res.cleaned_transcript = self.transcript_cleaner.clean(stt_res.raw_transcript)

        # 6. Speaker Metadata & Acoustic Urgency Analysis
        metadata_res = self.speaker_metadata_engine.extract_metadata(preprocessed, stt_res.cleaned_transcript)

        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        audio_id = f"aud_{uuid.uuid4().hex[:12]}"

        result = VoiceAnalysisResult(
            audio_id=audio_id,
            scan_id=f"scn_{audio_id}",
            duration_seconds=preprocessed.duration_seconds,
            stt_result=stt_res,
            speaker_metadata=metadata_res,
            detected_language=detected_lang,
            is_streaming=False,
            processing_time_ms=elapsed_ms
        )

        if use_cache and payload.raw_bytes:
            voice_cache_instance.set(payload.raw_bytes, result)

        return result

    async def async_process_batch(self, payloads: List[AudioPayload], use_cache: bool = True) -> List[VoiceAnalysisResult]:
        """
        Executes parallel multi-threaded batch processing across all audio payloads.
        """
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(self.executor, self.process_audio, payload, use_cache)
            for payload in payloads
        ]
        return await asyncio.gather(*tasks)
