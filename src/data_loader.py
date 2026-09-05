import pandas as pd


def load_retail_data():
    products = pd.read_csv("data/products.csv")
    sales = pd.read_csv("data/sales.csv")
    inventory = pd.read_csv("data/inventory.csv")

    return products, sales, inventory