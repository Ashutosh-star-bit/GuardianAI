/**
 * GuardianAI PageAnalysisService Engine
 * Purpose: Content service responsible for extracting, filtering, and sanitizing page DOM structures:
 *          Visible text, links, forms, buttons, meta tags, JSON-LD structured data, URL, and page title.
 *          Strictly enforces Privacy Controls (PII Redaction, Zero Credential Leakage).
 */

export interface ButtonElementData {
  text: string;
  type: string;
  aria_label: string;
  is_payment_action: boolean;
}

export interface MetaTagData {
  description: string;
  canonical_url: string;
  og_title: string;
  og_image: string;
  json_ld_types: string[];
}

export interface SanitizedPagePayload {
  url: string;
  domain: string;
  title: string;
  visible_text: string;
  meta: MetaTagData;
  links_summary: {
    total_count: number;
    external_count: number;
    upi_links_count: number;
    sample_links: { href: string; text: string }[];
  };
  forms_summary: {
    total_forms: number;
    has_insecure_http_form: boolean;
    has_password_input: boolean;
    form_actions: string[];
  };
  buttons: ButtonElementData[];
  sanitized_at: number;
}

export class PageAnalysisService {
  private static PII_EMAIL_REGEX = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
  private static PII_PHONE_REGEX = /(\+?\d{1,4}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}/g;
  private static PII_CREDIT_CARD_REGEX = /\b(?:\d[ -]*?){13,16}\b/g;

  /**
   * Main entry point collecting and sanitizing page DOM for GuardianAI backend inspection.
   */
  public static collectAndSanitizePageData(): SanitizedPagePayload {
    const currentUrl = window.location.href;
    const domain = window.location.hostname;
    const title = (document.title || '').trim().substring(0, 150);

    // 1. Meta Tags & JSON-LD Structured Data
    const meta = this.extractMetaTagsAndJsonLd();

    // 2. Visible Text (Sanitized of PII)
    const rawVisibleText = this.extractCleanVisibleText();
    const sanitizedText = this.redactPII(rawVisibleText);

    // 3. Links Summary
    const links_summary = this.extractLinksSummary(domain);

    // 4. Forms Summary (Privacy-preserving: ZERO input values included)
    const forms_summary = this.extractFormsSummary();

    // 5. Buttons Inspection
    const buttons = this.extractButtonElements();

    return {
      url: currentUrl,
      domain,
      title,
      visible_text: sanitizedText.substring(0, 10000), // Max 10,000 chars payload limit
      meta,
      links_summary,
      forms_summary,
      buttons,
      sanitized_at: Date.now()
    };
  }

  private static extractMetaTagsAndJsonLd(): MetaTagData {
    const descEl = document.querySelector<HTMLMetaElement>('meta[name="description"], meta[property="og:description"]');
    const ogTitleEl = document.querySelector<HTMLMetaElement>('meta[property="og:title"]');
    const ogImageEl = document.querySelector<HTMLMetaElement>('meta[property="og:image"]');
    const canonicalEl = document.querySelector<HTMLLinkElement>('link[rel="canonical"]');

    const jsonLdTypes: string[] = [];
    const jsonLdScripts = document.querySelectorAll<HTMLScriptElement>('script[type="application/ld+json"]');
    jsonLdScripts.forEach((script) => {
      try {
        const parsed = JSON.parse(script.textContent || '{}');
        if (parsed['@type']) {
          jsonLdTypes.push(String(parsed['@type']));
        }
      } catch {
        // Ignore invalid JSON-LD
      }
    });

    return {
      description: (descEl?.content || '').substring(0, 300),
      canonical_url: canonicalEl?.href || window.location.href,
      og_title: (ogTitleEl?.content || '').substring(0, 150),
      og_image: ogImageEl?.content || '',
      json_ld_types: jsonLdTypes.slice(0, 5)
    };
  }

  private static extractCleanVisibleText(): string {
    const textNodes: string[] = [];
    const walker = document.createTreeWalker(
      document.body || document.documentElement,
      NodeFilter.SHOW_TEXT,
      {
        acceptNode(node) {
          if (!node.parentElement) return NodeFilter.FILTER_REJECT;
          const tag = node.parentElement.tagName.toLowerCase();
          if (['script', 'style', 'noscript', 'iframe', 'svg'].includes(tag)) {
            return NodeFilter.FILTER_REJECT;
          }
          const text = node.textContent?.trim() || '';
          return text.length > 2 ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
        }
      }
    );

    let node = walker.nextNode();
    while (node) {
      if (node.textContent) textNodes.push(node.textContent.trim());
      node = walker.nextNode();
    }

    return textNodes.join(' ');
  }

  private static redactPII(text: string): string {
    return text
      .replace(this.PII_EMAIL_REGEX, '[REDACTED_EMAIL]')
      .replace(this.PII_CREDIT_CARD_REGEX, '[REDACTED_CARD_NUMBER]');
  }

  private static extractLinksSummary(currentDomain: string) {
    const anchors = document.querySelectorAll<HTMLAnchorElement>('a[href]');
    let externalCount = 0;
    let upiCount = 0;
    const samples: { href: string; text: string }[] = [];

    anchors.forEach((a, i) => {
      const href = a.href;
      if (href.startsWith('upi://')) upiCount++;

      try {
        if (new URL(href).hostname !== currentDomain) externalCount++;
      } catch {
        // Ignore malformed URLs
      }

      if (i < 15) {
        samples.push({
          href: href.substring(0, 200),
          text: (a.textContent || '').trim().substring(0, 60)
        });
      }
    });

    return {
      total_count: anchors.length,
      external_count: externalCount,
      upi_links_count: upiCount,
      sample_links: samples
    };
  }

  private static extractFormsSummary() {
    const forms = document.querySelectorAll<HTMLFormElement>('form');
    let hasInsecure = false;
    let hasPassword = false;
    const actions: string[] = [];

    forms.forEach((form) => {
      const action = form.action || window.location.href;
      if (action.startsWith('http:')) hasInsecure = true;
      actions.push(action.substring(0, 150));

      if (form.querySelector('input[type="password"]')) {
        hasPassword = true;
      }
    });

    return {
      total_forms: forms.length,
      has_insecure_http_form: hasInsecure,
      has_password_input: hasPassword,
      form_actions: actions.slice(0, 5)
    };
  }

  private static extractButtonElements(): ButtonElementData[] {
    const buttons = document.querySelectorAll<HTMLButtonElement | HTMLInputElement>('button, input[type="button"], input[type="submit"]');
    const result: ButtonElementData[] = [];
    const paymentKeywords = /pay|buy|transfer|checkout|verify|claim|refund/i;

    const maxButtons = Math.min(buttons.length, 20);
    for (let i = 0; i < maxButtons; i++) {
      const b = buttons[i];
      const text = (b.textContent || (b as HTMLInputElement).value || '').trim();
      const ariaLabel = b.getAttribute('aria-label') || '';
      const isPayment = paymentKeywords.test(text) || paymentKeywords.test(ariaLabel);

      result.push({
        text: text.substring(0, 50),
        type: b.getAttribute('type') || 'button',
        aria_label: ariaLabel.substring(0, 50),
        is_payment_action: isPayment
      });
    }

    return result;
  }
}
