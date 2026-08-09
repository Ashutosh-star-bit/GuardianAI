/**
 * GuardianAI High-Performance Privacy-Preserving DOM Extractor Module
 * Purpose: Extracts visible text, links, form structures, page title, and meta tags:
 *          - Skips hidden elements (display: none, visibility: hidden, opacity: 0, aria-hidden="true")
 *          - Strictly ignores password values, credit card numbers, CVVs, and secure input values
 *          - Optimized TreeWalker traversal with sub-5ms performance SLA.
 */

export interface ExtractedLink {
  href: string;
  text: string;
  is_external: boolean;
  is_upi: boolean;
}

export interface ExtractedFormField {
  name: string;
  type: string;
  placeholder: string;
  is_sensitive: boolean; // True for password, credit card, SSN fields
}

export interface ExtractedForm {
  action: string;
  method: string;
  is_insecure_http: boolean;
  fields: ExtractedFormField[];
}

export interface StructuredPageContent {
  title: string;
  meta_description: string;
  canonical_url: string;
  visible_text: string;
  links: ExtractedLink[];
  forms: ExtractedForm[];
  has_password_input: boolean;
  has_upi_link: boolean;
  extraction_time_ms: number;
}

const SENSITIVE_INPUT_TYPES = new Set(['password', 'hidden', 'credit-card', 'cvv']);
const SENSITIVE_NAME_REGEX = /pass|pwd|card|cvv|secret|token|ssn|pin/i;

export function extractStructuredPageContent(): StructuredPageContent {
  const startTime = performance.now();

  // 1. Page Title & Meta Extraction
  const title = document.title || '';
  const metaDescEl = document.querySelector<HTMLMetaElement>('meta[name="description"], meta[property="og:description"]');
  const metaDescription = metaDescEl ? metaDescEl.content : '';

  const canonicalEl = document.querySelector<HTMLLinkElement>('link[rel="canonical"]');
  const canonicalUrl = canonicalEl ? canonicalEl.href : window.location.href;

  // 2. Visible Text Extraction via TreeWalker (Skipping <script>, <style>, hidden elements)
  const visibleText = extractVisibleTextNodes();

  // 3. Links Extraction
  const { links, hasUpiLink } = extractPageLinks();

  // 4. Forms Extraction (Privacy-preserving: NO passwords or secure values extracted)
  const { forms, hasPasswordInput } = extractPageForms();

  const elapsedTimeMs = Math.round((performance.now() - startTime) * 100) / 100;

  return {
    title,
    meta_description: metaDescription,
    canonical_url: canonicalUrl,
    visible_text: visibleText,
    links,
    forms,
    has_password_input: hasPasswordInput,
    has_upi_link: hasUpiLink,
    extraction_time_ms: elapsedTimeMs
  };
}

function extractVisibleTextNodes(): string {
  const textParts: string[] = [];
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

        if (isElementHidden(node.parentElement)) {
          return NodeFilter.FILTER_REJECT;
        }

        const text = node.textContent?.trim() || '';
        return text.length > 0 ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
      }
    }
  );

  let currentNode = walker.nextNode();
  while (currentNode) {
    if (currentNode.textContent) {
      textParts.push(currentNode.textContent.trim());
    }
    currentNode = walker.nextNode();
  }

  // Limit max extracted text payload to 15,000 chars for efficiency
  return textParts.join(' ').substring(0, 15000);
}

function isElementHidden(el: HTMLElement): boolean {
  if (el.getAttribute('aria-hidden') === 'true') return true;

  const style = window.getComputedStyle(el);
  return (
    style.display === 'none' ||
    style.visibility === 'hidden' ||
    style.opacity === '0' ||
    el.offsetWidth === 0 ||
    el.offsetHeight === 0
  );
}

function extractPageLinks(): { links: ExtractedLink[]; hasUpiLink: boolean } {
  const links: ExtractedLink[] = [];
  let hasUpiLink = false;
  const currentHost = window.location.hostname;

  const anchorElements = document.querySelectorAll<HTMLAnchorElement>('a[href]');
  const maxLinks = Math.min(anchorElements.length, 100);

  for (let i = 0; i < maxLinks; i++) {
    const a = anchorElements[i];
    const href = a.href;
    const isUpi = href.startsWith('upi://');

    if (isUpi) hasUpiLink = true;

    let isExternal = false;
    try {
      const linkHost = new URL(href).hostname;
      isExternal = linkHost !== currentHost;
    } catch {
      isExternal = false;
    }

    links.push({
      href,
      text: (a.textContent || '').trim().substring(0, 100),
      is_external: isExternal,
      is_upi: isUpi
    });
  }

  return { links, hasUpiLink };
}

function extractPageForms(): { forms: ExtractedForm[]; hasPasswordInput: boolean } {
  const forms: ExtractedForm[] = [];
  let hasPasswordInput = false;

  const formElements = document.querySelectorAll<HTMLFormElement>('form');
  formElements.forEach((form) => {
    const action = form.action || window.location.href;
    const method = (form.method || 'GET').toUpperCase();
    const isInsecureHttp = action.startsWith('http:');

    const fields: ExtractedFormField[] = [];
    const inputs = form.querySelectorAll<HTMLInputElement | HTMLTextAreaElement>('input, textarea');

    inputs.forEach((input) => {
      const type = (input.getAttribute('type') || 'text').toLowerCase();
      const name = input.name || input.id || '';
      const placeholder = input.placeholder || '';
      const isSensitive = SENSITIVE_INPUT_TYPES.has(type) || SENSITIVE_NAME_REGEX.test(name);

      if (type === 'password') hasPasswordInput = true;

      // PRIVACY CONTROL: Never extract value attribute for passwords or sensitive inputs
      fields.push({
        name,
        type,
        placeholder: placeholder.substring(0, 50),
        is_sensitive: isSensitive
      });
    });

    forms.push({
      action,
      method,
      is_insecure_http: isInsecureHttp,
      fields
    });
  });

  return { forms, hasPasswordInput };
}
