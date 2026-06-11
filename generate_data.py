"""
generate_data.py
Run this FIRST to create the sales_data.csv file.
"""

import csv
import random
from datetime import datetime, timedelta

random.seed(42)

PRODUCTS = [
    ("Laptop",       "Electronics",  45000, 80000),
    ("Smartphone",   "Electronics",  12000, 45000),
    ("Headphones",   "Electronics",   800,   5000),
    ("Desk Chair",   "Furniture",    3000,  12000),
    ("Bookshelf",    "Furniture",    1500,   6000),
    ("T-Shirt",      "Clothing",      299,   1200),
    ("Jeans",        "Clothing",      799,   3000),
    ("Running Shoes","Clothing",     1500,   6000),
    ("Rice 5kg",     "Grocery",       250,    600),
    ("Coffee Beans", "Grocery",       400,   1500),
]

CITIES    = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai",
             "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow"]
GENDERS   = ["Male", "Female"]
PAYMENTS  = ["Credit Card", "Debit Card", "UPI", "Cash", "Net Banking"]

start = datetime(2023, 1, 1)

rows = []
for i in range(1, 1001):
    product, category, lo, hi = random.choice(PRODUCTS)
    price    = round(random.uniform(lo, hi), 2)
    qty      = random.randint(1, 5)
    discount = random.choice([0, 5, 10, 15, 20])
    revenue  = round(price * qty * (1 - discount / 100), 2)
    date     = start + timedelta(days=random.randint(0, 364))
    rows.append({
        "order_id":       f"ORD{i:04d}",
        "date":           date.strftime("%Y-%m-%d"),
        "month":          date.strftime("%B"),
        "quarter":        f"Q{(date.month-1)//3+1}",
        "product":        product,
        "category":       category,
        "unit_price":     price,
        "quantity":       qty,
        "discount_pct":   discount,
        "revenue":        revenue,
        "city":           random.choice(CITIES),
        "customer_gender":random.choice(GENDERS),
        "payment_method": random.choice(PAYMENTS),
    })

with open("sales_data.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print("✅ sales_data.csv created with 1000 records.")
