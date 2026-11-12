import assert from 'node:assert/strict';
import { pool } from '../src/db.js';

const api = process.env.API_BASE ?? 'http://localhost:3000/api';
const email = `commerce-smoke-${Date.now()}@sakpokaab.test`;
const customer = {
  customerName: 'Cliente de prueba',
  email,
  phone: null,
  shippingAddress: 'Calle de Prueba 123',
  city: 'Valladolid',
  state: 'Yucatán',
  postalCode: '97780'
};

async function post(path, body) {
  const response = await fetch(`${api}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  return { response, body: await response.json() };
}

let connection;
try {
  const productsResponse = await fetch(`${api}/products`);
  assert.equal(productsResponse.status, 200, 'catálogo debe responder 200');
  const { data: products } = await productsResponse.json();
  const variant = products.flatMap((product) => product.variants.map((item) => ({
    ...item,
    productName: product.name
  }))).find((item) => Number(item.price) >= 200 && Number(item.stock) > 1);
  assert.ok(variant, 'debe existir una variante con stock y subtotal elegible');

  const lowCoupon = await post('/coupons/validate', {
    code: 'BIENVENIDA10',
    subtotal: 150
  });
  assert.equal(lowCoupon.response.status, 400);
  assert.equal(lowCoupon.body.error, 'coupon_minimum_not_met');

  const subtotal = Number(variant.price);
  const coupon = await post('/coupons/validate', { code: 'BIENVENIDA10', subtotal });
  assert.equal(coupon.response.status, 200);
  assert.equal(coupon.body.data.discount, Math.round(subtotal * 0.1 * 100) / 100);

  const overStock = await post('/orders', {
    ...customer,
    couponCode: null,
    items: [{ variantId: Number(variant.id), quantity: Number(variant.stock) + 1 }]
  });
  assert.equal(overStock.response.status, 409);
  assert.equal(overStock.body.error, 'insufficient_stock');

  const order = await post('/orders', {
    ...customer,
    couponCode: 'BIENVENIDA10',
    items: [{ variantId: Number(variant.id), quantity: 1 }]
  });
  assert.equal(order.response.status, 201);
  assert.equal(order.body.data.subtotal, subtotal);
  assert.equal(order.body.data.discount, coupon.body.data.discount);
  assert.equal(order.body.data.total, subtotal - coupon.body.data.discount);
  assert.equal(order.body.data.paymentMethod, 'mock');
  assert.equal(order.body.data.items[0].productName, variant.productName);

  console.log(`COMMERCE_SMOKE_OK: coupon, minimum, stock lock, order ${order.body.data.orderNumber}.`);
} finally {
  try {
    connection = await pool.getConnection();
    await connection.beginTransaction();
    const [orders] = await connection.query(
      'SELECT id, coupon_code FROM orders WHERE email = ? ORDER BY id DESC LIMIT 1 FOR UPDATE',
      [email]
    );
    const order = orders[0];
    if (order) {
      const [items] = await connection.query(
        'SELECT variant_id, quantity FROM order_items WHERE order_id = ?',
        [order.id]
      );
      for (const item of items) {
        await connection.query(
          'UPDATE product_variants SET stock = stock + ? WHERE id = ?',
          [item.quantity, item.variant_id]
        );
      }
      if (order.coupon_code) {
        await connection.query(
          'UPDATE coupons SET used_count = GREATEST(used_count - 1, 0) WHERE code = ?',
          [order.coupon_code]
        );
      }
      await connection.query('DELETE FROM orders WHERE id = ?', [order.id]);
    }
    await connection.commit();
  } catch (error) {
    if (connection) await connection.rollback().catch(() => {});
    throw error;
  } finally {
    connection?.release();
    await pool.end();
  }
}
