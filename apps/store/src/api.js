const API_BASE = import.meta.env.VITE_API_BASE ?? '/api';

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      ...(options.body ? { 'Content-Type': 'application/json' } : {}),
      ...options.headers
    }
  });
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

export async function validateCoupon(code, subtotal) {
  return request('/coupons/validate', {
    method: 'POST',
    body: JSON.stringify({ code, subtotal })
  });
}

export async function createOrder(order) {
  return request('/orders', {
    method: 'POST',
    body: JSON.stringify(order)
  });
}
