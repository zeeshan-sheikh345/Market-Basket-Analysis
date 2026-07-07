"""
==========================================================
Market Basket Analysis (MBA) Using Pure Pandas
==========================================================

Description
-----------
This script performs Market Basket Analysis (Association Rule Mining)
using only the Pandas library.

Unlike mlxtend or other MBA libraries, this implementation builds
everything from scratch so that the complete logic is transparent.

The analysis calculates:

1. Support
2. Confidence
3. Lift

Input CSV Format
----------------

order_id,products

1001,Milk
1001,Bread
1001,Butter
1002,Milk
1002,Eggs

Each row represents ONE product purchased in ONE order.

==========================================================
"""

import pandas as pd


# ==========================================================
# STEP 1 : LOAD DATA
# ==========================================================

# Read transaction data from CSV file.
# Each row should contain:
#
# order_id   products
#
# Example:
#
# 1001       Milk
# 1001       Bread
# 1001       Butter
#
df = pd.read_csv("transactions.csv")

# Keep only required columns.
# This prevents unwanted columns from affecting the analysis.
df = df[['order_id', 'products']]

print("Transaction Data")
print(df.head())


# ==========================================================
# STEP 2 : TOTAL NUMBER OF ORDERS
# ==========================================================

# We count unique order IDs because one order can contain
# multiple products.
#
# Example:
#
# Order 1001
# Milk
# Bread
# Butter
#
# This is ONE order, not three.
#
total_orders = df["order_id"].nunique()

print("\nTotal Orders :", total_orders)


# ==========================================================
# STEP 3 : CALCULATE SUPPORT OF EACH PRODUCT
# ==========================================================

# Support tells us how frequently a product appears.
#
# Formula:
#
# Support(A)
#
# = Orders containing Product A
#   ----------------------------
#       Total Orders
#
# Example
#
# Milk appears in 200 orders
# Total Orders = 1000
#
# Support = 200 / 1000 = 0.20
#
item_support = (
    df.groupby("products")["order_id"]
      .nunique()
      .reset_index(name="item_order_count")
)

item_support["item_support"] = (
    item_support["item_order_count"] / total_orders
)

print("\nItem Support")
print(item_support.head())


# ==========================================================
# STEP 4 : GENERATE PRODUCT PAIRS
# ==========================================================

# This is the heart of Market Basket Analysis.
#
# We perform a SELF JOIN on order_id.
#
# Example
#
# Order 1001
#
# Milk
# Bread
# Butter
#
# becomes
#
# Milk - Bread
# Milk - Butter
# Bread - Butter
#
# We remove:
#
# Milk - Milk
#
# and duplicate combinations like:
#
# Bread - Milk
#
# because Milk - Bread already exists.
#
pairs = (
    df.merge(df, on="order_id")
      .query("products_x < products_y")
      .groupby(["products_x", "products_y"])["order_id"]
      .nunique()
      .reset_index(name="co_occurrence_count")
)

print("\nProduct Pairs")
print(pairs.head())


# ==========================================================
# STEP 5 : CALCULATE SUPPORT OF PRODUCT PAIRS
# ==========================================================

# Formula
#
# Support(A,B)
#
# Orders containing both A and B
# ------------------------------
#      Total Orders
#
pairs["support"] = (
    pairs["co_occurrence_count"] / total_orders
)


# ==========================================================
# STEP 6 : CALCULATE CONFIDENCE
# ==========================================================

# Confidence tells us:
#
# If Product A is purchased,
# how likely is Product B to be purchased?
#
# Formula
#
# Confidence(A → B)
#
# Orders(A,B)
# -----------
# Orders(A)
#
# Example
#
# Milk appears in 200 orders.
#
# Milk & Bread appear together in 80 orders.
#
# Confidence
#
# = 80 / 200
#
# = 0.40
#
pairs = pairs.merge(
    item_support[['products', 'item_order_count']],
    left_on='products_x',
    right_on='products',
    how='left'
).drop(columns='products')

pairs["confidence"] = (
    pairs["co_occurrence_count"] /
    pairs["item_order_count"]
)


# ==========================================================
# STEP 7 : CALCULATE LIFT
# ==========================================================

# Lift measures the TRUE strength of association.
#
# Formula
#
# Lift(A → B)
#
# = Confidence(A→B)
#   ----------------
#    Support(B)
#
#
# Interpretation
#
# Lift > 1
#
# Positive Association
#
# Lift = 1
#
# Independent Products
#
# Lift < 1
#
# Negative Association
#
pairs = pairs.merge(
    item_support[['products', 'item_support']],
    left_on='products_y',
    right_on='products',
    how='left'
).drop(columns='products')

pairs["lift"] = (
    pairs["confidence"] /
    pairs["item_support"]
)


# ==========================================================
# STEP 8 : FILTER STRONG ASSOCIATION RULES
# ==========================================================

# Remove weak rules.
#
# Minimum Support = 0.001
#
# Lift must be greater than 1
#
results = pairs[
    (pairs["support"] >= 0.001) &
    (pairs["lift"] > 1)
]


# ==========================================================
# STEP 9 : SELECT FINAL OUTPUT
# ==========================================================

# Keep only the important columns.
#
results = results[
    [
        "products_x",
        "products_y",
        "support",
        "confidence",
        "lift"
    ]
]

# Sort by Lift so the strongest associations appear first.
results = results.sort_values(
    by="lift",
    ascending=False
)


# ==========================================================
# STEP 10 : DISPLAY RESULTS
# ==========================================================

print("\nTop Association Rules")
print(results.head(20))


# ==========================================================
# STEP 11 : SAVE RESULTS
# ==========================================================

# Export results so they can be used in
# Excel, Power BI, Tableau, or Looker Studio.
#
results.to_csv(
    "market_basket_analysis_results.csv",
    index=False
)

print("\nAnalysis Completed Successfully!")
print("Results saved as market_basket_analysis_results.csv")
