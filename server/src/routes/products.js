import { Router } from 'express';
import { pool } from '../db.js';

const router = Router();

const PRODUCT_COLUMNS = `
  id, slug, name, description, story, category, base_price, has_ar, active
`;

const VARIANT_COLUMNS = `
  id, product_id, sku, name, price, stock, weight_g, attributes, active
`;

function normalizeProduct(product, variants) {
  return {
    ...product,
    has_ar: Boolean(product.has_ar),
    active: Boolean(product.active),
    variants: variants.map((variant) => ({
      ...variant,
      active: Boolean(variant.active)
    }))
  };
}

router.get('/', async (req, res, next) => {
  try {
    const [products] = await pool.query(
      `SELECT ${PRODUCT_COLUMNS} FROM products WHERE active = 1 ORDER BY id ASC`
    );
    const [variants] = await pool.query(
      `SELECT ${VARIANT_COLUMNS} FROM product_variants WHERE active = 1 ORDER BY id ASC`
    );

    const variantsByProduct = new Map();
    for (const variant of variants) {
      const list = variantsByProduct.get(variant.product_id) ?? [];
      list.push(variant);
      variantsByProduct.set(variant.product_id, list);
    }

    const data = products.map((product) =>
      normalizeProduct(product, variantsByProduct.get(product.id) ?? [])
    );

    res.json({ data });
  } catch (error) {
    next(error);
  }
});

router.get('/:slug', async (req, res, next) => {
  try {
    const [products] = await pool.query(
      `SELECT ${PRODUCT_COLUMNS} FROM products WHERE slug = ? AND active = 1 LIMIT 1`,
      [req.params.slug]
    );

    const product = products[0];
    if (!product) {
      return res.status(404).json({ error: 'product_not_found' });
    }

    const [variants] = await pool.query(
      `SELECT ${VARIANT_COLUMNS} FROM product_variants WHERE product_id = ? AND active = 1 ORDER BY id ASC`,
      [product.id]
    );

    res.json({ data: normalizeProduct(product, variants) });
  } catch (error) {
    next(error);
  }
});

export default router;
