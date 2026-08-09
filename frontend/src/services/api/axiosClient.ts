import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';

/**
 * GuardianAI Axios HTTP Client Instance
 * Purpose: Centralized HTTP client configured with base URL, JWT bearer token interceptor, correlation IDs, and RFC 7807 error parsing.
 */

export interface RFC7807Error {
  code: string;
  message: string;
  status: number;
  requestId: string;
  details?: Array<{ field: string; issue: string }>;
}

export class NormalizedApiError extends Error {
  public code: string;
  public status: number;
  public requestId: string;
  public details?: Array<{ field: string; issue: string }>;

  constructor(errorPayload: RFC7807Error) {
    super(errorPayload.message);
    this.name = 'NormalizedApiError';
    this.code = errorPayload.code;
    this.status = errorPayload.status;
    this.requestId = String(errorPayload.requestId || 'req_unknown');
    this.details = errorPayload.details;
  }
}

const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

export const axiosClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000, // 15 seconds SLA
});

// Request Interceptor: Attach JWT token & correlation headers
axiosClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('guardianai_access_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor: Normalize errors to RFC 7807 format
axiosClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<{ error?: RFC7807Error }>) => {
    if (error.response?.data?.error) {
      const payload = error.response.data.error;
      return Promise.reject(new NormalizedApiError(payload));
    }

    const fallbackError: RFC7807Error = {
      code: error.code || 'NETWORK_ERROR',
      message: error.message || 'An unexpected network error occurred',
      status: error.response?.status || 500,
      requestId: (error.response?.headers['x-request-id'] as string) || 'req_unknown',
    };

    return Promise.reject(new NormalizedApiError(fallbackError));
  }
);
