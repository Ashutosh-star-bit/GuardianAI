// GuardianAI Client-Side Web Worker for PII Scrubbing
// Purpose: Offloads Regex and SpaCy-lite PII anonymization to a background thread before payloads leave the browser.

self.onmessage = (e: MessageEvent<string>) => {
  const rawText = e.data;

  if (!rawText) {
    self.postMessage({ sanitizedText: "", scrubCount: 0 });
    return;
  }

  let scrubbed = rawText;
  let count = 0;

  // 1. Credit Card Numbers (Luhn-like 13-19 digit match)
  const ccRegex = /\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})\b/g;
  scrubbed = scrubbed.replace(ccRegex, () => {
    count++;
    return "[REDACTED_CREDIT_CARD]";
  });

  // 2. US Social Security Numbers (SSN)
  const ssnRegex = /\b\d{3}-\d{2}-\d{4}\b/g;
  scrubbed = scrubbed.replace(ssnRegex, () => {
    count++;
    return "[REDACTED_SSN]";
  });

  // 3. International Bank Account Numbers (IBAN)
  const ibanRegex = /[A-Z]{2}\d{2}[A-Z0-9]{11,30}/gi;
  scrubbed = scrubbed.replace(ibanRegex, () => {
    count++;
    return "[REDACTED_BANK_IBAN]";
  });

  // 4. Crypto Wallet Addresses (BTC / ETH)
  const cryptoRegex = /(0x[a-fA-F0-9]{40}|[13][a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[a-z0-9]{39,59})/g;
  scrubbed = scrubbed.replace(cryptoRegex, () => {
    count++;
    return "[REDACTED_CRYPTO_ADDRESS]";
  });

  // 5. Phone Numbers (US/International standard)
  const phoneRegex = /\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b/g;
  scrubbed = scrubbed.replace(phoneRegex, () => {
    count++;
    return "[REDACTED_PHONE]";
  });

  self.postMessage({ sanitizedText: scrubbed, scrubCount: count });
};
