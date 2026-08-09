# GuardianAI: Master UI/UX Design & Wireframe Specification

**Document Title:** Master UI/UX Wireframe & Accessibility Design Specification for GuardianAI  
**Document Version:** 1.0.0  
**Status:** Approved for Frontend Engineering  
**Authors:** Leadership Team (Principal Software Architect, Principal AI Engineer, Principal Cybersecurity Engineer, Senior Product Manager, Senior UX Designer)  
**Target Guidelines:** WCAG 2.1 Level AA, Accessible Non-Alarmist UX, Senior Citizen Friendly  

---

## Executive Summary & Design System Principles

GuardianAI's user experience is built around **Calm Security, Transparent Explainability, and Universal Accessibility**. Security interfaces often induce panic through aggressive red alert banners and cryptic technical jargon. GuardianAI flips this paradigm by providing clear, color-coded threat signals (Green/Yellow/Red), plain-language summaries, visual text attributions, and a dedicated **Senior Citizen Mode**.

---

## 1. Universal Layout Structure & Top Navigation

All authenticated screens share a responsive, accessible application shell featuring a top navigation bar with instant access to the **Senior Mode Toggle** and quick scanning tools.

```mermaid
graph TD
    subgraph AppShell["GuardianAI Responsive Application Shell"]
        TopNav["Navbar: Logo | Senior Mode Toggle (Big Button) | Scans Remaining | Profile Menu"]
        MainContent["Main Content Area (Dynamic Router View)"]
        BottomNav["Mobile Bottom Tab Bar (Scan | History | Analytics | Settings)"]
    end

    TopNav --> MainContent
    MainContent --> BottomNav
```

---

## 2. Screen Wireframes & UX Rationales

### 2.1 Screen 1: Landing Page (`/`)

* **Purpose:** Introduces GuardianAI, provides instant 1-click scan capabilities without requiring immediate sign-up, and demonstrates XAI visual highlights.

```mermaid
graph TD
    subgraph LandingPage["Landing Page Layout"]
        Hero["Hero Section: 'Stop AI Scams Before They Strike' + 1-Click Instant Scan Input Box"]
        LiveDemo["Live Interactive Demo: Sample Scam Text with Toggleable XAI Highlight Overlays"]
        ValuePillars["3-Step Process: 1. Paste/Upload -> 2. AI Explains Why -> 3. Actionable Safety"]
        PersonaSection["Target Audience Cards: Seniors, Students, Parents, Employees"]
        PricingTable["Tier Comparison: Free ($0/mo) | Pro ($4.99/mo) | Teams ($14.99/mo)"]
        Footer["Footer: Privacy Guarantee | Terms | FTC Direct Link"]
    end

    Hero --> LiveDemo
    LiveDemo --> ValuePillars
    ValuePillars --> PersonaSection
    PersonaSection --> PricingTable
    PricingTable --> Footer
```

* **UX Rationale:** 
  * Providing an immediate scan input directly on the hero section reduces conversion friction.
  * The Senior Mode quick-toggle switch is prominently displayed at the top right of the hero banner.

---

### 2.2 Screen 2: Main Dashboard (`/dashboard`)

* **Purpose:** Primary command hub for authenticated users, showing personal safety score, scan quota, and quick scanner tabs.

```mermaid
graph TD
    subgraph DashboardLayout["Dashboard Layout Grid"]
        Header["Welcome Header + Safety Status Index Badge (e.g. 'Safety Score: 94/100 - Good')"]
        
        subgraph TopRow["Metric Summary Cards"]
            Card1["Scans Used: 12 / 50 (Free)"]
            Card2["Scams Flagged: 3 This Month"]
            Card3["Top Threat Encountered: Smishing SMS"]
        end

        subgraph CenterScanner["Quick Multi-Payload Scanner Hub"]
            Tabs["Scanner Tabs: [Text/SMS] | [URL] | [QR Code] | [Email Header]"]
            InputArea["Active Scanner Input Area + Local PII Scrubbing Shield Icon"]
            SubmitBtn["Big Action Button: 'Analyze For Scams'"]
        end

        RecentList["Recent Scan History (Last 5 Scans with Risk Badges)"]
    end

    Header --> TopRow
    TopRow --> CenterScanner
    CenterScanner --> RecentList
```

