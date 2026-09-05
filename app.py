from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

from src.data_loader import load_retail_data

from src.analytics import (
    calculate_metrics,
    detect_inventory_issues,
    detect_sales_changes
)

from src.ai_engine import answer_question


# --------------------------------------------------
# APP SETUP
# --------------------------------------------------

app = FastAPI(
    title="RetailIQ",
    description="Retail Sales & Inventory Copilot"
)


# --------------------------------------------------
# LOAD RETAIL DATA
# --------------------------------------------------

products, sales, inventory = load_retail_data()


# --------------------------------------------------
# CALCULATE ANALYTICS
# --------------------------------------------------

metrics = calculate_metrics(
    products,
    sales,
    inventory
)

inventory_issues = detect_inventory_issues(
    products,
    sales,
    inventory
)

sales_changes = detect_sales_changes(
    sales,
    products
)


# --------------------------------------------------
# QUESTION MODEL
# --------------------------------------------------

class AskRequest(BaseModel):
    question: str


# --------------------------------------------------
# FRONTEND
# --------------------------------------------------

@app.get("/")
def home():

    return FileResponse(
        "frontend/index.html"
    )


@app.get("/style.css")
def style():

    return FileResponse(
        "frontend/style.css"
    )


@app.get("/script.js")
def script():

    return FileResponse(
        "frontend/script.js"
    )


# --------------------------------------------------
# DASHBOARD API
# --------------------------------------------------

@app.get("/api/dashboard")
def dashboard():

    low_stock = inventory_issues["low_stock"]

    dead_stock = inventory_issues["dead_stock"]


    return {

        "total_revenue": float(
            metrics["total_revenue"]
        ),

        "total_units_sold": int(
            metrics["total_units_sold"]
        ),

        "best_product": metrics[
            "best_product"
        ],

        "low_stock": low_stock[
            [
                "product_id",
                "product_name",
                "current_stock",
                "reorder_level"
            ]
        ].to_dict(
            orient="records"
        ),

        "dead_stock": dead_stock[
            [
                "product_id",
                "product_name",
                "current_stock"
            ]
        ].to_dict(
            orient="records"
        ),

        "sales_changes": sales_changes
    }


# --------------------------------------------------
# GEMINI AI COPILOT API
# --------------------------------------------------

@app.post("/api/ask")
def ask_question(request: AskRequest):

    return answer_question(
        request.question,
        products,
        sales,
        inventory,
        metrics,
        inventory_issues,
        sales_changes
    )


# --------------------------------------------------
# START SERVER
# --------------------------------------------------

if __name__ == "__main__":

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )