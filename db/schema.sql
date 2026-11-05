-- Sak P'o' Kaab - esquema de base de datos
-- MySQL 8.4 LTS
-- Este archivo se ejecuta automaticamente la primera vez que se crea el contenedor.

CREATE DATABASE IF NOT EXISTS melipona
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE melipona;

SET NAMES utf8mb4;

CREATE TABLE IF NOT EXISTS users (
  id            INT UNSIGNED NOT NULL AUTO_INCREMENT,
  name          VARCHAR(120) NOT NULL,
  email         VARCHAR(180) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role          ENUM('admin', 'customer') NOT NULL DEFAULT 'customer',
  created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_users_email (email)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS products (
  id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
  slug        VARCHAR(140) NOT NULL,
  name        VARCHAR(160) NOT NULL,
  description TEXT NOT NULL,
  story       TEXT NULL,
  category    ENUM('honey', 'soap', 'cosmetic', 'candle') NOT NULL,
  base_price  DECIMAL(10, 2) NOT NULL,
  has_ar      TINYINT(1) NOT NULL DEFAULT 0,
  active      TINYINT(1) NOT NULL DEFAULT 1,
  created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_products_slug (slug),
  KEY idx_products_category (category),
  KEY idx_products_active (active)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS product_variants (
  id         INT UNSIGNED NOT NULL AUTO_INCREMENT,
  product_id INT UNSIGNED NOT NULL,
  sku        VARCHAR(64) NOT NULL,
  name       VARCHAR(120) NOT NULL,
  price      DECIMAL(10, 2) NOT NULL,
  stock      INT UNSIGNED NOT NULL DEFAULT 0,
  weight_g   INT UNSIGNED NULL,
  attributes JSON NULL,
  active     TINYINT(1) NOT NULL DEFAULT 1,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_variants_sku (sku),
  KEY idx_variants_product (product_id),
  CONSTRAINT fk_variants_product
    FOREIGN KEY (product_id) REFERENCES products (id)
    ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS coupons (
  id           INT UNSIGNED NOT NULL AUTO_INCREMENT,
  code         VARCHAR(40) NOT NULL,
  type         ENUM('percent', 'fixed') NOT NULL,
  value        DECIMAL(10, 2) NOT NULL,
  min_subtotal DECIMAL(10, 2) NOT NULL DEFAULT 0,
  max_uses     INT UNSIGNED NULL,
  used_count   INT UNSIGNED NOT NULL DEFAULT 0,
  starts_at    DATETIME NULL,
  ends_at      DATETIME NULL,
  active       TINYINT(1) NOT NULL DEFAULT 1,
  created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_coupons_code (code)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS orders (
  id               INT UNSIGNED NOT NULL AUTO_INCREMENT,
  order_number     VARCHAR(24) NOT NULL,
  customer_name    VARCHAR(140) NOT NULL,
  email            VARCHAR(180) NOT NULL,
  phone            VARCHAR(30) NULL,
  shipping_address VARCHAR(255) NOT NULL,
  city             VARCHAR(120) NOT NULL,
  state            VARCHAR(120) NOT NULL,
  postal_code      VARCHAR(12) NOT NULL,
  subtotal         DECIMAL(10, 2) NOT NULL,
  discount         DECIMAL(10, 2) NOT NULL DEFAULT 0,
  shipping_cost    DECIMAL(10, 2) NOT NULL DEFAULT 0,
  total            DECIMAL(10, 2) NOT NULL,
  coupon_code      VARCHAR(40) NULL,
  status           ENUM('pending', 'paid', 'preparing', 'shipped', 'delivered', 'cancelled')
                   NOT NULL DEFAULT 'pending',
  payment_method   VARCHAR(40) NOT NULL DEFAULT 'mock',
  created_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_orders_number (order_number),
  KEY idx_orders_status (status),
  KEY idx_orders_email (email)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS order_items (
  id           INT UNSIGNED NOT NULL AUTO_INCREMENT,
  order_id     INT UNSIGNED NOT NULL,
  variant_id   INT UNSIGNED NOT NULL,
  product_name VARCHAR(160) NOT NULL,
  variant_name VARCHAR(120) NOT NULL,
  unit_price   DECIMAL(10, 2) NOT NULL,
  quantity     INT UNSIGNED NOT NULL,
  line_total   DECIMAL(10, 2) NOT NULL,
  PRIMARY KEY (id),
  KEY idx_order_items_order (order_id),
  KEY idx_order_items_variant (variant_id),
  CONSTRAINT fk_order_items_order
    FOREIGN KEY (order_id) REFERENCES orders (id)
    ON DELETE CASCADE,
  CONSTRAINT fk_order_items_variant
    FOREIGN KEY (variant_id) REFERENCES product_variants (id)
    ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS coupon_redemptions (
  id         INT UNSIGNED NOT NULL AUTO_INCREMENT,
  coupon_id  INT UNSIGNED NOT NULL,
  order_id   INT UNSIGNED NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_redemption_coupon_order (coupon_id, order_id),
  CONSTRAINT fk_redemptions_coupon
    FOREIGN KEY (coupon_id) REFERENCES coupons (id)
    ON DELETE RESTRICT,
  CONSTRAINT fk_redemptions_order
    FOREIGN KEY (order_id) REFERENCES orders (id)
    ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS order_status_history (
  id         INT UNSIGNED NOT NULL AUTO_INCREMENT,
  order_id   INT UNSIGNED NOT NULL,
  status     ENUM('pending', 'paid', 'preparing', 'shipped', 'delivered', 'cancelled') NOT NULL,
  note       VARCHAR(255) NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_status_history_order (order_id),
  CONSTRAINT fk_status_history_order
    FOREIGN KEY (order_id) REFERENCES orders (id)
    ON DELETE CASCADE
) ENGINE=InnoDB;
