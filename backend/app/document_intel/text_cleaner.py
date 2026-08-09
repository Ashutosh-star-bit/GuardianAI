"""
GuardianAI Enterprise OCRTextCleaner Subsystem
Purpose: Cleans raw OCR output streams:
         Repairs broken lines, removes hyphenation breaks, collapses repeated spaces/newlines,
         corrects common OCR character confusions, strips invisible/control chars, and normalizes Unicode homoglyphs.
"""

import re
import unicodedata
from typing import Dict

class TextCleaner:
    """Enterprise OCR Text Cleaner & Normalization Engine."""

    # Common OCR Character Confusion Substitutions
    OCR_CONFUSION_MAP: Dict[str, str] = {
        r'\bpaypa1\b': 'paypal',
        r'\bp@ypal\b': 'paypal',
        r'\bs3cur1ty\b': 'security',
        r'\bv3r1fy\b': 'verify',
        r'\bacc0unt\b': 'account',
        r'\bb@nk\b': 'bank',
        r'\buurg3nt\b': 'urgent',
    }

    # Unicode Cyrillic -> Latin Homoglyph Map
    CYRILLIC_HOMOGLYPH_MAP: Dict[str, str] = {
        '\u0430': 'a', '\u0410': 'A',
        '\u0435': 'e', '\u0415': 'E',
        '\u0456': 'i', '\u0406': 'I',
        '\u043e': 'o', '\u041e': 'O',
        '\u0440': 'p', '\u0420': 'P',
        '\u0441': 'c', '\u0421': 'C',
        '\u0443': 'y', '\u0423': 'Y',
        '\u0445': 'x', '\u0425': 'X',
    }

    @classmethod
    def clean_ocr_text(cls, raw_text: str, fix_homoglyphs: bool = True) -> str:
        """
        Executes complete 6-stage OCR text cleaning pipeline.
        """
        if not raw_text:
            return ""

        text = raw_text

        # Stage 1: Strip Invisible & Control Characters (Null bytes, Zero-width spaces, Control chars)
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\u200b-\u200d\ufeff]', '', text)

        # Stage 2: Unicode NFKC Normalization & Homoglyph Replacement
        text = unicodedata.normalize("NFKC", text)
        if fix_homoglyphs:
            for cyr, lat in cls.CYRILLIC_HOMOGLYPH_MAP.items():
                text = text.replace(cyr, lat)

        # Stage 3: Repair Hyphenated Line Breaks (e.g. "verifi-\ncation" -> "verification")
        text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)

        # Stage 4: Rejoin Broken Sentence Line Breaks
        # Lines ending without punctuation followed by a lowercase line start are rejoined
        text = re.sub(r'([^\.\!\?\:\;\n])\n([a-z])', r'\1 \2', text)

        # Stage 5: Correct Common OCR Character Mistakes & Leetspeak Confusions
        for pattern, replacement in cls.OCR_CONFUSION_MAP.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

        # Stage 6: Collapse Repeated Spaces & Excess Line Breaks
        text = re.sub(r'[ \t]+', ' ', text)  # Collapse horizontal whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)  # Collapse 3+ newlines to double newline
        lines = [line.strip() for line in text.split('\n')]
        
        return "\n".join(lines).strip()
