def calculate_metrics(products, sales, inventory):
    # Total revenue
    total_revenue = sales["revenue"].sum()

    # Total units sold
    total_units_sold = sales["units_sold"].sum()

    # Total sales by product
    product_sales = sales.groupby("product_id")["units_sold"].sum()

    # Best-selling product
    best_product_id = product_sales.idxmax()

    best_product_name = products.loc[
        products["product_id"] == best_product_id,
        "product_name"
    ].iloc[0]

    # Low-stock products
    low_stock = inventory[
        inventory["current_stock"] <= inventory["reorder_level"]
    ].copy()

    return {
        "total_revenue": total_revenue,
        "total_units_sold": total_units_sold,
        "best_product": best_product_name,
        "low_stock": low_stock
    }


def detect_inventory_issues(products, sales, inventory):
    # -----------------------------
    # LOW STOCK
    # -----------------------------
    low_stock = inventory[
        inventory["current_stock"] <= inventory["reorder_level"]
    ].copy()

    # -----------------------------
    # DEAD STOCK
    # -----------------------------
    sold_product_ids = set(sales["product_id"])

    dead_stock = inventory[
        (~inventory["product_id"].isin(sold_product_ids))
        & (inventory["current_stock"] > 0)
    ].copy()

    # Add product names
    low_stock["product_name"] = low_stock["product_id"].map(
        products.set_index("product_id")["product_name"]
    )

    dead_stock["product_name"] = dead_stock["product_id"].map(
        products.set_index("product_id")["product_name"]
    )

    return {
        "low_stock": low_stock,
        "dead_stock": dead_stock
    }


def detect_sales_changes(sales, products):
    # Make sure date is treated as a date
    sales = sales.copy()
    sales["date"] = sales["date"].astype(str)

    # Calculate total units sold per day
    daily_sales = (
        sales.groupby("date")["units_sold"]
        .sum()
        .sort_index()
    )

    results = []

    # Need at least 2 days to compare
    if len(daily_sales) < 2:
        return results

    latest_date = daily_sales.index[-1]
    latest_units = daily_sales.iloc[-1]

    previous_sales = daily_sales.iloc[:-1]
    average_previous_units = previous_sales.mean()

    # Avoid division by zero
    if average_previous_units == 0:
        return results

    percentage_change = (
        (latest_units - average_previous_units)
        / average_previous_units
    ) * 100

    # Detect significant change
    if percentage_change >= 25:
        change_type = "Sales Spike"
    elif percentage_change <= -25:
        change_type = "Sales Drop"
    else:
        change_type = "Normal"

    results.append({
        "date": latest_date,
        "latest_units": int(latest_units),
        "previous_average_units": round(average_previous_units, 2),
        "percentage_change": round(percentage_change, 2),
        "change_type": change_type
    })

    return results