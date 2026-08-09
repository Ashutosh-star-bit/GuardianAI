"""
GuardianAI Gemini Psychological Manipulation Prompt Unit Test Suite
Purpose: Tests prompt template registration, system prompt constraints (JSON only), and user prompt parameter formatting.
"""

import pytest
from app.nlp.prompts import GEMINI_XAI_SYSTEM_PROMPT
from app.ai.prompts import PromptRegistry
from app.ai.prompt_engine import PromptTemplateEngine

def test_prompt_system_constraints():
    """Tests that system prompt explicitly enforces raw JSON output and 7 psychological factors."""
    assert "ONLY a valid, raw JSON object" in GEMINI_XAI_SYSTEM_PROMPT
    assert "URGENCY" in GEMINI_XAI_SYSTEM_PROMPT
    assert "FEAR" in GEMINI_XAI_SYSTEM_PROMPT
    assert "GREED" in GEMINI_XAI_SYSTEM_PROMPT
    assert "AUTHORITY" in GEMINI_XAI_SYSTEM_PROMPT
    assert "TRUST" in GEMINI_XAI_SYSTEM_PROMPT
    assert "IMPERSONATION" in GEMINI_XAI_SYSTEM_PROMPT
    assert "SOCIAL ENGINEERING" in GEMINI_XAI_SYSTEM_PROMPT

def test_prompt_template_rendering():
    """Tests rendering user prompt with required NLP metadata variables."""
    rendered = PromptTemplateEngine.render_prompt(
        template_id="psychological_threat_analysis",
        variables={
            "channel_type": "SMS",
            "raw_content": "URGENT: Your PayPal account is suspended. Click http://paypa1-check.com",
            "extracted_urls": "http://paypa1-check.com",
            "extracted_entities": "PayPal",
            "detected_patterns": "BANK_SPOOF, URGENCY_PHRASE"
        }
    )
    assert "SMS" in rendered["user_prompt"]
    assert "paypa1-check.com" in rendered["user_prompt"]
    assert "PayPal" in rendered["user_prompt"]
    assert "BANK_SPOOF" in rendered["user_prompt"]
