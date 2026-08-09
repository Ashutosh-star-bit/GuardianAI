"""
GuardianAI Production Transcript Cleaner Engine
Purpose: Provides 6-stage STT transcript repair and normalization:
         1. Unicode Normalization (NFKC normalization, stripping non-breaking spaces & control chars)
         2. Filler Word Removal (Strips 'uh', 'um', 'aah', 'er', 'hmm', 'you know', etc.)
         3. Repeated Stutter Word Removal ('the the' -> 'the', 'pay pay' -> 'pay')
         4. Spoken Homoglyph & Keyword Repair ('pay pal' -> 'paypal', 'g pay' -> 'gpay')
         5. Punctuation & Sentence Restoration (Capitalization & trailing sentence punctuation)
         6. Broken Hyphen & Line Wrap Reconstruction.
"""

import re
import unicodedata
from app.voice_intel.base import BaseTranscriptCleaner

class TranscriptCleaner(BaseTranscriptCleaner):
    """Enterprise STT Transcript Repair Engine."""

    # 1. Acoustic Filler Words Regex
    FILLER_WORDS_REGEX = re.compile(
        r'\b(uh+|um+|aah+|er+|hmm+|like|you\s+know|i\s+mean|basically|actually|listen\s+carefully)\b',
        re.IGNORECASE
    )

    # 2. Repeated Stutter Words Regex (e.g., "pay pay", "the the", "to to")
    REPEATED_WORDS_REGEX = re.compile(r'\b(\w+)\s+\1\b', re.IGNORECASE)

    # 3. Spoken Homoglyphs & Keyword Repair Rules
    HOMOGLYPH_REPLACEMENTS = {
        r'\bpay\s*pal\b': 'paypal',
        r'\bg\s*pay\b': 'gpay',
        r'\bphone\s*pe\b': 'phonepe',
        r'\bpay\s*tm\b': 'paytm',
        r'\bkyc\b': 'KYC',
        r'\botp\b': 'OTP',
        r'\bcbi\b': 'CBI',
        r'\bupi\b': 'UPI',
        r'\baadhaar\b': 'Aadhaar'
    }

    def clean(self, raw_transcript: str) -> str:
        """
        Executes 6-stage STT transcript cleaning pipeline.
        """
        if not raw_transcript or not raw_transcript.strip():
            return ""

        # Stage 1: Unicode Normalization (NFKC) & Control Character Stripping
        text = unicodedata.normalize('NFKC', raw_transcript)
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\xa0]', ' ', text)

        # Stage 2: Acoustic Filler Word Removal
        text = self.FILLER_WORDS_REGEX.sub('', text)

        # Stage 3: Repeated Stutter Word Removal (e.g. "pay pay" -> "pay")
        # Run twice to catch triple repetitions ("the the the" -> "the")
        text = self.REPEATED_WORDS_REGEX.sub(r'\1', text)
        text = self.REPEATED_WORDS_REGEX.sub(r'\1', text)

        # Stage 4: Spoken Homoglyph & Domain Keyword Repair
        for pattern, replacement in self.HOMOGLYPH_REPLACEMENTS.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

        # Stage 5: Broken Line Wraps & Hyphen Reconstruction
        text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)

        # Stage 6: Punctuation & Sentence Capitalization Restoration
        text = self._restore_punctuation_and_capitalization(text)

        return text

    def _restore_punctuation_and_capitalization(self, text: str) -> str:
        """Restores missing capitalization and trailing sentence punctuation."""
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        cleaned_text = " ".join(lines)

        # Normalize multiple spaces
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        if not cleaned_text:
            return ""

        # Capitalize first letter of text
        cleaned_text = cleaned_text[0].upper() + cleaned_text[1:]

        # Capitalize after sentence periods
        cleaned_text = re.sub(r'(\.\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper(), cleaned_text)

        # Ensure trailing sentence punctuation
        if not cleaned_text.endswith(('.', '!', '?')):
            cleaned_text += '.'

        return cleaned_text
