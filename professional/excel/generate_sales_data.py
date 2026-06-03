"""
Generate realistic sales data for the AI Vibe Coding Excel tutorial.
Produces an Excel file with multiple sheets representing a real business scenario.
"""
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "sales_data.xlsx")

# ── Configuration ──────────────────────────────────────────────────────
NUM_ORDERS = 5000
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 12, 31)

# ── Product catalogue ──────────────────────────────────────────────────
PRODUCTS = [
    # (Category, Sub-Category, Product Name, Unit Price)
    ("Electronics", "Laptops",       "ThinkPad X1 Carbon",   1599.00),
    ("Electronics", "Laptops",       "MacBook Pro 16",       2499.00),
    ("Electronics", "Laptops",       "Dell XPS 15",          1899.00),
    ("Electronics", "Phones",        "iPhone 16 Pro",        1099.00),
    ("Electronics", "Phones",        "Samsung Galaxy S25",   999.00),
    ("Electronics", "Phones",        "Google Pixel 9",       799.00),
    ("Electronics", "Headphones",    "AirPods Pro 2",        249.00),
    ("Electronics", "Headphones",    "Sony WH-1000XM5",      349.00),
    ("Electronics", "Accessories",   "USB-C Hub",            49.99),
    ("Electronics", "Accessories",   "Wireless Charger",     29.99),
    ("Clothing",    "Shirts",        "Casual Button Down",   59.99),
    ("Clothing",    "Shirts",        "Polo T-Shirt",         39.99),
    ("Clothing",    "Jeans",         "Slim Fit Jeans",       79.99),
    ("Clothing",    "Jeans",         "Straight Leg Jeans",   69.99),
    ("Clothing",    "Jackets",       "Leather Jacket",       199.00),
    ("Clothing",    "Jackets",       "Rain Jacket",          89.99),
    ("Clothing",    "Shoes",         "Running Sneakers",     129.99),
    ("Clothing",    "Shoes",         "Formal Loafers",       89.99),
    ("Furniture",   "Chairs",        "Ergonomic Office Chair", 449.00),
    ("Furniture",   "Chairs",        "Gaming Chair",         399.00),
    ("Furniture",   "Tables",        "Standing Desk",        599.00),
    ("Furniture",   "Tables",        "Coffee Table",         249.00),
    ("Furniture",   "Sofas",         "3-Seater Fabric Sofa", 899.00),
    ("Furniture",   "Sofas",         "Leather Recliner",     1299.00),
    ("Furniture",   "Lighting",      "LED Desk Lamp",        49.99),
    ("Furniture",   "Lighting",      "Floor Lamp",           79.99),
    ("Food",        "Beverages",     "Specialty Coffee Pack", 24.99),
    ("Food",        "Beverages",     "Green Tea Collection", 18.99),
    ("Food",        "Snacks",        "Premium Nut Mix",      12.99),
    ("Food",        "Snacks",        "Dark Chocolate Box",   15.99),
    ("Food",        "Organic",       "Organic Fruit Basket", 34.99),
    ("Food",        "Organic",       "Organic Veg Box",      29.99),
]