* **UX Rationale:**
  * Displays a consolidated "Safety Index" badge giving users positive reinforcement for scanning messages.
  * Multi-payload tabs allow switching between Text, URL, QR, and Email without page reloads.

---

### 2.3 Screen 3: Scan Message Screen (`/scan/text`)

* **Purpose:** Specialized interface for analyzing raw text and SMS messages.

```mermaid
graph TD
    subgraph TextScanner["Scan Message Layout"]
        Instruction["Instruction Header: 'Paste any suspicious text or SMS message below'"]
        InputBox["Large Text Area + Auto-Paste Helper Button"]
        PIINotice["Shield Badge: 'Client-Side Privacy Enabled - Names & Phone Numbers scrubbed locally'"]
        AnalyzeBtn["Action Button: 'Analyze Message'"]

        subgraph ResultPanel["XAI Result Report Panel (Renders on completion)"]
            RiskGauge["Threat Score Gauge: [ 88 / 100 - DANGEROUS ] (Red Badge)"]
            PlainRationale["Plain-Language Box: 'Claims to be your bank, but links to an untrusted site.'"]
            SpanHighlighter["Interactive Highlight Box: [URGENT] (Amber) | [paypa1-check.com] (Red)"]
            RemediationCard["Step-by-Step Action List: 1. Do NOT click link | 2. Call Bank"]
        end
    end

    InputBox --> PIINotice
    PIINotice --> AnalyzeBtn
    AnalyzeBtn --> ResultPanel
```

* **UX Rationale:**
  * Auto-paste helper button reduces friction on mobile devices.
  * Visual highlights allow users to click individual flagged words to read specific threat reasons.

---

### 2.4 Screen 4: Scan Email Screen (`/scan/email`)

* **Purpose:** Parses `.eml` raw email files or pasted email headers to detect Business Email Compromise (BEC) and domain spoofing.

```mermaid
graph TD
    subgraph EmailScanner["Scan Email Layout"]
        Dropzone["Drag-and-Drop File Zone (Upload .eml file) OR Switch to Raw Header Paste Tab"]
        SubmitEmail["Action Button: 'Inspect Email Headers'"]

        subgraph EmailResults["Forensic Header Analysis Panel"]
            HeaderSummary["Status Card: SPF = FAIL | DKIM = NONE | DMARC = FAIL"]
            SpoofAlert["Warning Banner: 'Sender domain company.com mismatch with Reply-To bad.ru'"]
            BodyPreview["Sanitized Sandboxed Email Body Preview (Safe HTML Renderer)"]
            ActionList["Remediation: 'Do NOT authorize wire transfer. Contact sender in person.'"]
        end
    end

    Dropzone --> SubmitEmail
    SubmitEmail --> EmailResults
```

* **UX Rationale:**
  * Clearly separates authentication technical matrices (SPF/DKIM) from practical human advice.
  * Email body rendering is sandboxed inside an isolated iframe to prevent script execution.

---

### 2.5 Screen 5: Scan URL Screen (`/scan/url`)

* **Purpose:** Evaluates target web links for WHOIS age, typosquatting, and homoglyphs.

```mermaid
graph TD
    subgraph URLScanner["Scan URL Layout"]
        URLInput["Single-Line URL Input Bar (e.g. https://paypa1-check.com/login)"]
        ScanURLBtn["Action Button: 'Inspect URL Safety'"]

        subgraph URLResults["URL Safety Report"]
            ScoreBadge["Threat Score: 92 / 100 - DANGEROUS"]
            DomainStats["Domain Metrics: Domain Age = 2 Days | Typosquatting = YES (PayPal)"]
            HeadlessPreview["Safe Headless Sandbox Preview Screenshot (Non-interactive image)"]
            Remediation["Safety Guide: 'Do not enter credentials on this site.'"]
        end
    end

    URLInput --> ScanURLBtn
    ScanURLBtn --> URLResults
```

* **UX Rationale:**
  * Shows a static screenshot of the destination page taken in a cloud sandbox so users can visually recognize spoofed login portals without opening the link themselves.

---

### 2.6 Screen 6: Scan QR Screen (`/scan/qr`)

* **Purpose:** Decodes QR codes from flyer pictures or live camera feeds.

