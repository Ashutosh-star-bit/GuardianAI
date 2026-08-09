"""
GuardianAI Persona-Tailored Human-Friendly Explainability (XAI) Engine
Purpose: Generates persona-tailored XAI explanations (Students, Parents, Senior Citizens, Professionals) covering:
         1. Why it is risky, 2. Which evidence matters most, 3. Possible false positives,
         4. Confidence explanation, and 5. Recommended action.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class PersonaExplanationDTO(BaseModel):
    """Structured Persona Explanation DTO."""
    persona_key: str = Field(description="STUDENTS, PARENTS, SENIOR_CITIZENS, PROFESSIONALS")
    risk_summary: str
    key_evidence_highlight: str
    false_positive_possibility: str
    confidence_explanation: str
    recommended_action: str

class DecisionXAIExplanationReport(BaseModel):
    """Container for multi-persona XAI explanation report."""
    scan_id: str
    risk_level: str
    active_persona: str
    primary_explanation: PersonaExplanationDTO
    all_persona_explanations: Dict[str, PersonaExplanationDTO] = Field(default_factory=dict)

class DecisionXAIEngine:
    """Enterprise Persona-Tailored Human-Friendly Explainability Engine."""

    @classmethod
    def generate_persona_explanation(
        cls,
        persona: str,
        risk_level: str,
        confidence: float,
        top_evidence: List[str],
        scam_category: str
    ) -> PersonaExplanationDTO:
        """Generates 5-part explanation tailored for a specific persona perspective."""
        p_key = persona.upper()
        r_level = risk_level.upper()
        conf_pct = int(confidence * 100)

        top_ev_str = ", ".join(top_evidence[:2]) if top_evidence else "suspicious formatting"

        if p_key == "SENIOR_CITIZENS":
            risk_summary = f"CAUTION: This message looks like a scam attempt ({r_level} RISK). It uses fake warnings to trick you into sending money or clicking bad links."
            evidence_hl = f"The most dangerous part is: {top_ev_str}."
            false_pos = "Occasionally, a real company might send an urgent notice, but legitimate companies will never rush you or ask for secret codes."
            conf_exp = f"Our security system is {conf_pct}% certain about this assessment."
            rec_act = "PLEASE DO NOT CLICK ANY LINKS OR SEND MONEY. Ask a trusted family member or call your bank directly using the phone number on your card."

        elif p_key == "PARENTS":
            risk_summary = f"FAMILY ALERT ({r_level} RISK): This message contains phishing or smishing markers aimed at compromising financial accounts."
            evidence_hl = f"Key threats identified: {top_ev_str}."
            false_pos = "Sometimes legitimate utility or school notices use urgent phrasing, but they will not request immediate wire transfers or PIN entries."
            conf_exp = f"Evaluated with {conf_pct}% confidence across AI and technical security databases."
            rec_act = "Warn family members not to engage. Verify the sender independently before taking any action."

        elif p_key == "STUDENTS":
            risk_summary = f"HEADS UP ({r_level} RISK): Fake alert or phishing link detected."
            evidence_hl = f"Flagged indicators: {top_ev_str}."
            false_pos = "Unusual links or tracking parameters can trigger flags on legit promos."
            conf_exp = f"Model confidence: {conf_pct}% based on cross-modal signal agreement."
            rec_act = "Don't click the link or DM the sender. Block & report."

        else: # PROFESSIONALS
            risk_summary = f"SECURITY VERDICT ({r_level} RISK): Potential Social Engineering / Business Email Compromise (BEC) attempt."
            evidence_hl = f"Primary IOC Evidence: {top_ev_str}."
            false_pos = "External marketing campaigns or unverified vendor domains can occasionally mimic suspicious patterns."
            conf_exp = f"Confidence score: {conf_pct}% based on technical IOC matching and LLM psychological factor evaluation."
            rec_act = "Do not click links or execute transactions. Forward payload to corporate SecOps (abuse@domain.com) for investigation."

        return PersonaExplanationDTO(
            persona_key=p_key,
            risk_summary=risk_summary,
            key_evidence_highlight=evidence_hl,
            false_positive_possibility=false_pos,
            confidence_explanation=conf_exp,
            recommended_action=rec_act
        )

    @classmethod
    def generate_full_xai_report(
        cls,
        scan_id: str,
        risk_level: str = "HIGH",
        confidence: float = 0.95,
        evidence_list: Optional[List[str]] = None,
        scam_category: str = "BANK_SPOOF",
        target_persona: str = "SENIOR_CITIZENS"
    ) -> DecisionXAIExplanationReport:
        """
        Generates multi-persona human-friendly explanations across Students, Parents, Senior Citizens, and Professionals.
        """
        ev_items = evidence_list or ["Suspicious website link", "Fake account lock warning"]
        personas = ["STUDENTS", "PARENTS", "SENIOR_CITIZENS", "PROFESSIONALS"]

        all_reports: Dict[str, PersonaExplanationDTO] = {}
        for p in personas:
            all_reports[p] = cls.generate_persona_explanation(
                persona=p,
                risk_level=risk_level,
                confidence=confidence,
                top_evidence=ev_items,
                scam_category=scam_category
            )

        active_p = target_persona.upper() if target_persona.upper() in all_reports else "SENIOR_CITIZENS"
        primary = all_reports[active_p]

        return DecisionXAIExplanationReport(
            scan_id=scan_id,
            risk_level=risk_level,
            active_persona=active_p,
            primary_explanation=primary,
            all_persona_explanations=all_reports
        )
