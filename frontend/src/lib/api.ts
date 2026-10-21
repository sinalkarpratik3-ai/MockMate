export class ApiError extends Error {
  status: number;
  data: any;

  constructor(status: number, message: string, data?: any) {
    super(message);
    this.status = status;
    this.data = data;
  }
}

export function getApiBaseUrl(): string {
  // 1. Runtime script variable injected by RootLayout SSR inside container
  if (typeof window !== "undefined" && (window as any).__MOCKMATE_API_URL__) {
    const runtimeUrl = String((window as any).__MOCKMATE_API_URL__).trim();
    if (runtimeUrl.length > 0 && !runtimeUrl.includes("localhost:8000")) {
      return runtimeUrl.endsWith("/api") ? runtimeUrl : `${runtimeUrl.replace(/\/+$/, "")}/api`;
    }
  }

  // 2. Build-time environment variable
  const envUrl = process.env.NEXT_PUBLIC_API_URL;
  if (envUrl && envUrl.trim().length > 0) {
    const trimmed = envUrl.trim();
    const isRemote =
      typeof window !== "undefined" &&
      window.location.hostname !== "localhost" &&
      window.location.hostname !== "127.0.0.1";
    if (!isRemote || !trimmed.includes("localhost:8000")) {
      return trimmed.endsWith("/api") ? trimmed : `${trimmed.replace(/\/+$/, "")}/api`;
    }
  }

  // 3. Smart Render hostname mapping:
  // When running on Render (e.g. mockmate-frontend.onrender.com), automatically point to mockmate-backend
  if (typeof window !== "undefined" && window.location.hostname.endsWith(".onrender.com")) {
    const currentHost = window.location.hostname;
    let backendHost = currentHost.replace("-frontend", "-backend").replace("frontend", "backend");
    if (backendHost === currentHost) {
      backendHost = "mockmate-backend.onrender.com";
    }
    return `https://${backendHost}/api`;
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

  try {
    const response = await fetch(url, {
      ...options,
      headers,
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
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(500, error.message || "Network connection error");
  }
}

