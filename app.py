from src.data_loader import load_retail_data
from src.analytics import (
    calculate_metrics,
    detect_inventory_issues,
    detect_sales_changes
)


# Load retail data
products, sales, inventory = load_retail_data()


# Calculate basic metrics
metrics = calculate_metrics(
    products,
    sales,
    inventory
)


# Detect inventory issues
inventory_issues = detect_inventory_issues(
    products,
    sales,
    inventory
)


# Detect sales changes
sales_changes = detect_sales_changes(
    sales,
    products
)


# -----------------------------------------
# DISPLAY RETAILIQ RESULTS
# -----------------------------------------

print("=" * 55)
print("              RETAILIQ")
print("       RETAIL SALES & INVENTORY COPILOT")
print("=" * 55)

print(f"\nTotal Revenue     : ₹{metrics['total_revenue']:,.2f}")
print(f"Total Units Sold  : {metrics['total_units_sold']}")
print(f"Best Selling Item : {metrics['best_product']}")


# -----------------------------------------
# LOW STOCK
# -----------------------------------------

print("\n" + "-" * 55)
print("LOW STOCK PRODUCTS")
print("-" * 55)

low_stock = inventory_issues["low_stock"]

if low_stock.empty:
    print("No low-stock products detected.")

else:
    for _, item in low_stock.iterrows():
        print(
            f"{item['product_name']} | "
            f"Stock: {item['current_stock']} | "
            f"Reorder Level: {item['reorder_level']}"
        )


# -----------------------------------------
# DEAD STOCK
# -----------------------------------------

print("\n" + "-" * 55)
print("DEAD STOCK PRODUCTS")
print("-" * 55)

dead_stock = inventory_issues["dead_stock"]

if dead_stock.empty:
    print("No dead-stock products detected.")

else:
    for _, item in dead_stock.iterrows():
        print(
            f"{item['product_name']} | "
            f"Current Stock: {item['current_stock']}"
        )


# -----------------------------------------
# SALES SPIKE / DROP
# -----------------------------------------

print("\n" + "-" * 55)
print("SALES CHANGE DETECTION")
print("-" * 55)

if not sales_changes:
    print("Not enough data to detect sales changes.")

else:
    for change in sales_changes:
        print(
            f"Date: {change['date']} | "
            f"Units: {change['latest_units']} | "
            f"Previous Avg: {change['previous_average_units']} | "
            f"Change: {change['percentage_change']}% | "
            f"Status: {change['change_type']}"
        )


print("\n" + "=" * 55)
print("RetailIQ analysis completed successfully!")
print("=" * 55)