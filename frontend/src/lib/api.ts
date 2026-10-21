export class ApiError extends Error {
  status: number;
  data: any;

  constructor(status: number, message: string, data?: any) {
    super(message);
    this.status = status;
    this.data = data;
  }
}

export function normalizeApiUrl(rawUrl: string): string {
  let trimmed = rawUrl.trim().replace(/\/+$/, "");
  if (!trimmed) return "";
  if (!trimmed.startsWith("http://") && !trimmed.startsWith("https://")) {
    trimmed = `https://${trimmed}`;
  }
  return trimmed.endsWith("/api") ? trimmed : `${trimmed}/api`;
}

export function getApiBaseUrl(): string {
  const isBrowser = typeof window !== "undefined";
  const isRemoteBrowser =
    isBrowser &&
    window.location.hostname !== "localhost" &&
    window.location.hostname !== "127.0.0.1";

  // 1. Runtime script variable injected by RootLayout SSR inside container
  if (isBrowser && (window as any).__MOCKMATE_API_URL__) {
    const runtimeUrl = String((window as any).__MOCKMATE_API_URL__).trim();
    if (runtimeUrl.length > 0) {
      if (!isRemoteBrowser || (!runtimeUrl.includes("localhost") && !runtimeUrl.includes("127.0.0.1"))) {
        return normalizeApiUrl(runtimeUrl);
      }
    }
  }

  // 2. Build-time environment variable
  const envUrl = process.env.NEXT_PUBLIC_API_URL || process.env.BACKEND_URL;
  if (envUrl && envUrl.trim().length > 0) {
    const trimmed = envUrl.trim();
    if (!isRemoteBrowser || (!trimmed.includes("localhost") && !trimmed.includes("127.0.0.1"))) {
      return normalizeApiUrl(trimmed);
    }
  }

  // 3. Remote browser fallback: use same-origin /api proxied by Next.js server rewrites
  if (isRemoteBrowser) {
    return `${window.location.origin}/api`;
  }

  // 4. Default to localhost for local development
  return "http://localhost:8000/api";
}

export function extractErrorMessage(data: any, status: number): string {
  if (!data) return `HTTP ${status} Request failed`;
  if (typeof data === "string") return data;
  if (typeof data.detail === "string") return data.detail;
  if (Array.isArray(data.detail)) {
    const messages = data.detail
      .map((item: any) => {
        if (typeof item === "string") return item;
        if (item && typeof item.msg === "string") {
          const field =
            Array.isArray(item.loc) && item.loc.length > 1
              ? `${item.loc[item.loc.length - 1]}: `
              : "";
          return `${field}${item.msg}`;
        }
        return JSON.stringify(item);
      })
      .filter(Boolean);
    if (messages.length > 0) {
      return messages.join("; ");
    }
  }
  if (typeof data.message === "string") return data.message;
  if (typeof data.error === "string") return data.error;
  return `HTTP ${status} Request failed`;
}

export async function apiRequest<T = any>(
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

  const baseUrl = getApiBaseUrl();
  const cleanEndpoint = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
  const url = `${baseUrl}${cleanEndpoint}`;

  const controller = new AbortController();
  const timeoutMs = 20000;
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

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      const errorMsg = extractErrorMessage(data, response.status);
      throw new ApiError(response.status, errorMsg, data);
    }

    return data as T;
  } catch (error: any) {
    if (error?.name === "AbortError") {
      throw new ApiError(408, `Connection timed out reaching ${url}. On Render free tier, services may take ~30–50s to wake up. Please retry.`);
    }
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(500, error.message || "Network connection error");
  } finally {
    clearTimeout(timeoutId);
  }
}

