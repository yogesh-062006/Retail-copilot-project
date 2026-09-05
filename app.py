import pandas as pd

# Load retail data
products = pd.read_csv("data/products.csv")
sales = pd.read_csv("data/sales.csv")
inventory = pd.read_csv("data/inventory.csv")


# Basic calculations
total_revenue = sales["revenue"].sum()
total_units_sold = sales["units_sold"].sum()

best_product_id = (
    sales.groupby("product_id")["units_sold"]
    .sum()
    .idxmax()
)

best_product_name = products.loc[
    products["product_id"] == best_product_id,
    "product_name"
].iloc[0]

low_stock = inventory[
    inventory["current_stock"] <= inventory["reorder_level"]
]


# Display results
print("=" * 50)
print("        RETAILIQ - RETAIL ANALYTICS")
print("=" * 50)

print(f"Total Revenue      : ₹{total_revenue:,.2f}")
print(f"Total Units Sold   : {total_units_sold}")
print(f"Best Selling Item  : {best_product_name}")

print("\nLOW STOCK PRODUCTS")
print("-" * 50)

for _, item in low_stock.iterrows():
    product_name = products.loc[
        products["product_id"] == item["product_id"],
        "product_name"
    ].iloc[0]

    print(
        f"{product_name} | "
        f"Stock: {item['current_stock']} | "
        f"Reorder Level: {item['reorder_level']}"
    )