# ── Customers ──────────────────────────────────────────────────────────
FIRST_NAMES = [
    "Alice", "Bob", "Charlie", "Diana", "Edward", "Fiona", "George",
    "Hannah", "Ivan", "Julia", "Kevin", "Linda", "Michael", "Nancy",
    "Oscar", "Patricia", "Quinn", "Rachel", "Samuel", "Tina", "Uma",
    "Victor", "Wendy", "Xavier", "Yvonne", "Zachary"
]
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"
]
STATES_US = [
    "California", "Texas", "New York", "Florida", "Illinois", "Pennsylvania",
    "Ohio", "Georgia", "North Carolina", "Michigan"
]
STATES_EU = [
    "Germany", "France", "UK", "Italy", "Spain", "Netherlands", "Sweden",
    "Denmark", "Norway", "Switzerland"
]
STATES_APAC = [
    "Japan", "China", "South Korea", "Australia", "India", "Singapore",
    "Taiwan", "New Zealand", "Thailand", "Vietnam"
]
CITIES = {
    "California": ["Los Angeles", "San Francisco", "San Diego"],
    "Texas": ["Houston", "Dallas", "Austin"],
    "New York": ["New York City", "Buffalo", "Rochester"],
    "Florida": ["Miami", "Orlando", "Tampa"],
    "Illinois": ["Chicago", "Naperville", "Springfield"],
    "Pennsylvania": ["Philadelphia", "Pittsburgh", "Allentown"],
    "Ohio": ["Columbus", "Cleveland", "Cincinnati"],
    "Georgia": ["Atlanta", "Savannah", "Augusta"],
    "North Carolina": ["Charlotte", "Raleigh", "Greensboro"],
    "Michigan": ["Detroit", "Grand Rapids", "Ann Arbor"],
    "Germany": ["Berlin", "Munich", "Hamburg"],
    "France": ["Paris", "Lyon", "Marseille"],
    "UK": ["London", "Manchester", "Edinburgh"],
    "Italy": ["Rome", "Milan", "Florence"],
    "Spain": ["Madrid", "Barcelona", "Valencia"],
    "Netherlands": ["Amsterdam", "Rotterdam", "Utrecht"],
    "Sweden": ["Stockholm", "Gothenburg", "Malmo"],
    "Denmark": ["Copenhagen", "Aarhus", "Odense"],
    "Norway": ["Oslo", "Bergen", "Stavanger"],
    "Switzerland": ["Zurich", "Geneva", "Basel"],
    "Japan": ["Tokyo", "Osaka", "Kyoto"],
    "China": ["Shanghai", "Beijing", "Shenzhen"],
    "South Korea": ["Seoul", "Busan", "Incheon"],
    "Australia": ["Sydney", "Melbourne", "Brisbane"],
    "India": ["Mumbai", "Delhi", "Bangalore"],
    "Singapore": ["Singapore"],
    "Taiwan": ["Taipei", "Kaohsiung", "Taichung"],
    "New Zealand": ["Auckland", "Wellington", "Christchurch"],
    "Thailand": ["Bangkok", "Chiang Mai", "Phuket"],
    "Vietnam": ["Ho Chi Minh City", "Hanoi", "Da Nang"],
}

REGIONS = {
    "North America": STATES_US,
    "Europe": STATES_EU,
    "Asia Pacific": STATES_APAC,
}

SHIPPING_MODES = ["Standard", "Express", "Next Day", "Same Day"]
PAYMENT_METHODS = ["Credit Card", "PayPal", "Bank Transfer", "Apple Pay", "Google Pay"]
SEGMENTS = ["Consumer", "Corporate", "Home Office"]

# ── Build Customer Pool ────────────────────────────────────────────────
def generate_customers(n=200):
    customers = []
    for i in range(1, n + 1):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        region = random.choice(list(REGIONS.keys()))
        state = random.choice(REGIONS[region])
        city = random.choice(CITIES[state])
        customers.append({
            "CustomerID": f"CUST{i:05d}",
            "FirstName": first,
            "LastName": last,
            "FullName": f"{first} {last}",
            "Segment": random.choice(SEGMENTS),
            "Region": region,
            "Country": state,
            "City": city,
            "Email": f"{first.lower()}.{last.lower()}@example.com",
        })
    return pd.DataFrame(customers)

