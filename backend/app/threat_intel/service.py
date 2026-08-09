"""
GuardianAI ThreatIntelligenceService Master Pipeline Orchestrator
Purpose: Orchestrates full Threat Intelligence Pipeline:
         Receive Indicators -> Analyse URLs -> Analyse Domains -> Analyse Email -> Analyse Phone ->
         Analyse UPI -> Generate Evidence -> Calculate Technical Risk Score -> Generate XAI Explanation -> Return Structured Result DTO.
"""

import uuid
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from app.threat_intel.url_intel import URLIntelligenceEngine, URLIntelligenceReport
from app.threat_intel.domain_intel import DomainIntelligenceEngine, DomainIntelReport
from app.threat_intel.email_intel import EmailIntelligenceEngine, EmailIntelReport
from app.threat_intel.phone_intel import PhoneIntelligenceEngine, PhoneIntelReport
from app.threat_intel.upi_intel import UPIIntelligenceEngine, UPIIntelReport
from app.threat_intel.indicator_extractor import IndicatorExtractorEngine, StructuredIOCContainer
from app.threat_intel.evidence_builder import EvidenceBuilderEngine, ThreatEvidenceReport, ThreatEvidenceItem
from app.threat_intel.scoring import ThreatScoringEngine, ThreatScoreResult
from app.threat_intel.explainability import ThreatExplainabilityEngine, ThreatIntelXAISummary

class ThreatIntelligencePipelineResult(BaseModel):
    """End-to-End Threat Intelligence Pipeline Execution Output DTO."""
    scan_id: str
    extracted_iocs: StructuredIOCContainer
    url_reports: List[URLIntelligenceReport] = Field(default_factory=list)
    domain_reports: List[DomainIntelReport] = Field(default_factory=list)
    email_reports: List[EmailIntelReport] = Field(default_factory=list)
    phone_reports: List[PhoneIntelReport] = Field(default_factory=list)
    upi_reports: List[UPIIntelReport] = Field(default_factory=list)
    evidence_report: ThreatEvidenceReport
    scoring_result: ThreatScoreResult
    xai_summary: ThreatIntelXAISummary

class ThreatIntelligenceService:
    """Enterprise Master Threat Intelligence Service Orchestrator."""

    @classmethod
    async def analyze_threat_payload(
        cls,
        scan_id: Optional[str] = None,
        raw_text: Optional[str] = None,
        urls: Optional[List[str]] = None,
        domains: Optional[List[str]] = None,
        emails: Optional[List[str]] = None,
        phones: Optional[List[str]] = None,
        upi_ids: Optional[List[str]] = None
    ) -> ThreatIntelligencePipelineResult:
        """
        Executes end-to-end Threat Intelligence Analysis Pipeline across all 5 threat vectors.
        """
        sid = scan_id or f"scn_th_{uuid.uuid4().hex[:10]}"

        # 1. Extract Indicators if raw_text provided
        if raw_text:
            extracted_container = IndicatorExtractorEngine.extract_all_indicators(raw_text)
        else:
            extracted_container = StructuredIOCContainer(
                urls=urls or [],
                domains=domains or [],
                emails=emails or [],
                phones=phones or [],
                upi_ids=upi_ids or []
            )

        # 2. Analyse URLs
        url_reports = [URLIntelligenceEngine.analyze_url(u) for u in extracted_container.urls]
        max_url_risk = max([r.risk_score for r in url_reports], default=0)

        # 3. Analyse Domains
        domain_reports = [DomainIntelligenceEngine.analyze_domain_intel(d) for d in extracted_container.domains]
        max_domain_risk = max([r.risk_score for r in domain_reports], default=0)

        # 4. Analyse Email
        email_reports = [EmailIntelligenceEngine.analyze_email(e) for e in extracted_container.emails]
        max_email_risk = max([r.risk_score for r in email_reports], default=0)

        # 5. Analyse Phone
        phone_reports = [PhoneIntelligenceEngine.parse_phone_number(p) for p in extracted_container.phones]
        max_phone_risk = max([r.risk_score for r in phone_reports], default=0)

        # 6. Analyse UPI
        upi_reports = [UPIIntelligenceEngine.analyze_upi(upi) for upi in extracted_container.upi_ids]
        max_upi_risk = max([r.risk_score for r in upi_reports], default=0)

        # 7. Generate Evidence
        evidence_items: List[ThreatEvidenceItem] = []

        # Collect URL evidence
        for r in url_reports:
            for ind in r.risk_indicators:
                evidence_items.append(
                    EvidenceBuilderEngine.create_evidence_item(
                        evidence_id=f"ev_url_{uuid.uuid4().hex[:6]}",
                        indicator=r.full_url,
                        category="URL",
                        reason=f"URL threat indicator: {ind}",
                        severity="High" if r.risk_score >= 50 else "Medium",
                        confidence=0.95,
                        source="URL_INTELLIGENCE"
                    )
                )

        # Collect Domain evidence
        for r in domain_reports:
            for ind in r.risk_indicators:
                evidence_items.append(
                    EvidenceBuilderEngine.create_evidence_item(
                        evidence_id=f"ev_dom_{uuid.uuid4().hex[:6]}",
                        indicator=r.domain,
                        category="DOMAIN",
                        reason=f"Domain threat indicator: {ind}",
                        severity="Critical" if r.risk_score >= 70 else "High",
                        confidence=0.98,
                        source="DOMAIN_INTELLIGENCE"
                    )
                )

        # Collect Email evidence
        for r in email_reports:
            for ind in r.risk_indicators:
                evidence_items.append(
                    EvidenceBuilderEngine.create_evidence_item(
                        evidence_id=f"ev_eml_{uuid.uuid4().hex[:6]}",
                        indicator=r.email_address,
                        category="EMAIL",
                        reason=f"Email threat indicator: {ind}",
                        severity="High" if r.risk_score >= 40 else "Medium",
                        confidence=0.92,
                        source="EMAIL_INTELLIGENCE"
                    )
                )

        # Collect UPI evidence
        for r in upi_reports:
            for ind in r.risk_indicators:
                evidence_items.append(
                    EvidenceBuilderEngine.create_evidence_item(
                        evidence_id=f"ev_upi_{uuid.uuid4().hex[:6]}",
                        indicator=r.upi_id,
                        category="UPI_ID",
                        reason=f"UPI threat indicator: {ind}",
                        severity="High" if r.risk_score >= 40 else "Medium",
                        confidence=0.95,
                        source="UPI_INTELLIGENCE"
                    )
                )

        evidence_report = EvidenceBuilderEngine.build_evidence_report(sid, evidence_items)

        # 8. Calculate Technical Risk
        scoring_result = ThreatScoringEngine.calculate_threat_score(
            scan_id=sid,
            domain_risk=max_domain_risk,
            url_risk=max_url_risk,
            upi_risk=max_upi_risk,
            email_risk=max_email_risk,
            phone_risk=max_phone_risk,
            evidence_report=evidence_report
        )

        # 9. Generate XAI Summary
        all_risk_indicator_keys = [item.reason.split(": ")[-1] for item in evidence_items]
        xai_summary = ThreatExplainabilityEngine.generate_xai_summary(sid, all_risk_indicator_keys)

        return ThreatIntelligencePipelineResult(
            scan_id=sid,
            extracted_iocs=extracted_container,
            url_reports=url_reports,
            domain_reports=domain_reports,
            email_reports=email_reports,
            phone_reports=phone_reports,
            upi_reports=upi_reports,
            evidence_report=evidence_report,
            scoring_result=scoring_result,
            xai_summary=xai_summary
        )
