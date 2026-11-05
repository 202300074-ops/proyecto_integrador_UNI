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
    'Miel de abeja sin aguijón, cosechada en jobones tradicionales. Notas florales, acidez suave y textura ligera.',
    'La Melipona beecheii, xunan kaab, ha sido criada por comunidades mayas durante siglos. Su miel se obtiene sin aguijón y con un manejo cuidadoso del jobón.',
    'honey',
    320.00,
    1,
    1
  ),
  (
    2,
    'jabon-sak-po',
    'Jabón Sak P''o''',
    'Jabón artesanal con miel de melipona y aceites vegetales. Limpia sin resecar y conserva el aroma de la colmena.',
    'Sak P''o'' significa jabón en maya yucateco. Cada barra se elabora en lotes pequeños con miel de la cooperativa.',
    'soap',
    95.00,
    1,
    1
  ),
  (
    3,
    'balsamo-xunan',
    'Bálsamo labial Xunán',
    'Bálsamo nutritivo con cera de melipona y manteca de cacao. Protección suave para labios secos.',
    'Xunán es la señora abeja: la melipona. La cera de sus jobones sella la humedad sin sensación grasa.',
    'cosmetic',
    120.00,
    0,
    1
  ),
  (
    4,
    'vela-jobon',
    'Vela Jobón',
    'Vela de cera de melipona con mecha de algodón. Luz cálida y aroma natural a miel y madera.',
    'El jobón es el tronco hueco donde vive la colmena. Esta vela recupera la memoria de la cera ceremonial maya.',
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
