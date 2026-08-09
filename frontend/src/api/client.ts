/**
 * GuardianAI Typed API Service Layer Client
 * Purpose: Provides a lightweight, typed fetch wrapper handling headers, base URLs, error parsing (RFC 7807 format), and JWT injection.
 */

export interface ApiErrorResponse {
  code: string;
  message: string;
  status: number;
  details?: Array<{ field: string; issue: string }>;
}

export class ApiError extends Error {
  public status: number;
  public code: string;
  public details?: Array<{ field: string; issue: string }>;

  constructor(errorResponse: ApiErrorResponse) {
    super(errorResponse.message);
    this.name = 'ApiError';
    this.status = errorResponse.status;
    this.code = errorResponse.code;
    this.details = errorResponse.details;
  }
}

const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem('guardianai_access_token');
  
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(options.headers || {}),
  };

  const config: RequestInit = {
    ...options,
    headers,
  };

  const response = await fetch(`${BASE_URL}${endpoint}`, config);

  if (!response.ok) {
    let errorData: ApiErrorResponse;
    try {
      const json = await response.json();
      errorData = json.error || {
        code: 'HTTP_ERROR',
        message: response.statusText || 'An unexpected API error occurred',
        status: response.status,
      };
    } catch {
      errorData = {
        code: 'NETWORK_ERROR',
        message: 'Failed to parse error response from server',
        status: response.status,
      };
    }
    throw new ApiError(errorData);
  }

  return response.json() as Promise<T>;
}

export const apiClient = {
  get: <T>(endpoint: string, options?: RequestInit) => request<T>(endpoint, { ...options, method: 'GET' }),
  post: <T>(endpoint: string, body?: unknown, options?: RequestInit) =>
    request<T>(endpoint, { ...options, method: 'POST', body: JSON.stringify(body) }),
  put: <T>(endpoint: string, body?: unknown, options?: RequestInit) =>
    request<T>(endpoint, { ...options, method: 'PUT', body: JSON.stringify(body) }),
  delete: <T>(endpoint: string, options?: RequestInit) => request<T>(endpoint, { ...options, method: 'DELETE' }),
};
