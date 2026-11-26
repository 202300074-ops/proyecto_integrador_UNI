-- Sak P'o' Kaab - datos de demostración
-- Productos y variantes iniciales del Sprint 1.

USE melipona;

SET NAMES utf8mb4;

INSERT INTO products
  (id, slug, name, description, story, category, base_price, has_ar, active)
VALUES
  (
    1,
    'miel-de-melipona',
    'Miel de melipona',
    'Producto conceptual inspirado en la miel de abeja sin aguijón y el manejo tradicional en jobones. Perfil floral ilustrativo; no es un producto comercial.',
    'Melipona beecheii, xunan kaab, forma parte de la meliponicultura yucateca. Esta ficha pertenece a un caso académico simulado y no documenta una cosecha real.',
    'honey',
    320.00,
    1,
    1
  ),
  (
    2,
    'jabon-sak-po',
    'Jabón Sak P''o''',
    'Propuesta conceptual de jabón con miel de melipona y aceites vegetales. Sus características son ilustrativas; no se fabrica ni se comercializa.',
    'Sak P''o'' significa jabón en maya yucateco. En este catálogo simulado, el producto representa una idea de diseño y no un lote real.',
    'soap',
    95.00,
    1,
    1
  ),
  (
    3,
    'balsamo-xunan',
    'Bálsamo labial Xunán',
    'Concepto de bálsamo labial inspirado en la cera de melipona y manteca de cacao. Formulación ilustrativa, no comercial.',
    'Xunán es una referencia a la abeja melipona. Este producto es conceptual y no se fabricó ni se probó sobre personas.',
    'cosmetic',
    120.00,
    0,
    1
  ),
  (
    4,
    'vela-jobon',
    'Vela Jobón',
    'Concepto de vela decorativa inspirado en el jobón y la cera de melipona. Luz cálida ilustrativa; no corresponde a una vela comercial real.',
    'El jobón es un tronco hueco donde vive la colonia. El diseño de esta vela es una propuesta visual y no atribuye una práctica ceremonial a ninguna comunidad.',
    'candle',
    180.00,
    0,
    1
  );

INSERT INTO product_variants
  (id, product_id, sku, name, price, stock, weight_g, attributes, active)
VALUES
  (1, 1, 'MEL-250', 'Frasco 250 g', 320.00, 24, 250, JSON_OBJECT('presentacion', 'frasco de vidrio'), 1),
  (2, 1, 'MEL-500', 'Frasco 500 g', 580.00, 12, 500, JSON_OBJECT('presentacion', 'frasco de vidrio'), 1),
  (3, 2, 'JAB-MIEL', 'Miel', 95.00, 30, 100, JSON_OBJECT('aroma', 'miel'), 1),
  (4, 2, 'JAB-CACAO', 'Cacao', 105.00, 20, 100, JSON_OBJECT('aroma', 'cacao'), 1),
  (5, 3, 'BAL-10', 'Barra 10 g', 120.00, 25, 10, JSON_OBJECT('acabado', 'natural'), 1),
  (6, 4, 'VEL-200', 'Vela 200 g', 180.00, 15, 200, JSON_OBJECT('mecha', 'algodón'), 1);

INSERT INTO coupons
  (code, type, value, min_subtotal, max_uses, used_count, starts_at, ends_at, active)
VALUES
  ('BIENVENIDA10', 'percent', 10.00, 200.00, 100, 0, NULL, NULL, 1);
