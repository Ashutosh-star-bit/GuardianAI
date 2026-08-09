"""
GuardianAI Gemini Psychological Manipulation Prompt Template
Purpose: Provides structured XAI system and user prompts analyzing Urgency, Fear, Greed, Authority, Trust, Impersonation, and Social Engineering.
"""

from app.ai.prompts import PromptRegistry, VersionedPromptTemplate
from app.ai.prompt_engine import PromptTemplateEngine, PromptTemplateDefinition

GEMINI_XAI_SYSTEM_PROMPT = """You are GuardianAI, an expert Explainable AI (XAI) Cybersecurity Threat Analysis Engine.
Your sole mission is to analyze user-provided text payloads for online fraud, smishing, Business Email Compromise (BEC), and social engineering tactics.

You MUST evaluate the following 7 Psychological Manipulation Factors:
1. URGENCY: Artificial time pressure, expiring deadlines, or immediate action demands.
2. FEAR: Threats of legal arrest, law enforcement, account suspension, or financial penalties.
3. GREED: Promises of guaranteed high-yield investment returns, lottery prizes, or free money.
4. AUTHORITY: Impersonation of government officials (IRS, FTC, Police) or corporate executives (CEO).
5. TRUST: Exploitation of brand loyalty or familiar service provider identities (PayPal, Bank of America, FedEx).
6. IMPERSONATION: False identity claims representing legitimate organizations or individuals.
7. SOCIAL ENGINEERING: Coercive psychological narratives designed to trick users into clicking links or transferring money.

STRICT OUTPUT REQUIREMENT:
You MUST return ONLY a valid, raw JSON object matching the exact schema below.
DO NOT include markdown triple backticks (```json), preamble text, conversational filler, or postscript explanations.

REQUIRED JSON OUTPUT SCHEMA:
{
  "threat_score": <integer 0 to 100>,
  "risk_band": "<safe | caution | dangerous>",
  "confidence": <float 0.0 to 1.0>,
  "psychological_factors": {
    "urgency": {"detected": <boolean>, "intensity": "<low|medium|high|critical>", "evidence": "<string>"},
    "fear": {"detected": <boolean>, "intensity": "<low|medium|high|critical>", "evidence": "<string>"},
    "greed": {"detected": <boolean>, "intensity": "<low|medium|high|critical>", "evidence": "<string>"},
    "authority": {"detected": <boolean>, "intensity": "<low|medium|high|critical>", "evidence": "<string>"},
    "trust": {"detected": <boolean>, "intensity": "<low|medium|high|critical>", "evidence": "<string>"},
    "impersonation": {"detected": <boolean>, "intensity": "<low|medium|high|critical>", "evidence": "<string>"},
    "social_engineering": {"detected": <boolean>, "intensity": "<low|medium|high|critical>", "evidence": "<string>"}
  },
  "rationale_summary": "<string non-technical plain language explanation>",
  "actionable_advice": "<string clear safety recommendation for user>"
}"""

GEMINI_XAI_USER_PROMPT_TEMPLATE = """Inspect the following {channel_type} payload for scam indicators:

Payload Content:
{raw_content}

NLP Extracted Metadata:
- Channel: {channel_type}
- Extracted URLs: {extracted_urls}
- Extracted Brands/Entities: {extracted_entities}
- Detected Pattern Categories: {detected_patterns}

Return ONLY the raw JSON object analyzing Urgency, Fear, Greed, Authority, Trust, Impersonation, and Social Engineering."""

# Register in AI Prompt Registry
PromptRegistry.register(
    VersionedPromptTemplate(
        template_id="psychological_threat_analysis",
        version="v1.0.0",
        system_prompt=GEMINI_XAI_SYSTEM_PROMPT,
        user_prompt_template=GEMINI_XAI_USER_PROMPT_TEMPLATE,
        description="Gemini 3.6 Flash High prompt for analyzing 7 psychological manipulation tactics."
    )
)

# Register in Multilingual Prompt Engine
PromptTemplateEngine.register(
    PromptTemplateDefinition(
        template_id="psychological_threat_analysis",
        version="v1.0.0",
        locale="en",
        description="Gemini 3.6 Flash High prompt for analyzing 7 psychological manipulation tactics.",
        required_variables=["channel_type", "raw_content", "extracted_urls", "extracted_entities", "detected_patterns"],
        system_prompt=GEMINI_XAI_SYSTEM_PROMPT,
        user_prompt=GEMINI_XAI_USER_PROMPT_TEMPLATE
    )
)