```mermaid
graph TD
    subgraph QRScanner["Scan QR Layout"]
        CameraFeed["Live Camera Scanner Frame (Mobile) OR Drag & Drop QR Image Upload"]
        ExtractedURL["Decoded Payload Banner: 'Extracted URL: http://malicious-qr.com'"]

        subgraph QRResults["Quishing Risk Assessment"]
            QRScore["Threat Score: 85 / 100 - DANGEROUS"]
            QRRationale["Rationale: 'This QR code flyer links to an unverified domain.'"]
            QRAction["Action: 'Do not proceed to link.'"]
        end
    end

    CameraFeed --> ExtractedURL
    ExtractedURL --> QRResults
```

* **UX Rationale:**
  * Does NOT automatically open the decoded URL in the browser, preventing drive-by downloads.

---

### 2.7 Screen 7: Scan History Screen (`/history`)

* **Purpose:** Allows users to search, filter, and review past scan results.

```mermaid
graph TD
    subgraph HistoryLayout["Scan History Layout"]
        FilterBar["Filter Controls: [All Risk Bands] | [Text/URL/QR/Email] | Date Picker | Search"]
        HistoryTable["Paginated Data Table / Mobile Card Stack"]
        
        subgraph TableRow["Sample Table Row"]
            Col1["Date: July 28, 2026"]
            Col2["Type: SMS Text"]
            Col3["Risk Badge: DANGEROUS (88)"]
            Col4["Summary: Bank imposter text..."]
            Col5["Action: [ Re-Inspect Report ]"]
        end

        Pagination["Pagination Bar: < Page 1 of 5 >"]
    end

    FilterBar --> HistoryTable
    HistoryTable --> Pagination
```

* **UX Rationale:**
  * Uses clear color-coded pill badges for quick visual scanning of historical threats.

---

### 2.8 Screen 8: Reports & Fraud Dispatch Screen (`/reports`)

* **Purpose:** Formats anonymized threat payloads and submits official reports to public anti-fraud agencies.

```mermaid
graph TD
    subgraph ReportsLayout["Fraud Reporting Layout"]
        SelectScan["Dropdown: Select Scan to Report (e.g. Scan #scn_a1b2c3 - Dangerous)"]
        AgencyPicker["Radio Selection: [ FTC (Federal Trade Commission) ] | [ APWG ] | [ IC3 ]"]
        PreviewCard["Formatted Anonymized Report Preview (PII Scrubbed)"]
        SendBtn["Big Action Button: 'Dispatch Automated Report'"]
        StatusTracker["Dispatched Reports History & Submission Receipts Table"]
    end

    SelectScan --> AgencyPicker
    AgencyPicker --> PreviewCard
    PreviewCard --> SendBtn
    SendBtn --> StatusTracker
```

* **UX Rationale:**
  * Shows users a live preview of the scrubbed data *before* sending, reinforcing privacy trust.

---

### 2.9 Screen 9: Analytics Screen (`/analytics`)

* **Purpose:** Visualizes personal or organization threat metrics over time.

```mermaid
graph TD
    subgraph AnalyticsLayout["Analytics Grid Layout"]
        TimeFilter["Time Window Selector: [ Last 7 Days ] | [ Last 30 Days ] | [ YTD ]"]
        
        subgraph ChartRow1["Charts Row 1"]
            PieChart["Risk Breakdown (Pie Chart: Safe vs Caution vs Dangerous)"]
            LineGraph["Scams Encountered Over Time (Trend Line Graph)"]
        end

        subgraph ChartRow2["Charts Row 2"]
            BarChart["Top Targeted Channels (SMS vs QR vs URL vs Email)"]
            StatBox["Personal Scam Avoidance Rate: 100%"]
        end
    end

    TimeFilter --> ChartRow1
    ChartRow1 --> ChartRow2
```

---

### 2.10 Screen 10: Profile Screen (`/profile`)

* **Purpose:** Manages account information, subscription tier, and active security sessions.

```mermaid
graph TD
    subgraph ProfileLayout["Profile Management Layout"]
        UserInfo["User Details Card: Email | Verified Status | Member Since"]
        SubCard["Subscription Card: Current Tier (Free / Pro) + Upgrade Button"]
        SecCard["Security & Sessions: MFA Status (Active) | Active Devices List"]
    end

    UserInfo --> SubCard
    SubCard --> SecCard
```

---

### 2.11 Screen 11: Settings Screen (`/settings`)

* **Purpose:** Controls accessibility modes, privacy options, and developer API keys.

