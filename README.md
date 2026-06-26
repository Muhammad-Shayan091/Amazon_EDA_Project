# 🛒 Amazon India Products — Exploratory Data Analysis

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=python&logoColor=white)
![Amazon](https://img.shields.io/badge/Amazon-FF9900?style=for-the-badge&logo=amazon&logoColor=white)

> A complete Exploratory Data Analysis on **1,465 Amazon India products** — uncovering pricing patterns, discount strategies, rating quality, and best value deals using Python, Pandas, NumPy & Matplotlib.

---

## 📌 Table of Contents
- [About the Project](#-about-the-project)
- [Dataset](#-dataset)
- [Project Structure](#-project-structure)
- [Analysis Steps & Chart Summaries](#-analysis-steps--chart-summaries)
- [Key Insights](#-key-insights)
- [How to Run](#-how-to-run)
- [Libraries Used](#-libraries-used)

---

## 📖 About the Project

This project digs deep into Amazon India's product listings to answer:
- Which categories dominate Amazon India?
- Do expensive products get better ratings?
- Which categories offer the biggest discounts?
- What makes a product the "Best Value Deal"?
- Is popularity (review count) linked to quality (rating)?
- How much money do customers actually save?

---

## 📂 Dataset

Dataset is **not included** in this repository due to size.

👉 Download from Kaggle: [Amazon Sales Dataset](https://www.kaggle.com/datasets/karkavelrajaj/amazon-sales-dataset)

| Detail | Info |
|---|---|
| File Name | `amazon.csv` |
| Total Rows | ~1,465 products |
| Total Columns | 16 |
| Source | Kaggle |
| Region | Amazon India |

After downloading, place `amazon.csv` in the same folder as `amazon_eda.py`.

---

## 📁 Project Structure

```
amazon-eda/
│
├── amazon_eda.py                    ← Main EDA script
├── amazon_new_insights.py           ← Additional insights (Step 15-24)
├── README.md                        ← Project documentation
│
├── 01_top_categories.png            ← Top 10 product categories
├── 02_rating_distribution.png       ← Rating histogram
├── 03_discount_by_category.png      ← Discount box plot
├── 04_price_comparison.png          ← Price vs discounted scatter
├── 05_most_reviewed.png             ← Most reviewed products
├── 06_rating_vs_discount.png        ← Rating vs discount trend
├── 07_price_segments.png            ← Price segment donut
├── 08_avg_rating_by_category.png    ← Avg rating per category
├── 09_money_saved.png               ← Money saved bar chart
├── 10_discount_distribution.png     ← Discount histogram
├── 11_rating_segments.png           ← Rating quality donut
├── 12_best_value_products.png       ← Best value scatter
├── 13_top_subcategories.png         ← Top sub-categories
├── 14_high_discount_products.png    ← 70%+ discount bar
├── 15_price_vs_rating.png           ← Price vs rating scatter
├── 16_avg_discount_by_category.png  ← Avg discount per category
├── 17_reviews_vs_rating.png         ← Reviews vs rating scatter
├── 18_top_rated_products.png        ← Top rated products
└── 19_actual_vs_discounted.png      ← Grouped price comparison
```

---

## 🔍 Analysis Steps & Chart Summaries

| Step | Analysis | Chart Type | What It Shows |
|---|---|---|---|
| 1 | Load Dataset | — | Shape, columns, first rows |
| 2 | Data Overview | — | Data types, missing values |
| 3 | Data Cleaning | — | Price cleaning, category extraction |
| 4 | Top Categories | Horizontal Bar | Which category has most products |
| 5 | Rating Distribution | Histogram | How ratings are spread (mean vs median) |
| 6 | Discount by Category | Box Plot | Spread of discounts per category |
| 7 | Price vs Discounted | Scatter | Relationship between actual & sale price |
| 8 | Most Reviewed Products | Horizontal Bar | Products with highest review counts |
| 9 | Rating vs Discount | Scatter + Trend | Does more discount = better rating? |
| 10 | Price Segments | Donut Chart | Budget vs Economy vs Premium split |
| 11 | Avg Rating by Category | Color Bar | Which category is highest rated |
| 12 | Money Saved | Bar Chart | Average savings per category |
| 13 | Discount Distribution | Histogram | How discounts are distributed |
| 14 | Final Summary I | — | First set of key metrics |
| 15 | Rating Quality Segments | Donut Chart | Poor / Average / Good / Excellent split |
| 16 | Best Value Products | Scatter | High rating + high discount = best deal |
| 17 | Top Sub-Categories | Horizontal Bar | Second-level category breakdown |
| 18 | High Discount (70%+) | Bar Chart | Categories with massive discounts |
| 19 | Price vs Rating | Scatter + Trend | Does price affect product quality? |
| 20 | Avg Discount by Category | Color Bar | Which category discounts most |
| 21 | Reviews vs Rating | Scatter | Does popularity = quality? |
| 22 | Top Rated Products | Horizontal Bar | Highest rated (min. 100 reviews) |
| 23 | Actual vs Discounted Price | Grouped Bar | Price gap per category |
| 24 | Final Summary II | — | Complete metrics summary |

---

## 💡 Key Insights

> Each insight below explains **what was found**, **why it was analyzed**, and **what business decision it supports**.

---

### 📦 Insight 1 — Top Product Categories
**What:** Electronics dominates with **526+ products**, followed by Computers & Accessories and Home & Kitchen.

**Why analyzed:** Understanding which categories have the most listings tells us where Amazon India focuses its inventory — and where competition is highest for sellers.

**Business use:** A new seller should avoid oversaturated categories like Electronics unless they have a unique product. Niche categories like Health or Office Products have less competition and strong ratings.

---

### 📂 Insight 2 — Top Sub-Categories
**What:** Accessories & Peripherals is the largest sub-category, followed by USB Cables and Networking Devices.

**Why analyzed:** Main categories are too broad — sub-categories reveal the actual product demand at a granular level.

**Business use:** A seller wanting to enter Electronics should target sub-categories like USB Cables or Chargers, which have high demand but are low-cost to produce.

---

### ⭐ Insight 3 — Rating Distribution
**What:** The average rating is **4.1/5.0** and the distribution is left-skewed — most products are rated between 3.8 and 4.5.

**Why analyzed:** Rating distribution reveals the overall quality health of Amazon India's catalog and whether customers are generally satisfied.

**Business use:** Products rated below 3.5 are likely to lose the Buy Box and get buried in search results — sellers must maintain at least 4.0 to stay competitive.

---

### 🏆 Insight 4 — Rating Quality Segments
**What:** Over **60% of products** fall in the "Good (4.0–4.5)" segment. Very few fall below 3.0.

**Why analyzed:** Segmenting ratings into quality buckets gives a clearer picture than just an average number.

**Business use:** Amazon's quality control is strong — poor products get removed. This means buyers can trust most listings, and sellers must maintain quality to survive.

---

### 🏷️ Insight 5 — Discount Distribution
**What:** Average discount is **~48%** across all products. Most discounts fall between 40–70%.

**Why analyzed:** Discount patterns reveal Amazon's pricing strategy and how aggressively sellers compete on price.

**Business use:** If your product's discount is below 30%, it may appear less attractive to deal-seeking Indian customers who expect 40–60% off.

---

### 🔥 Insight 6 — High Discount Products (70%+ OFF)
**What:** Electronics and Computers categories have the most products with **70%+ discounts**.

**Why analyzed:** Identifying extreme discount products reveals where price wars are most intense and where customers get the best deals.

**Business use:** For deal hunters — Electronics is the go-to category. For sellers — maintaining 70%+ discounts long-term is unsustainable and may signal low-quality or clearance products.

---

### 🏷️ Insight 7 — Average Discount by Category
**What:** Home Improvement and Computers offer the highest average discounts (50%+). Health & Personal Care offers the least.

**Why analyzed:** Category-level discount comparison shows which sectors compete most on price vs quality.

**Business use:** Health & Beauty products rely on brand trust rather than discounts, while Electronics rely heavily on deals — sellers should set their pricing strategy accordingly.

---

### 💰 Insight 8 — Price vs Discounted Price (Scatter)
**What:** Most products show a clear gap between actual and discounted price. Higher-priced items show the largest absolute savings.

**Why analyzed:** Visualizing both prices together reveals how real or inflated the "original price" is, and how much customers actually save.

**Business use:** Some sellers artificially inflate original prices to show bigger discounts. This analysis helps detect such patterns and understand true value.

---

### 💰 Insight 9 — Price Segments (Donut)
**What:** Over **40% of products** fall in the Mid-Range (₹1K–5K) segment. Budget products (≤₹500) make up ~15%.

**Why analyzed:** Understanding price distribution helps identify which customer income segment Amazon India primarily serves.

**Business use:** Mid-range products dominate — sellers targeting budget (₹0–500) or luxury (₹10K+) segments face less competition and can capture niche audiences.

---

### 💸 Insight 10 — Money Saved by Category
**What:** Customers save the most money in Electronics and Computers — average savings of **₹1,700+** per purchase.

**Why analyzed:** Absolute savings are more impactful than discount % — a 50% off on ₹200 saves only ₹100, but 30% off on ₹5,000 saves ₹1,500.

**Business use:** Marketing "Save ₹2,000 today" is more powerful than "50% OFF" for high-value products. This insight helps sellers craft better promotional messaging.

---

### 💰 Insight 11 — Actual vs Discounted Price by Category
**What:** Electronics has the largest gap between actual and discounted price — showing both the highest prices and highest savings.

**Why analyzed:** Category-level price comparison reveals where customers get the most value for money across different product types.

**Business use:** If a customer has a ₹2,000 budget, they should shop Electronics or Computers where discounts bring premium products into affordable range.

---

### ⭐ Insight 12 — Average Rating by Category
**What:** Office Products and Home & Kitchen have the highest average ratings. Electronics, despite being most listed, doesn't top in ratings.

**Why analyzed:** High product count doesn't mean high quality. This comparison separates quantity from quality.

**Business use:** Buyers looking for reliable products should prioritize Office Products and Home categories. Electronics has more variance in quality.

---

### 🏆 Insight 13 — Top Rated Products (Min. 100 Reviews)
**What:** The highest rated products (4.9–5.0) span multiple categories — not just one dominant type.

**Why analyzed:** Without minimum review filter, a product with 1 review and 5.0 rating would top the list — which is misleading. 100+ review filter ensures credibility.

**Business use:** Buyers can use this as a reliable "best products" list. Sellers should aim for 100+ reviews before promoting heavily, as ratings stabilize after sufficient feedback.

---

### 📝 Insight 14 — Most Reviewed Products
**What:** The most reviewed products have **90,000+ reviews**, showing viral-level popularity for specific items like basic USB cables and chargers.

**Why analyzed:** Review count is a proxy for sales volume — more reviews = more purchases = more trust.

**Business use:** Sellers entering the USB Cable or Charger space will face products with 90K+ reviews. New sellers must focus on differentiation (better packaging, bundle deals) to compete.

---

### 📊 Insight 15 — Rating vs Discount Correlation
**What:** Correlation between rating and discount is nearly **0** — no meaningful link exists.

**Why analyzed:** A common assumption is that discounted products are lower quality. This analysis proves or disproves that assumption with real data.

**Business use:** Sellers can offer deep discounts WITHOUT hurting their rating perception. Customers don't associate discounts with poor quality on Amazon India.

---

### 💰 Insight 16 — Does Price Affect Rating?
**What:** Price and rating show **almost no correlation** — expensive products are NOT necessarily better rated.

**Why analyzed:** This challenges the "you get what you pay for" assumption and is one of the most counter-intuitive insights in this project.

**Business use:** Budget product sellers can compete with premium brands on quality. Customers don't need to overspend for a good rating product — value exists at all price points.

---

### 📊 Insight 17 — Review Count vs Rating
**What:** Products with more reviews tend to stabilize around **4.0 rating** — very few high-review products are below 3.5.

**Why analyzed:** This tests whether "crowd wisdom" (many reviewers) leads to more accurate and higher ratings.

**Business use:** Early-stage products with few reviews can have volatile ratings (1-star or 5-star extremes). Getting to 500+ reviews is key to achieving a stable, trustworthy rating.

---

### 🏆 Insight 18 — Best Value Products
**What:** Products in the **top-right zone** of the scatter (high rating + high discount) represent the best deals. These are hidden gems customers should target.

**Why analyzed:** Neither rating alone nor discount alone defines value. The custom `value_score = rating × log(discount)` metric combines both to find true deals.

**Business use:** Customers using this metric can identify products that are both high quality AND heavily discounted — the ultimate deal. Sellers scoring high on this metric will see higher conversion rates.

---

## ▶️ How to Run

**1. Clone the repository**
```bash
git clone https://github.com/Muhammad-Shayan091/Amazon_EDA.git
cd Amazon_EDA
```

**2. Install required libraries**
```bash
pip install pandas numpy matplotlib
```

**3. Download the dataset**

👉 [Amazon Sales Dataset on Kaggle](https://www.kaggle.com/datasets/karkavelrajaj/amazon-sales-dataset)

Place `amazon.csv` in the project folder.

**4. Run main script**
```bash
python amazon_eda.py
```

**5. Run additional insights**
```bash
python amazon_new_insights.py
```

All 19 charts will be saved as PNG files automatically! ✅

---

## 🛠️ Libraries Used

| Library | Purpose |
|---|---|
| `pandas` | Data loading, cleaning, groupby analysis |
| `numpy` | Statistics, correlations, percentiles |
| `matplotlib` | Professional dark-theme visualizations |

---

## 🎨 Chart Style

All charts use a **professional dark GitHub-inspired theme**:
- Background: `#0D1117` (GitHub dark)
- Surface: `#161B22`
- Amazon Orange: `#FF9900`
- Green accents for positive metrics
- Red accents for negative/alert metrics

---

## 👤 Author

Made with ❤️ by **Muhammad Shayan**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Muhammad-Shayan091)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/muhammad-shayan)

---

⭐ **If you found this project helpful, please give it a star!** ⭐