# ── Build Orders ───────────────────────────────────────────────────────
def generate_orders(customers_df):
    orders = []
    order_ids = set()
    date_range_days = (END_DATE - START_DATE).days

    for _ in range(NUM_ORDERS):
        # Unique order ID
        while True:
            oid = f"ORD-{random.randint(10000, 99999)}"
            if oid not in order_ids:
                order_ids.add(oid)
                break

        customer = customers_df.sample(1).iloc[0]
        product = random.choice(PRODUCTS)
        category, subcategory, pname, unit_price = product

        qty = np.random.choice([1, 1, 1, 2, 2, 3, 4, 5])
        discount = np.random.choice([0, 0, 0, 0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3])
        shipping_cost = round(np.random.uniform(5, 50), 2)

        sales = round(unit_price * qty * (1 - discount), 2)
        # Profit margin varies by category
        margin_map = {"Electronics": 0.25, "Clothing": 0.45, "Furniture": 0.35, "Food": 0.30}
        margin = margin_map.get(category, 0.3)
        # Add some noise to profit
        margin_noise = np.random.normal(0, 0.05)
        profit = round(sales * (margin + margin_noise) - shipping_cost, 2)

        order_date = START_DATE + timedelta(days=random.randint(0, date_range_days))
        ship_date = order_date + timedelta(days=random.randint(1, 14))

        orders.append({
            "OrderID": oid,
            "OrderDate": order_date,
            "ShipDate": ship_date,
            "CustomerID": customer["CustomerID"],
            "CustomerName": customer["FullName"],
            "Segment": customer["Segment"],
            "Region": customer["Region"],
            "Country": customer["Country"],
            "City": customer["City"],
            "Category": category,
            "SubCategory": subcategory,
            "ProductName": pname,
            "UnitPrice": unit_price,
            "Quantity": qty,
            "Discount": discount,
            "Sales": sales,
            "Profit": profit,
            "ShippingCost": shipping_cost,
            "ShippingMode": random.choice(SHIPPING_MODES),
            "PaymentMethod": random.choice(PAYMENT_METHODS),
        })

    return pd.DataFrame(orders)

def main():
    print("Generating customers...")
    customers_df = generate_customers(200)
    print("Generating orders...")
    orders_df = generate_orders(customers_df)
    # Sort by date
    orders_df = orders_df.sort_values("OrderDate").reset_index(drop=True)

    # ── Summary tables for additional sheets ──
    print("Building summary sheets...")
    monthly_sales = orders_df.copy()
    monthly_sales["YearMonth"] = monthly_sales["OrderDate"].dt.to_period("M")
    monthly_summary = monthly_sales.groupby("YearMonth").agg(
        OrderCount=("OrderID", "nunique"),
        TotalSales=("Sales", "sum"),
        TotalProfit=("Profit", "sum"),
        AvgDiscount=("Discount", "mean"),
    ).reset_index()
    monthly_summary["YearMonth"] = monthly_summary["YearMonth"].astype(str)

    category_perf = orders_df.groupby("Category").agg(
        TotalSales=("Sales", "sum"),
        TotalProfit=("Profit", "sum"),
        OrderCount=("OrderID", "nunique"),
        AvgDiscount=("Discount", "mean"),
    ).reset_index().sort_values("TotalSales", ascending=False)

    region_perf = orders_df.groupby("Region").agg(
        TotalSales=("Sales", "sum"),
        TotalProfit=("Profit", "sum"),
        OrderCount=("OrderID", "nunique"),
    ).reset_index().sort_values("TotalSales", ascending=False)

    # Segment performance
    segment_perf = orders_df.groupby("Segment").agg(
        TotalSales=("Sales", "sum"),
        TotalProfit=("Profit", "sum"),
        OrderCount=("OrderID", "nunique"),
    ).reset_index()

    # Top 10 products
    top_products = orders_df.groupby("ProductName").agg(
        TotalSales=("Sales", "sum"),
        TotalProfit=("Profit", "sum"),
        QuantitySold=("Quantity", "sum"),
    ).reset_index().sort_values("TotalSales", ascending=False).head(10)

    # ── Write to Excel ──
    print(f"Writing to {OUTPUT_FILE}...")
    with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
        orders_df.to_excel(writer, sheet_name="Orders", index=False)
        customers_df.to_excel(writer, sheet_name="Customers", index=False)
        monthly_summary.to_excel(writer, sheet_name="MonthlySummary", index=False)
        category_perf.to_excel(writer, sheet_name="CategoryPerformance", index=False)
        region_perf.to_excel(writer, sheet_name="RegionPerformance", index=False)
        segment_perf.to_excel(writer, sheet_name="SegmentPerformance", index=False)
        top_products.to_excel(writer, sheet_name="TopProducts", index=False)

    print(f"Done! Generated {len(orders_df):,} orders across {len(customers_df)} customers.")
    print(f"File: {OUTPUT_FILE}")

    # Print column names for reference
    print(f"\nColumns in Orders: {list(orders_df.columns)}")
    print(f"Columns in Customers: {list(customers_df.columns)}")

if __name__ == "__main__":
    main()