```mermaid
graph TD
    subgraph SettingsLayout["Settings Layout"]
        subgraph AccSection["1. Accessibility & Senior Citizen Settings"]
            SeniorToggle["Switch: Senior Mode (Large text, high contrast, zero jargon)"]
            AudioToggle["Switch: Auto-play Audio Rationale Summaries"]
        end

        subgraph PrivacySection["2. Privacy & Data Retention Toggles"]
            ZKToggle["Switch: Zero-Knowledge Mode (Do not store scan metadata)"]
            PurgeBtn["Button: 'Purge All My Personal Data Instantly'"]
        end

        subgraph DevSection["3. Developer API Keys (Pro / Team Tiers)"]
            KeyTable["Generated API Keys List + [ Generate New Key Button ]"]
        end
    end

    AccSection --> PrivacySection
    PrivacySection --> DevSection
```

* **UX Rationale:**
  * Senior Mode toggle is given top billing on the settings page for immediate accessibility configuration.

---

### 2.12 Screen 12: Error Pages (`404`, `500`, `Offline`)

```mermaid
graph TD
    subgraph ErrorLayout["Standard Error Screen Structure"]
        Icon["Friendly Graphic Icon (Shield / Network Disconnected)"]
        Title["Plain Language Headline: 'We Couldn't Find That Page' OR 'Service Momentarily Busy'"]
        Explanation["Explanation: 'Don't worry, your personal safety data remains secure.'"]
        PrimaryAction["Primary Button: 'Return to Safety Dashboard'"]
    end

    Icon --> Title
    Title --> Explanation
    Explanation --> PrimaryAction
```

---

### 2.13 Screen 13: Loading States (Skeleton UI & Progress Indicators)

```mermaid
graph TD
    subgraph LoadingState["Scan Execution Loading Overlay"]
        Spinner["Pulsing Shield Animation"]
        StepText["Dynamic Step Indicator: 'Scrubbing PII locally...' -> 'Analyzing WHOIS age...' -> 'Synthesizing XAI rationale...'"]
        ProgressPill["Progress Bar (0% to 100%)"]
    end

    Spinner --> StepText
    StepText --> ProgressPill
```

* **UX Rationale:**
  * Informative dynamic step text manages user expectations and educates them on the deep checks being performed during the sub-1.8s wait.

---

### 2.14 Screen 14: Empty States (`No History`, `No Scans`)

```mermaid
graph TD
    subgraph EmptyState["Empty State Container"]
        Illustration["Calm Empty Box Illustration"]
        Header["Header: 'No Scans Yet'"]
        Body["Body: 'Paste a suspicious message or try one of our safe sample messages below.'"]
        SampleBtns["Sample Try-It Buttons: [ Sample Smishing SMS ] | [ Sample Typosquat URL ]"]
    end

    Illustration --> Header
    Header --> Body
    Body --> SampleBtns
```

* **UX Rationale:**
  * Includes 1-click sample buttons so new users can test GuardianAI's XAI features immediately without needing a real scam message.

---

### 2.15 Screen 15: Success Pages (`Report Dispatched`, `Key Generated`)

```mermaid
graph TD
    subgraph SuccessPage["Success State Container"]
        Checkmark["Green Animated Checkmark Icon"]
        Headline["Headline: 'Report Dispatched to FTC Successfully'"]
        ReceiptDetails["Receipt Card: Confirmation ID #FTC-998877 | Timestamp"]
        NextAction["Primary Button: 'Back to Dashboard'"]
    end

    Checkmark --> Headline
    Headline --> ReceiptDetails
    ReceiptDetails --> NextAction
```

---

## 3. Usability & Accessibility Audit

The cross-functional UI/UX leadership team audited the screen wireframes against core accessibility standards:

1. **Senior Citizen Accessibility (WCAG 2.1 AA):**  
   * **Senior Mode** activates $18\text{px}+$ typography, $7:1$ contrast ratios, converts complex technical graphs into plain-language status cards, and turns on Web Speech audio narrations.
2. **Colorblind Friendliness:**  
   * All risk badges rely on **Icon + Text Label + Color** (e.g., `[!] DANGEROUS (Red)` vs `[v] SAFE (Green)`), ensuring users with color vision deficiencies can distinguish risk bands easily.
3. **Non-Alarmist UX:**  
   * Red alerts provide instant, reassuring remediation checklists ("What you should do next") rather than inciting fear.

---
*End of Master UI/UX Design & Wireframe Specification.*
