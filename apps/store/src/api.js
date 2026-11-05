const API_BASE = import.meta.env.VITE_API_BASE ?? '/api';

async function request(path) {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.error ?? `Error ${response.status}`);
  }
  return response.json();
}

export async function getProducts() {
  const { data } = await request('/products');
  return data;
}

export async function getHealth() {
  return request('/health');
}
