import { randomBytes } from 'node:crypto';
import { Router } from 'express';
import { z } from 'zod';
import { pool } from '../db.js';
import { config } from '../env.js';

const router = Router();

const couponSchema = z.object({
  code: z.string().trim().min(1).max(40),
  subtotal: z.number().finite().nonnegative()
});

const orderSchema = z.object({
  customerName: z.string().trim().min(2).max(140),
  email: z.string().trim().email().max(180),
  phone: z.string().trim().max(30).optional().nullable(),
  shippingAddress: z.string().trim().min(5).max(255),
  city: z.string().trim().min(2).max(120),
  state: z.string().trim().min(2).max(120),
  postalCode: z.string().trim().min(4).max(12),
  couponCode: z.string().trim().max(40).optional().nullable(),
  items: z.array(z.object({
    variantId: z.number().int().positive(),
    quantity: z.number().int().min(1).max(99)
  })).min(1).max(30)
});

class CommerceError extends Error {
  constructor(status, code) {
    super(code);
    this.status = status;
    this.code = code;
  }
}

function money(value) {
  return Math.round((Number(value) + Number.EPSILON) * 100) / 100;
}

function calculateDiscount(coupon, subtotal) {
  const value = Number(coupon.value);
  const discount = coupon.type === 'percent'
    ? subtotal * (value / 100)
    : value;
  return money(Math.min(subtotal, discount));
}

function assertCouponUsable(coupon, subtotal) {
  if (!coupon || !coupon.active) throw new CommerceError(400, 'coupon_unavailable');
  if (coupon.starts_at && new Date(coupon.starts_at).getTime() > Date.now()) {
    throw new CommerceError(400, 'coupon_not_started');
  }
  if (coupon.ends_at && new Date(coupon.ends_at).getTime() < Date.now()) {
    throw new CommerceError(400, 'coupon_expired');
  }
  if (coupon.max_uses !== null && Number(coupon.used_count) >= Number(coupon.max_uses)) {
    throw new CommerceError(400, 'coupon_limit_reached');
  }
  if (subtotal < Number(coupon.min_subtotal)) {
    throw new CommerceError(400, 'coupon_minimum_not_met');
  }
}

async function findCoupon(executor, code, { lock = false } = {}) {
  const lockClause = lock ? ' FOR UPDATE' : '';
  const [rows] = await executor.query(
    `SELECT id, code, type, value, min_subtotal, max_uses, used_count,
            starts_at, ends_at, active
     FROM coupons WHERE code = ? LIMIT 1${lockClause}`,
    [code.trim().toUpperCase()]
  );
  return rows[0] ?? null;
}

router.post('/coupons/validate', async (req, res, next) => {
  const parsed = couponSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({ error: 'invalid_request' });
  }

  try {
    const { code, subtotal } = parsed.data;
    const coupon = await findCoupon(pool, code);
    assertCouponUsable(coupon, subtotal);

    res.json({
      data: {
        code: coupon.code,
        type: coupon.type,
        value: Number(coupon.value),
        minSubtotal: Number(coupon.min_subtotal),
        discount: calculateDiscount(coupon, subtotal)
      }
    });
  } catch (error) {
    if (error instanceof CommerceError) {
      return res.status(error.status).json({ error: error.code });
    }
    next(error);
  }
});

