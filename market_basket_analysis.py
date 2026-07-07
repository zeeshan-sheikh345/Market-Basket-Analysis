"""
====================================================
Market Basket Analysis (MBA) using Pure Pandas
====================================================

Author : Your Name
GitHub : https://github.com/yourusername

Description
-----------
This project performs Market Basket Analysis without using
any external association rule libraries.

The algorithm is implemented using:

1. Self Join
2. GroupBy
3. Support
4. Confidence
5. Lift

Input
-----
transactions.csv

Columns:
--------
order_id
products

Output
------
market_basket_results.csv

"""

import pandas as pd


# ---------------------------------------------------
# Load Transaction Data
# ---------------------------------------------------

def load_data(filepath: str) -> pd.DataFrame:
    """
    Loads transaction data.

    Parameters
    ----------
    filepath : str
        CSV file path

    Returns
    -------
    DataFrame
    """

    df = pd.read_csv(filepath)

    # Keep only required columns
    df = df[['order_id', 'products']]

    return df


# ---------------------------------------------------
# Calculate Item Support
# ---------------------------------------------------

def calculate_item_support(df: pd.DataFrame):
    """
    Calculates support for each individual product.

    Support(Product A)

    = Orders containing Product A
      ---------------------------
          Total Orders
    """

    total_orders = df["order_id"].nunique()

    item_support = (
        df.groupby("products")["order_id"]
        .nunique()
        .reset_index(name="item_order_count")
    )

    item_support["item_support"] = (
        item_support["item_order_count"] / total_orders
    )

    return item_support, total_orders


# ---------------------------------------------------
# Generate Product Pairs
# ---------------------------------------------------

def generate_product_pairs(df: pd.DataFrame):
    """
    Creates product combinations purchased together.

    Example

    Order 1001

    Milk
    Bread
    Butter

    becomes

    Milk - Bread
    Milk - Butter
    Bread - Butter

    """

    pairs = (
        df.merge(df, on="order_id")
        .query("products_x < products_y")
        .groupby(["products_x", "products_y"])["order_id"]
        .nunique()
        .reset_index(name="co_occurrence_count")
    )

    return pairs


# ---------------------------------------------------
# Calculate Support
# ---------------------------------------------------

def calculate_support(pairs, total_orders):
    """
    Support(A,B)

    Orders containing A and B
    -------------------------
        Total Orders
    """

    pairs["support"] = (
        pairs["co_occurrence_count"] / total_orders
    )

    return pairs


# ---------------------------------------------------
# Calculate Confidence
# ---------------------------------------------------

def calculate_confidence(pairs, item_support):
    """
    Confidence(A -> B)

    Orders(A,B)
    ----------
    Orders(A)

    """

    pairs = pairs.merge(
        item_support[["products", "item_order_count"]],
        left_on="products_x",
        right_on="products",
        how="left"
    ).drop(columns="products")

    pairs["confidence"] = (
        pairs["co_occurrence_count"] /
        pairs["item_order_count"]
    )

    return pairs


# ---------------------------------------------------
# Calculate Lift
# ---------------------------------------------------

def calculate_lift(pairs, item_support):
    """
    Lift(A -> B)

         Confidence(A->B)
    ----------------------------
       Support(B)

    Lift > 1

    Positive Association

    Lift = 1

    Independent

    Lift < 1

    Negative Association
    """

    pairs = pairs.merge(
        item_support[["products", "item_support"]],
        left_on="products_y",
        right_on="products",
        how="left"
    ).drop(columns="products")

    pairs["lift"] = (
        pairs["confidence"] /
        pairs["item_support"]
    )

    return pairs


# ---------------------------------------------------
# Filter Rules
# ---------------------------------------------------

def filter_rules(
        pairs,
        min_support=0.001,
        min_lift=1.0):

    return pairs[
        (pairs["support"] >= min_support) &
        (pairs["lift"] >= min_lift)
    ]


# ---------------------------------------------------
# Main Function
# ---------------------------------------------------

def main():

    print("Loading data...")

    df = load_data("data/transactions.csv")

    print(df.head())

    item_support, total_orders = calculate_item_support(df)

    print(f"Total Orders : {total_orders}")

    pairs = generate_product_pairs(df)

    pairs = calculate_support(
        pairs,
        total_orders
    )

    pairs = calculate_confidence(
        pairs,
        item_support
    )

    pairs = calculate_lift(
        pairs,
        item_support
    )

    results = filter_rules(
        pairs,
        min_support=0.001,
        min_lift=1
    )

    results = results[[
        "products_x",
        "products_y",
        "support",
        "confidence",
        "lift"
    ]].sort_values(
        by="lift",
        ascending=False
    )

    print(results.head(20))

    results.to_csv(
        "output/market_basket_results.csv",
        index=False
    )

    print("\nAnalysis Completed Successfully!")


if __name__ == "__main__":
    main()
