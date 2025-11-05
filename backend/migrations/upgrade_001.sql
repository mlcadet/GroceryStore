-- Migration: upgrade_001.sql
-- Purpose: Change price_per_unit to DECIMAL(10,2), add unique constraint on uom.uom_name,
-- and add foreign key constraint products.uom_id -> uom.uom_id.
-- IMPORTANT: Run a backup before applying this migration.

-- 1) Change price_per_unit to DECIMAL(10,2)
ALTER TABLE gs.products
  MODIFY COLUMN price_per_unit DECIMAL(10,2) NOT NULL;

-- 2) Add UNIQUE on uom.uom_name to avoid duplicate unit names
ALTER TABLE gs.uom
  ADD UNIQUE uq_uom_name (uom_name);

-- 3) Add foreign key constraint from products.uom_id -> uom.uom_id
-- Note: This will fail if there are uom_id values in products that do not exist in uom.
-- Verify referential integrity before running, or run the provided check below.

-- Referential integrity check (run and ensure result is 0):
-- SELECT COUNT(*) FROM gs.products p LEFT JOIN gs.uom u ON p.uom_id = u.uom_id WHERE u.uom_id IS NULL;

-- If the above returns 0, you can safely add the constraint.
ALTER TABLE gs.products
  ADD CONSTRAINT fk_products_uom
  FOREIGN KEY (uom_id) REFERENCES gs.uom(uom_id)
  ON DELETE RESTRICT ON UPDATE CASCADE;

-- 4) Insert typical UOMs if missing
INSERT INTO gs.uom (uom_name)
  SELECT * FROM (SELECT 'liter' AS uom_name) AS tmp
  WHERE NOT EXISTS (SELECT 1 FROM gs.uom WHERE uom_name = 'liter');

INSERT INTO gs.uom (uom_name)
  SELECT * FROM (SELECT 'pack' AS uom_name) AS tmp
  WHERE NOT EXISTS (SELECT 1 FROM gs.uom WHERE uom_name = 'pack');

-- End of migration
