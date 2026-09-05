from src.data_loader import load_retail_data
from src.analytics import calculate_metrics


# Load data
products, sales, inventory = load_retail_data()

# Calculate analytics
metrics = calculate_metrics(
    products,
    sales,
    inventory
)


# Display results
print("=" * 50)
print("        RETAILIQ - RETAIL ANALYTICS")
print("=" * 50)

print(f"Total Revenue     : ₹{metrics['total_revenue']:,.2f}")
print(f"Total Units Sold  : {metrics['total_units_sold']}")
print(f"Best Selling Item : {metrics['best_product']}")

print("\nLOW STOCK PRODUCTS")
print("-" * 50)

for _, item in metrics["low_stock"].iterrows():

    product_name = products.loc[
        products["product_id"] == item["product_id"],
        "product_name"
    ].iloc[0]

    print(
        f"{product_name} | "
        f"Stock: {item['current_stock']} | "
        f"Reorder Level: {item['reorder_level']}"
    )