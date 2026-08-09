/**
 * GuardianAI Real-Time DOM Scanner Module
 * Purpose: Scans DOM links, forms, and UPI VPA patterns (`upi://pay?pa=...`) for phishing indicators.
 */

const UPI_REGEX = /upi:\/\/pay\?pa=([a-zA-Z0-9.\-_]+@[a-zA-Z0-9]+)/g;
const SUSPICIOUS_DOMAINS = ['paypa1', 'hdfc-verify', 'sbi-kyc', 'okaxis', 'ybl'];

export function scanDomLinksAndForms() {
  // 1. Scan Links
  const anchors = document.querySelectorAll<HTMLAnchorElement>('a[href]');
  anchors.forEach((a) => {
    const href = a.href;

    // Check for suspicious domains
    if (SUSPICIOUS_DOMAINS.some((sub) => href.toLowerCase().includes(sub))) {
      highlightSuspiciousElement(a, 'Suspicious Phishing Domain');
    }

    // Check for UPI Links
    if (href.startsWith('upi://')) {
      highlightSuspiciousElement(a, 'UPI Payment Handle');
    }
  });

  // 2. Scan Form Inputs
  const passwordInputs = document.querySelectorAll<HTMLInputElement>('input[type="password"]');
  if (passwordInputs.length > 0 && window.location.protocol === 'http:') {
    passwordInputs.forEach((input) => {
      highlightSuspiciousElement(input, 'Insecure Unencrypted Password Input (HTTP)');
    });
  }
}

function highlightSuspiciousElement(el: HTMLElement, reason: string) {
  el.style.outline = '2px solid #ef4444';
  el.style.backgroundColor = 'rgba(239, 68, 68, 0.15)';
  el.title = `GuardianAI Alert: ${reason}`;
}
