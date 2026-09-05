def calculate_metrics(products, sales, inventory):

    total_revenue = sales["revenue"].sum()
    total_units_sold = sales["units_sold"].sum()

    product_sales = sales.groupby("product_id")["units_sold"].sum()

    best_product_id = product_sales.idxmax()

    best_product_name = products.loc[
        products["product_id"] == best_product_id,
        "product_name"
    ].iloc[0]

    low_stock = inventory[
        inventory["current_stock"] <= inventory["reorder_level"]
    ]

    return {
        "total_revenue": total_revenue,
        "total_units_sold": total_units_sold,
        "best_product": best_product_name,
        "low_stock": low_stock
    }