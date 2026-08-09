# GuardianAI Text Intelligence Gemini JSON Response Schema Specification

**Document Version:** 1.0.0  
**Schema Identifier:** `gemini_text_threat_analysis_v1`  
**Target LLM Model:** Gemini 3.6 Flash High  
**Date:** July 2026  
**Status:** **ACTIVE PRODUCTION SPECIFICATION**  

---

## 1. Schema Overview & Architecture

The **Gemini Text Threat Analysis Schema** defines the structured JSON payload returned by Gemini 3.6 Flash High when analyzing SMS, Email, WhatsApp, and Telegram payloads.

### Future Compatibility Guarantee:
All Pydantic v2 schemas are configured with `model_config = ConfigDict(extra="ignore")`, ensuring backward and forward compatibility if future Gemini model revisions output new optional metadata attributes.

---

## 2. JSON Schema Specification

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "GeminiTextThreatAnalysisSchema",
  "type": "object",
  "required": [
    "threat_score",
    "risk_band",
    "confidence",
    "explanation",
    "psychological_techniques"
  ],
  "properties": {
    "threat_score": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100,
      "description": "Composite threat score from 0 (Safe) to 100 (Critical Fraud)"
    },
    "risk_band": {
      "type": "string",
      "enum": ["safe", "caution", "dangerous"],
      "description": "Qualitative threat classification"
    },
    "confidence": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0,
      "description": "Model confidence level"
    },
    "detected_features": {
      "type": "object",
      "description": "Extracted NLP quantitative features (urgency_score, link_count, caps_ratio)"
    },
    "entities": {
      "type": "array",
      "items": { "type": "object" },
      "description": "Extracted named entities (Brand, Money, Phone, URL)"
    },
    "reasons": {
      "type": "array",
      "items": { "type": "string" },
      "description": "List of specific threat rationale statements"
    },
    "risk_indicators": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "indicator_key": { "type": "string" },
          "severity": { "type": "string" },
          "description": { "type": "string" }
        }
      }
    },
    "explanation": {
      "type": "string",
      "description": "Non-technical plain language explanation for end users"
    },
    "psychological_techniques": {
      "type": "object",
      "description": "Evaluation of 7 psychological manipulation tactics (urgency, fear, greed, authority, trust, impersonation, social_engineering)"
    },
    "recommendations": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Actionable safety guidance for end users"
    }
  }
}
```

---

## 3. Complete Output Payload Example

```json
{
  "threat_score": 92,
  "risk_band": "dangerous",
  "confidence": 0.984,
  "detected_features": {
    "urgency_score": 0.85,
    "financial_coercion_score": 0.90,
    "caps_ratio": 0.35,
    "link_count": 1,
    "homoglyph_detected": true
  },
  "entities": [
    {
      "entity_type": "BRAND",
      "text": "PayPal",
      "confidence": 0.95
    },
    {
      "entity_type": "URL",
      "text": "http://paypa1-check.com",
      "confidence": 0.98
    }
  ],
  "reasons": [
    "High urgency smishing payload detected.",
    "Spoofed domain mimicking PayPal brand identity."
  ],
  "risk_indicators": [
    {
      "indicator_key": "TYPOSQUATTING_LINK",
      "severity": "Critical",
      "description": "Link uses paypa1-check.com to mimic PayPal"
    }
  ],
  "explanation": "High risk scam attempt. Message uses fake account lock warnings and a spoofed website link to steal credentials.",
  "psychological_techniques": {
    "urgency": { "detected": true, "intensity": "high", "evidence": "Your account is locked!" },
    "fear": { "detected": true, "intensity": "high", "evidence": "Immediate action required or access revoked" },
    "greed": { "detected": false, "intensity": "low", "evidence": "" },
    "authority": { "detected": false, "intensity": "low", "evidence": "" },
    "trust": { "detected": true, "intensity": "critical", "evidence": "Spoofed PayPal brand" },
    "impersonation": { "detected": true, "intensity": "critical", "evidence": "Mimicking PayPal login domain" },
    "social_engineering": { "detected": true, "intensity": "high", "evidence": "Fake account lock narrative" }
  },
  "recommendations": [
    "Do NOT click the embedded link.",
    "Log into PayPal independently via their official mobile app."
  ]
}
```