router.post('/orders', async (req, res, next) => {
  const parsed = orderSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({ error: 'invalid_request' });
  }

  let connection;
  let transactionStarted = false;
  try {
    connection = await pool.getConnection();
    await connection.beginTransaction();
    transactionStarted = true;

    const { items: requestedItems } = parsed.data;
    const quantities = new Map();
    for (const item of requestedItems) {
      quantities.set(item.variantId, (quantities.get(item.variantId) ?? 0) + item.quantity);
    }
    const variantIds = [...quantities.keys()];
    const placeholders = variantIds.map(() => '?').join(', ');
    const [variants] = await connection.query(
      `SELECT v.id, v.product_id, v.name AS variant_name, v.sku, v.price, v.stock,
              p.name AS product_name
       FROM product_variants v
       INNER JOIN products p ON p.id = v.product_id
       WHERE v.id IN (${placeholders}) AND v.active = 1 AND p.active = 1
       FOR UPDATE`,
      variantIds
    );

    if (variants.length !== variantIds.length) {
      throw new CommerceError(409, 'variant_unavailable');
    }

    const variantById = new Map(variants.map((variant) => [Number(variant.id), variant]));
    const orderItems = variantIds.map((variantId) => {
      const variant = variantById.get(variantId);
      const quantity = quantities.get(variantId);
      if (quantity > Number(variant.stock)) {
        throw new CommerceError(409, 'insufficient_stock');
      }
      const unitPrice = money(variant.price);
      return {
        variantId,
        productName: variant.product_name,
        variantName: variant.variant_name,
        unitPrice,
        quantity,
        lineTotal: money(unitPrice * quantity)
      };
    });

    const subtotal = money(orderItems.reduce((sum, item) => sum + item.lineTotal, 0));
    let coupon = null;
    let discount = 0;
    const couponCode = parsed.data.couponCode?.trim().toUpperCase() || null;
    if (couponCode) {
      coupon = await findCoupon(connection, couponCode, { lock: true });
      assertCouponUsable(coupon, subtotal);
      discount = calculateDiscount(coupon, subtotal);
    }

    const shippingCost = 0;
    const total = money(subtotal - discount + shippingCost);
    const orderNumber = `SKP-${Date.now().toString(36).toUpperCase()}-${randomBytes(3).toString('hex').toUpperCase()}`;
    const [orderResult] = await connection.query(
      `INSERT INTO orders
        (order_number, customer_name, email, phone, shipping_address, city, state,
         postal_code, subtotal, discount, shipping_cost, total, coupon_code, status, payment_method)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending', 'mock')`,
      [
        orderNumber,
        parsed.data.customerName,
        parsed.data.email,
        parsed.data.phone || null,
        parsed.data.shippingAddress,
        parsed.data.city,
        parsed.data.state,
        parsed.data.postalCode,
        subtotal,
        discount,
        shippingCost,
        total,
        couponCode
      ]
    );

    for (const item of orderItems) {
      await connection.query(
        `INSERT INTO order_items
          (order_id, variant_id, product_name, variant_name, unit_price, quantity, line_total)
         VALUES (?, ?, ?, ?, ?, ?, ?)`,
        [orderResult.insertId, item.variantId, item.productName, item.variantName, item.unitPrice, item.quantity, item.lineTotal]
      );
      const [stockResult] = await connection.query(
        'UPDATE product_variants SET stock = stock - ? WHERE id = ? AND stock >= ?',
        [item.quantity, item.variantId, item.quantity]
      );
      if (stockResult.affectedRows !== 1) {
        throw new CommerceError(409, 'insufficient_stock');
      }
    }

    if (coupon) {
      await connection.query('UPDATE coupons SET used_count = used_count + 1 WHERE id = ?', [coupon.id]);
      await connection.query(
        'INSERT INTO coupon_redemptions (coupon_id, order_id) VALUES (?, ?)',
        [coupon.id, orderResult.insertId]
      );
    }

    await connection.query(
      `INSERT INTO order_status_history (order_id, status, note)
       VALUES (?, 'pending', 'Pedido de demostración creado.')`,
      [orderResult.insertId]
    );

    await connection.commit();
    transactionStarted = false;
    res.status(201).json({
      data: {
        orderNumber,
        subtotal,
        discount,
        shippingCost,
        total,
        status: 'pending',
        paymentMethod: 'mock',
        items: orderItems
      }
    });
  } catch (error) {
    if (connection && transactionStarted) {
      await connection.rollback().catch(() => {});
    }
    if (error instanceof CommerceError) {
      return res.status(error.status).json({ error: error.code });
    }
    next(error);
  } finally {
    connection?.release();
  }
});

router.get('/orders/demo', async (req, res, next) => {
  if (config.nodeEnv === 'production') {
    return res.status(404).json({ error: 'not_found' });
  }

  try {
    const [rows] = await pool.query(
      `SELECT o.id, o.order_number, o.status, o.total, o.created_at,
              COUNT(oi.id) AS item_count
       FROM orders o
       LEFT JOIN order_items oi ON oi.order_id = o.id
       WHERE o.payment_method = ?
       GROUP BY o.id
       ORDER BY o.created_at DESC, o.id DESC
       LIMIT 25`,
      ['mock']
    );

    res.json({
      data: rows.map((row) => ({
        orderNumber: `…${String(row.order_number).slice(-6)}`,
        status: row.status,
        total: Number(row.total),
        itemCount: Number(row.item_count),
        createdAt: new Date(row.created_at).toISOString()
      }))
    });
  } catch (error) {
    next(error);
  }
});

export default router;
