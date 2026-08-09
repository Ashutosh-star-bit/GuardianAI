/**
 * GuardianAI Extension Security & DOM Sanitizer Module
 * Purpose: Strict XSS Prevention, Message Origin Validation, and Input Sanitization:
 *          1. Safe HTML Entity Escaping (Prevents XSS Injection)
 *          2. Extension Message Sender Origin Validation (sender.id === chrome.runtime.id)
 *          3. Safe Text Truncation and URL Origin Validation.
 */

export class ExtensionSecuritySanitizer {
  /**
   * Safely escapes HTML special characters to prevent DOM-based XSS attacks.
   */
  public static escapeHtml(rawStr: string): string {
    if (!rawStr) return '';
    return rawStr
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  /**
   * Validates that incoming extension runtime messages originate strictly from this Extension ID.
   */
  public static isMessageOriginTrusted(sender: chrome.runtime.MessageSender): boolean {
    if (!sender || !sender.id) return false;
    return sender.id === chrome.runtime.id;
  }

  /**
   * Validates if target string is a valid HTTP / HTTPS web URL.
   */
  public static isValidWebUrl(urlStr: string): boolean {
    try {
      const parsed = new URL(urlStr);
      return parsed.protocol === 'http:' || parsed.protocol === 'https:';
    } catch {
      return false;
    }
  }

  /**
   * Sanitizes text strings by stripping null bytes and ASCII control characters.
   */
  public static sanitizeStringInput(inputStr: string, maxLength: number = 10000): string {
    if (!inputStr) return '';
    // Strip null bytes and control characters
    const clean = inputStr.replace(/[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]/g, '');
    return clean.trim().substring(0, maxLength);
  }
}
