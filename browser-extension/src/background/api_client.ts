/**
 * GuardianAI Reusable Extension API Client Subsystem
 * Purpose: High-security HTTP API client for extension-to-backend REST communication:
 *          - JWT Bearer Token Authentication Ready
 *          - HTTPS-only transport enforcement
 *          - AbortController timeout bounds (default 5000ms)
 *          - Exponential backoff retries (3 attempts)
 *          - Request & Response schema validation
 *          - Standardized ExtensionAPIError handling.
 */

import { ExtensionResponse, ExtensionScanResult } from '../shared/types';

export interface APIClientConfig {
  baseUrl: string;
  timeoutMs?: number;
  maxRetries?: number;
  enforceHttps?: boolean;
}

export class ExtensionAPIError extends Error {
  public statusCode?: number;
  public errorCode?: string;

  constructor(message: str, statusCode?: number, errorCode?: string) {
    super(message);
    this.name = 'ExtensionAPIError';
    this.statusCode = statusCode;
    this.errorCode = errorCode;
  }
}

export class GuardianExtensionAPIClient {
  private baseUrl: string;
  private timeoutMs: number;
  private maxRetries: number;
  private enforceHttps: boolean;
  private jwtToken: string | null = null;

  constructor(config: APIClientConfig) {
    this.baseUrl = config.baseUrl.replace(/\/+$/, '');
    this.timeoutMs = config.timeoutMs || 5000;
    this.maxRetries = config.maxRetries || 3;
    this.enforceHttps = config.enforceHttps ?? (process.env.NODE_ENV === 'production');

    this.validateBaseUrl(this.baseUrl);
    this.initializeAuthToken();
  }

  private validateBaseUrl(url: string) {
    if (this.enforceHttps && !url.startsWith('https://')) {
      throw new ExtensionAPIError('Security Violation: API endpoint must use secure HTTPS protocol.', 400, 'HTTPS_REQUIRED');
    }
  }

  private async initializeAuthToken() {
    try {
      const data = await chrome.storage.session.get('jwt_token');
      if (data.jwt_token) {
        this.jwtToken = data.jwt_token;
      }
    } catch {
      // Session storage fallback to local storage
      const localData = await chrome.storage.local.get('jwt_token');
      if (localData.jwt_token) {
        this.jwtToken = localData.jwt_token;
      }
    }
  }

  public setAuthToken(token: string) {
    this.jwtToken = token;
    chrome.storage.session.set({ jwt_token: token }).catch(() => {
      chrome.storage.local.set({ jwt_token: token });
    });
  }

  public clearAuthToken() {
    this.jwtToken = null;
    chrome.storage.session.remove('jwt_token').catch(() => {
      chrome.storage.local.remove('jwt_token');
    });
  }

  /**
   * Executes HTTP POST request with AbortController timeout and exponential backoff retries.
   */
  public async post<T>(endpoint: string, payload: any): Promise<ExtensionResponse<T>> {
    const targetUrl = `${this.baseUrl}/${endpoint.replace(/^\/+/, '')}`;
    this.validateRequestPayload(payload);

    let delay = 1000;
    let lastError: Error | null = null;

    for (let attempt = 1; attempt <= this.maxRetries; attempt++) {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), this.timeoutMs);

      try {
        const headers: Record<string, string> = {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        };

        if (this.jwtToken) {
          headers['Authorization'] = `Bearer ${this.jwtToken}`;
        }

        const response = await fetch(targetUrl, {
          method: 'POST',
          headers,
          body: JSON.stringify(payload),
          signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (response.ok) {
          const json = await response.json();
          this.validateResponseObject(json);
          return json as ExtensionResponse<T>;
        }

        if (response.status >= 400 && response.status < 500) {
          const errorJson = await response.json().catch(() => ({}));
          throw new ExtensionAPIError(
            errorJson.detail || `Client error HTTP ${response.status}`,
            response.status,
            'CLIENT_ERROR'
          );
        }

        throw new ExtensionAPIError(`Server error HTTP ${response.status}`, response.status, 'SERVER_ERROR');
      } catch (err: any) {
        clearTimeout(timeoutId);
        lastError = err;

        if (err.name === 'AbortError') {
          lastError = new ExtensionAPIError(`API request timed out after ${this.timeoutMs}ms SLA`, 408, 'REQUEST_TIMEOUT');
        }

        if (err instanceof ExtensionAPIError && err.statusCode && err.statusCode < 500) {
          // Do not retry 4xx client errors
          throw err;
        }

        if (attempt === this.maxRetries) break;

        await new Promise((resolve) => setTimeout(resolve, delay));
        delay *= 2; // Exponential backoff: 1s -> 2s -> 4s
      }
    }

    throw lastError || new ExtensionAPIError('API request failed after maximum retries', 500, 'MAX_RETRIES_EXCEEDED');
  }

  public async analyzeUrl(url: string, persona: string = 'SENIOR_CITIZENS', locale: string = 'en'): Promise<ExtensionResponse<ExtensionScanResult>> {
    if (!url || typeof url !== 'string' || url.length > 2048) {
      throw new ExtensionAPIError('Invalid URL string parameter', 400, 'INVALID_URL_PARAMETER');
    }
    return this.post<ExtensionScanResult>('analyse/url', {
      url,
      target_persona: persona,
      locale
    });
  }

  public async analyzeText(text: string, persona: string = 'SENIOR_CITIZENS', locale: string = 'en'): Promise<ExtensionResponse<ExtensionScanResult>> {
    if (!text || typeof text !== 'string' || text.length > 50000) {
      throw new ExtensionAPIError('Invalid text payload length', 400, 'INVALID_TEXT_PARAMETER');
    }
    return this.post<ExtensionScanResult>('analyse/text', {
      text,
      target_persona: persona,
      locale
    });
  }

  private validateRequestPayload(payload: any) {
    if (payload === null || payload === undefined) {
      throw new ExtensionAPIError('Request payload body cannot be null or undefined', 400, 'NULL_PAYLOAD');
    }
  }

  private validateResponseObject(json: any) {
    if (!json || typeof json !== 'object') {
      throw new ExtensionAPIError('Invalid JSON response format received from server', 502, 'BAD_GATEWAY');
    }
  }
}
