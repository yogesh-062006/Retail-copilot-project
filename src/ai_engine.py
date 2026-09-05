import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY) if API_KEY else None

MODEL = "gemini-3.6-flash"


def build_retail_context(
    products,
    sales,
    inventory,
    metrics,
    inventory_issues,
    sales_changes
):

    product_lookup = products.set_index(
        "product_id"
    )["product_name"].to_dict()

    product_sales = (
        sales.groupby("product_id")
        .agg(
            units_sold=("units_sold", "sum"),
            revenue=("revenue", "sum")
        )
        .reset_index()
    )

    product_sales["product_name"] = product_sales[
        "product_id"
    ].map(product_lookup)

    context = {

        "total_revenue":
            float(metrics["total_revenue"]),

        "total_units_sold":
            int(metrics["total_units_sold"]),

        "best_product":
            metrics["best_product"],

        "product_sales":
            product_sales.to_dict(
                orient="records"
            ),

        "low_stock":
            inventory_issues["low_stock"][
                [
                    "product_id",
                    "product_name",
                    "current_stock",
                    "reorder_level"
                ]
            ].to_dict(
                orient="records"
            ),

        "dead_stock":
            inventory_issues["dead_stock"][
                [
                    "product_id",
                    "product_name",
                    "current_stock"
                ]
            ].to_dict(
                orient="records"
            ),

        "sales_changes":
            sales_changes
    }

    return context


def answer_question(
    question,
    products,
    sales,
    inventory,
    metrics,
    inventory_issues,
    sales_changes
):

    if not question.strip():

        return {
            "answer": "Please enter a question.",
            "evidence": [],
            "recommendation": ""
        }


    if client is None:

        return {
            "answer": "Gemini API key is not configured.",
            "evidence": [],
            "recommendation": ""
        }


    context = build_retail_context(
        products,
        sales,
        inventory,
        metrics,
        inventory_issues,
        sales_changes
    )


    prompt = f"""
You are RetailIQ, a retail sales and inventory copilot.

Answer the store manager's question using ONLY the
retail data provided below.

RETAIL DATA:
{context}

STORE MANAGER QUESTION:
{question}

RULES:

1. Never invent numbers, products, sales or inventory information.

2. Always use the actual numbers from the provided data.

3. If the data cannot answer the question, clearly say:
"The available data cannot determine this."

4. Keep the answer simple and useful for a store manager.

5. When appropriate, give a recommendation based on
the available evidence.

6. Clearly mention important numbers used in the answer.

7. Do not claim that a product was sold for a certain
number of days unless the data proves it.

8. Recommendations must be based on the provided data.

9. If making an assumption, clearly label it as an assumption.

Return the response in this format:

ANSWER:
<direct answer>

EVIDENCE:
- <important data point>
- <important data point>

RECOMMENDATION:
<action to take, or "No specific action recommended.">
"""


    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        text = response.text.strip()

        return {
            "answer": text,
            "evidence": [],
            "recommendation": ""
        }


    except Exception as error:

        return {
            "answer":
                f"Gemini request failed: {str(error)}",

            "evidence": [],

            "recommendation": ""
        }