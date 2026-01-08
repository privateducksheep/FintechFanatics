import { API_BASE_URL } from "./config";

function safeJson(text: string) {
  try {
    return JSON.parse(text);
  } catch {
    return { raw: text };
  }
}

export async function apiGet(path: string, token?: string) {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });
  const text = await res.text();
  if (!res.ok) throw new Error(text || "Request failed");
  return safeJson(text);
}

export async function apiPost(path: string, body?: any, token?: string) {
    console.log("API_BASE_URL =", API_BASE_URL);
    
    const url = `${API_BASE_URL}${path}`;
    console.log("FETCHING:", url, "BODY:", body);
  
    try {
      const res = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: body ? JSON.stringify(body) : undefined,
      });
  
      console.log("STATUS:", res.status);
  
      const text = await res.text();
      console.log("BODY:", text);
  
      if (!res.ok) {
        throw new Error(text || `Request failed (${res.status})`);
      }
  
      return text ? JSON.parse(text) : null;
    } catch (e) {
      console.log("NETWORK ERROR:", e);
      throw e;
    }
  }
