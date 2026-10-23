export interface ErrorDetailItem {
  loc?: (string | number)[];
  msg?: string;
  type?: string;
}

export interface ErrorResponseBody {
  detail?: string | ErrorDetailItem[] | Record<string, unknown>;
  message?: string;
  error?: string;
  [key: string]: unknown;
}

export class ApiError extends Error {
  status: number;
  data: unknown;

  constructor(status: number, message: string, data?: unknown) {
    super(message);
    this.status = status;
    this.data = data;
    this.name = "ApiError";
  }
}

/**
 * Normalizes any backend URL or path into a canonical API base URL ending with '/api'
 * without duplicate prefixes or trailing slashes.
 */
export function normalizeApiUrl(rawUrl: string): string {
  let trimmed = rawUrl.trim().replace(/\/+$/, "");
  if (!trimmed) return "";

  // Relative path (e.g. "/api" or "/custom-api")
  if (trimmed.startsWith("/")) {
    return trimmed.endsWith("/api") ? trimmed : `${trimmed}/api`;
  }

  // Ensure valid HTTP/HTTPS protocol
  if (!trimmed.startsWith("http://") && !trimmed.startsWith("https://")) {
    trimmed = `https://${trimmed}`;
  }

  return trimmed.endsWith("/api") ? trimmed : `${trimmed}/api`;
}

/**
 * Resolves the backend API base URL with priority:
 * 1. Explicit NEXT_PUBLIC_API_URL environment variable (if non-localhost on remote host)
 * 2. Remote browser (e.g. behind AWS ALB with path-based routing): relative '/api'
 * 3. Localhost browser development: 'http://localhost:8000/api'
 * 4. Server-side Next.js runtime fallback: BACKEND_INTERNAL_URL or 'http://localhost:8000/api'
 */
export function getApiBaseUrl(): string {
  const isBrowser = typeof window !== "undefined";
  const isRemoteBrowser =
    isBrowser &&
    window.location.hostname !== "localhost" &&
    window.location.hostname !== "127.0.0.1";

  // 1. Explicit environment variable
  const envUrl = process.env.NEXT_PUBLIC_API_URL;
  if (envUrl && envUrl.trim().length > 0) {
    const trimmed = envUrl.trim();
    if (!isRemoteBrowser || (!trimmed.includes("localhost") && !trimmed.includes("127.0.0.1"))) {
      return normalizeApiUrl(trimmed);
    }
  }

  // 2. Remote browser fallback: use same-origin relative '/api' routed by AWS ALB
  if (isRemoteBrowser) {
    return "/api";
  }

  // 3. Local browser development: direct to local backend port 8000
  if (isBrowser) {
    return "http://localhost:8000/api";
  }

  // 4. Server-side Next.js runtime fallback
  const serverBackend = process.env.BACKEND_INTERNAL_URL || process.env.BACKEND_URL;
  if (serverBackend && serverBackend.trim().length > 0) {
    return normalizeApiUrl(serverBackend);
  }

  return "http://localhost:8000/api";
}

/**
 * Normalizes an API endpoint to ensure no duplicate '/api' prefix
 */
export function normalizeEndpoint(endpoint: string): string {
  // Strip any leading slashes and optional leading 'api/'
  const cleaned = endpoint.trim().replace(/^\/+/, "").replace(/^api\/?/i, "");
  return `/${cleaned}`;
}

export function extractErrorMessage(data: unknown, status: number): string {
  if (!data) return `HTTP ${status} Request failed`;
  if (typeof data === "string") return data;
  
  if (typeof data === "object" && data !== null) {
    const obj = data as ErrorResponseBody;
    if (typeof obj.detail === "string") return obj.detail;
    if (Array.isArray(obj.detail)) {
      const messages = obj.detail
        .map((item: unknown) => {
          if (typeof item === "string") return item;
          if (item && typeof item === "object") {
            const detailItem = item as ErrorDetailItem;
            const field =
              Array.isArray(detailItem.loc) && detailItem.loc.length > 1
                ? `${detailItem.loc[detailItem.loc.length - 1]}: `
                : "";
            return `${field}${detailItem.msg || JSON.stringify(item)}`;
          }
          return String(item);
        })
        .filter(Boolean);
      if (messages.length > 0) {
        return messages.join("; ");
      }
    }
    if (typeof obj.message === "string") return obj.message;
    if (typeof obj.error === "string") return obj.error;
  }

  return `HTTP ${status} Request failed`;
}

export async function apiRequest<T = unknown>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = typeof window !== "undefined" ? localStorage.getItem("mockmate_token") : null;

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  if (token) {
    (headers as Record<string, string>)["Authorization"] = `Bearer ${token}`;
  }

  const baseUrl = getApiBaseUrl().replace(/\/+$/, "");
  const cleanEndpoint = normalizeEndpoint(endpoint);
  const url = `${baseUrl}${cleanEndpoint}`;

  const controller = new AbortController();
  const timeoutMs = 30000;
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);
  const signal = options.signal || controller.signal;

  try {
    const response = await fetch(url, {
      ...options,
      headers,
      signal,
    });

    if (response.status === 204) {
      return {} as T;
    }

    const data: unknown = await response.json().catch(() => ({}));

    if (!response.ok) {
      const errorMsg = extractErrorMessage(data, response.status);
      throw new ApiError(response.status, errorMsg, data);
    }

    return data as T;
  } catch (error: unknown) {
    if (error instanceof Error && error.name === "AbortError") {
      throw new ApiError(
        408,
        `Connection timed out reaching ${url}. The server took longer than 30 seconds to respond. Please verify that the backend is running and reachable, then retry.`
      );
    }
    if (error instanceof ApiError) {
      throw error;
    }
    const message = error instanceof Error ? error.message : "Network connection error";
    throw new ApiError(500, message);
  } finally {
    clearTimeout(timeoutId);
  }
}


