"""
analysis.py
Run AFTER generate_data.py
Performs full exploratory data analysis on the sales dataset.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

# ── Setup ──────────────────────────────────────────────────────────────────────
os.makedirs("outputs", exist_ok=True)
plt.style.use("seaborn-v0_8-whitegrid")
COLORS = ["#2563EB", "#16A34A", "#DC2626", "#D97706", "#7C3AED",
          "#0891B2", "#DB2777", "#65A30D", "#EA580C", "#6366F1"]

df = pd.read_csv("sales_data.csv", parse_dates=["date"])
print(f"✅ Loaded {len(df)} records\n")

# ── 1. Basic Info ──────────────────────────────────────────────────────────────
print("=" * 50)
print("DATASET OVERVIEW")
print("=" * 50)
print(df.describe().round(2))
print("\nNull values:\n", df.isnull().sum())

# ── 2. KPI Summary ─────────────────────────────────────────────────────────────
total_revenue   = df["revenue"].sum()
total_orders    = len(df)
avg_order_value = df["revenue"].mean()
top_category    = df.groupby("category")["revenue"].sum().idxmax()

print("\n" + "=" * 50)
print("KEY PERFORMANCE INDICATORS")
print("=" * 50)
print(f"  Total Revenue    : Rs.{total_revenue:,.2f}")
print(f"  Total Orders     : {total_orders}")
print(f"  Avg Order Value  : Rs.{avg_order_value:,.2f}")
print(f"  Top Category     : {top_category}")

# ── 3. Monthly Revenue Trend ───────────────────────────────────────────────────
monthly = df.groupby(df["date"].dt.to_period("M"))["revenue"].sum().reset_index()
monthly["date"] = monthly["date"].astype(str)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(monthly["date"], monthly["revenue"], marker="o", color=COLORS[0], linewidth=2.5)
ax.fill_between(range(len(monthly)), monthly["revenue"], alpha=0.15, color=COLORS[0])
ax.set_xticks(range(len(monthly)))
ax.set_xticklabels(monthly["date"], rotation=45, ha="right", fontsize=8)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"Rs.{x/1000:.0f}K"))
ax.set_title("Monthly Revenue Trend (2023)", fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Month"); ax.set_ylabel("Revenue")
plt.tight_layout()
plt.savefig("outputs/01_monthly_revenue.png", dpi=150)
plt.close()
print("\n✅ Chart saved: outputs/01_monthly_revenue.png")

# ── 4. Revenue by Category ─────────────────────────────────────────────────────
cat_rev = df.groupby("category")["revenue"].sum().sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.barh(cat_rev.index, cat_rev.values, color=COLORS[:len(cat_rev)], edgecolor="white")
for bar, val in zip(bars, cat_rev.values):
    ax.text(val + 5000, bar.get_y() + bar.get_height()/2,
            f"Rs.{val/100000:.1f}L", va="center", fontsize=9)
ax.set_title("Revenue by Category", fontsize=13, fontweight="bold", pad=12)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"Rs.{x/100000:.0f}L"))
plt.tight_layout()
plt.savefig("outputs/02_revenue_by_category.png", dpi=150)
plt.close()
print("✅ Chart saved: outputs/02_revenue_by_category.png")

# ── 5. Top 5 Products ──────────────────────────────────────────────────────────
top_products = df.groupby("product")["revenue"].sum().sort_values(ascending=False).head(5)

fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(top_products.index, top_products.values,
              color=COLORS[:5], edgecolor="white", width=0.6)
for bar, val in zip(bars, top_products.values):
    ax.text(bar.get_x() + bar.get_width()/2, val + 10000,
            f"Rs.{val/100000:.1f}L", ha="center", fontsize=9)
ax.set_title("Top 5 Products by Revenue", fontsize=13, fontweight="bold", pad=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"Rs.{x/100000:.0f}L"))
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig("outputs/03_top5_products.png", dpi=150)
plt.close()
print("✅ Chart saved: outputs/03_top5_products.png")

# ── 6. Revenue by City ─────────────────────────────────────────────────────────
city_rev = df.groupby("city")["revenue"].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(9, 4))
bars = ax.bar(city_rev.index, city_rev.values,
              color=COLORS[:len(city_rev)], edgecolor="white", width=0.6)
for bar, val in zip(bars, city_rev.values):
    ax.text(bar.get_x() + bar.get_width()/2, val + 5000,
            f"Rs.{val/100000:.1f}L", ha="center", fontsize=8)
ax.set_title("Revenue by City", fontsize=13, fontweight="bold", pad=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"Rs.{x/100000:.0f}L"))
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("outputs/04_revenue_by_city.png", dpi=150)
plt.close()
print("✅ Chart saved: outputs/04_revenue_by_city.png")

# ── 7. Payment Method Distribution ────────────────────────────────────────────
pay = df["payment_method"].value_counts()

fig, ax = plt.subplots(figsize=(6, 5))
wedges, texts, autotexts = ax.pie(
    pay.values, labels=pay.index, autopct="%1.1f%%",
    colors=COLORS[:len(pay)], startangle=140,
    wedgeprops=dict(edgecolor="white", linewidth=1.5))
for at in autotexts:
    at.set_fontsize(9)
ax.set_title("Payment Method Distribution", fontsize=13, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig("outputs/05_payment_methods.png", dpi=150)
plt.close()
print("✅ Chart saved: outputs/05_payment_methods.png")

# ── 8. Quarterly Revenue ───────────────────────────────────────────────────────
qtr = df.groupby("quarter")["revenue"].sum()

fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.bar(qtr.index, qtr.values, color=COLORS[:4], edgecolor="white", width=0.5)
for bar, val in zip(bars, qtr.values):
    ax.text(bar.get_x() + bar.get_width()/2, val + 5000,
            f"Rs.{val/100000:.1f}L", ha="center", fontsize=10, fontweight="bold")
ax.set_title("Quarterly Revenue Comparison", fontsize=13, fontweight="bold", pad=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"Rs.{x/100000:.0f}L"))
plt.tight_layout()
plt.savefig("outputs/06_quarterly_revenue.png", dpi=150)
plt.close()
print("✅ Chart saved: outputs/06_quarterly_revenue.png")

# ── 9. Gender-wise Revenue ─────────────────────────────────────────────────────
gender = df.groupby("customer_gender")["revenue"].sum()

fig, ax = plt.subplots(figsize=(5, 4))
ax.bar(gender.index, gender.values, color=[COLORS[0], COLORS[3]],
       edgecolor="white", width=0.4)
for i, (idx, val) in enumerate(gender.items()):
    ax.text(i, val + 5000, f"Rs.{val/100000:.1f}L", ha="center", fontsize=11, fontweight="bold")
ax.set_title("Revenue by Customer Gender", fontsize=13, fontweight="bold", pad=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"Rs.{x/100000:.0f}L"))
plt.tight_layout()
plt.savefig("outputs/07_gender_revenue.png", dpi=150)
plt.close()
print("✅ Chart saved: outputs/07_gender_revenue.png")

# ── 10. Discount Impact on Revenue ────────────────────────────────────────────
disc = df.groupby("discount_pct")["revenue"].mean().reset_index()

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(disc["discount_pct"], disc["revenue"], marker="s",
        color=COLORS[2], linewidth=2.5, markersize=8)
ax.set_title("Avg Revenue vs Discount %", fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Discount (%)"); ax.set_ylabel("Avg Revenue (Rs.)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"Rs.{x:,.0f}"))
plt.tight_layout()
plt.savefig("outputs/08_discount_impact.png", dpi=150)
plt.close()
print("✅ Chart saved: outputs/08_discount_impact.png")

# ── Final Summary ──────────────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("ANALYSIS COMPLETE")
print("=" * 50)
print(f"  8 charts saved in /outputs/ folder")
print(f"  Total Revenue  : Rs.{total_revenue:,.2f}")
print(f"  Best Quarter   : {qtr.idxmax()} (Rs.{qtr.max():,.2f})")
print(f"  Top City       : {city_rev.idxmax()}")
print(f"  Top Product    : {top_products.idxmax()}")
print(f"  Top Category   : {top_category}")
