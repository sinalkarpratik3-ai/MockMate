import test from "node:test";
import assert from "node:assert/strict";
import {
  normalizeApiUrl,
  normalizeEndpoint,
  extractErrorMessage,
  getApiBaseUrl,
} from "../src/lib/api.ts";

test("normalizeApiUrl handles URLs without /api prefix", () => {
  const result = normalizeApiUrl("https://api.mockmate.com");
  assert.equal(result, "https://api.mockmate.com/api");
});

test("normalizeApiUrl preserves existing /api prefix without duplicating", () => {
  const result = normalizeApiUrl("https://api.mockmate.com/api");
  assert.equal(result, "https://api.mockmate.com/api");
});

test("normalizeApiUrl trims trailing slashes", () => {
  const result = normalizeApiUrl("https://api.mockmate.com/api///");
  assert.equal(result, "https://api.mockmate.com/api");
});

test("normalizeApiUrl automatically prepends https to raw domain names", () => {
  const result = normalizeApiUrl("mockmate-alb-123456.us-east-1.elb.amazonaws.com");
  assert.equal(result, "https://mockmate-alb-123456.us-east-1.elb.amazonaws.com/api");
});

test("normalizeApiUrl supports relative paths for same-origin proxy", () => {
  const result = normalizeApiUrl("/api");
  assert.equal(result, "/api");
});

test("normalizeEndpoint prevents duplicate /api prefixes", () => {
  assert.equal(normalizeEndpoint("/auth/register"), "/auth/register");
  assert.equal(normalizeEndpoint("auth/register"), "/auth/register");
  assert.equal(normalizeEndpoint("/api/auth/register"), "/auth/register");
  assert.equal(normalizeEndpoint("api/auth/register"), "/auth/register");
  assert.equal(normalizeEndpoint("/api/auth/login"), "/auth/login");
  assert.equal(normalizeEndpoint("/api/auth/me"), "/auth/me");
});

test("extractErrorMessage parses FastAPI detail strings", () => {
  const msg = extractErrorMessage({ detail: "An account with this email address already exists." }, 400);
  assert.equal(msg, "An account with this email address already exists.");
});

test("extractErrorMessage parses FastAPI Pydantic validation errors", () => {
  const msg = extractErrorMessage({
    detail: [
      { loc: ["body", "password"], msg: "String should have at least 6 characters" },
      { loc: ["body", "email"], msg: "value is not a valid email address" }
    ]
  }, 422);
  assert.match(msg, /password: String should have at least 6 characters/);
  assert.match(msg, /email: value is not a valid email address/);
});

test("extractErrorMessage fallbacks gracefully on empty or primitive data", () => {
  assert.equal(extractErrorMessage(null, 500), "HTTP 500 Request failed");
  assert.equal(extractErrorMessage("Direct error string", 500), "Direct error string");
});

test("getApiBaseUrl defaults to localhost for SSR / Node environment without env", () => {
  const originalEnv = process.env.NEXT_PUBLIC_API_URL;
  delete process.env.NEXT_PUBLIC_API_URL;
  delete process.env.BACKEND_URL;
  delete process.env.BACKEND_INTERNAL_URL;

  const url = getApiBaseUrl();
  assert.equal(url, "http://localhost:8000/api");

  if (originalEnv) process.env.NEXT_PUBLIC_API_URL = originalEnv;
});

test("getApiBaseUrl resolves relative /api for remote browser without localhost leak", () => {
  // Simulate remote browser window
  globalThis.window = {
    location: {
      hostname: "mockmate-alb-123456.us-east-1.elb.amazonaws.com",
      origin: "http://mockmate-alb-123456.us-east-1.elb.amazonaws.com"
    }
  };

  const originalEnv = process.env.NEXT_PUBLIC_API_URL;
  // Even if an env var had localhost:8000 baked in, remote browser must not call localhost
  process.env.NEXT_PUBLIC_API_URL = "http://localhost:8000/api";

  const url = getApiBaseUrl();
  assert.equal(url, "/api");

  // Cleanup
  delete globalThis.window;
  if (originalEnv) {
    process.env.NEXT_PUBLIC_API_URL = originalEnv;
  } else {
    delete process.env.NEXT_PUBLIC_API_URL;
  }
});

test("getApiBaseUrl resolves direct localhost:8000 for local browser development", () => {
  globalThis.window = {
    location: {
      hostname: "localhost",
      origin: "http://localhost:3000"
    }
  };

  const originalEnv = process.env.NEXT_PUBLIC_API_URL;
  delete process.env.NEXT_PUBLIC_API_URL;

  const url = getApiBaseUrl();
  assert.equal(url, "http://localhost:8000/api");

  delete globalThis.window;
  if (originalEnv) process.env.NEXT_PUBLIC_API_URL = originalEnv;
});

