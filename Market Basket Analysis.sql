WITH
-- 1️⃣ Total unique orders
total_orders AS (
SELECT COUNT(DISTINCT order_id) AS total_orders
FROM transactions
),

-- 2️⃣ Item-level support (single item frequency)
item_support AS (
SELECT
products,
COUNT(DISTINCT order_id) AS item_order_count
FROM transactions
GROUP BY products
),

-- 3️⃣ Product pair co-occurrence
pair_co_occurrence AS (
SELECT
t1.products AS product_a,
t2.products AS product_b,
COUNT(DISTINCT t1.order_id)AS co_occurrence_count
FROM transactions as t1
JOIN transactions as t2
ON t1.order_id = t2.order_id
AND t1.products <  t2.products -- avoids duplicates & self-pairs
GROUP BY
product_a,
product_b
)

-- 4️⃣ Final MBA metrics
SELECT
p.product_a,
p.product_b,

-- Support
p.co_occurrence_count*1.0/ t.total_orders AS support,

-- Confidence (A → B)
p.co_occurrence_count*1.0/ ia.item_order_count AS confidence,

-- Lift
(p.co_occurrence_count*1.0/ ia.item_order_count)/(ib.item_order_count*1.0/ t.total_orders) AS lift

FROM pair_co_occurrence p
JOIN item_support ia
ON p.product_a= ia.products
JOIN item_support ib
ON p.product_b= ib.products
CROSS JOIN total_orders t

-- 🔍 Optional filters (recommended)
WHERE
    p.co_occurrence_count>=20-- minimum common orders
AND (p.co_occurrence_count*1.0/ t.total_orders)>= 0.001
AND (
        (p.co_occurrence_count*1.0/ ia.item_order_count)/
        (ib.item_order_count*1.0/ t.total_orders)
    )>1

ORDER BY lift DESC;
