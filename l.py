# ==================================================
# AMAZON INDIA PRODUCTS — EXPLORATORY DATA ANALYSIS
# TOOLS: PANDAS, NUMPY, MATPLOTLIB
# ==================================================

# IMPORT REQUIRED LIBRARIES
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
import warnings
warnings.filterwarnings('ignore')

# SET GLOBAL STYLE FOR ALL CHARTS
plt.rcParams.update({
    'figure.facecolor'  : '#0D1117',
    'axes.facecolor'    : '#161B22',
    'axes.edgecolor'    : '#30363D',
    'axes.labelcolor'   : '#C9D1D9',
    'xtick.color'       : '#8B949E',
    'ytick.color'       : '#8B949E',
    'text.color'        : '#C9D1D9',
    'grid.color'        : '#21262D',
    'grid.linewidth'    : 0.8,
    'font.family'       : 'DejaVu Sans',
    'font.size'         : 11,
})

# AMAZON BRAND COLOR PALETTE
COLOR_ORANGE   = '#FF9900'
COLOR_BLUE     = '#146EB4'
COLOR_GREEN    = '#00A650'
COLOR_RED      = '#CC0C39'
COLOR_DARK     = '#0D1117'
COLOR_SURFACE  = '#161B22'
COLOR_TEXT     = '#C9D1D9'
COLOR_MUTED    = '#8B949E'


# ====================
# STEP 1: LOAD DATASET
# ====================
amazon_data = pd.read_csv('amazon.csv')

print("=" * 60)
print("STEP 1: DATASET LOADED")
print("=" * 60)
print(f"Total Rows    : {amazon_data.shape[0]}")
print(f"Total Columns : {amazon_data.shape[1]}")
print(f"\nColumn Names  : {amazon_data.columns.tolist()}")
print(f"\nFirst 3 Rows  :\n{amazon_data.head(3)}")


# =====================
# STEP 2: DATA OVERVIEW
# =====================
print("\n" + "=" * 60)
print("STEP 2: DATA OVERVIEW")
print("=" * 60)

print("\nDATA TYPES:")
print(amazon_data.dtypes)

# COUNT MISSING VALUES AND CALCULATE PERCENTAGE
missing_count      = amazon_data.isnull().sum()
missing_percentage = np.round((missing_count / len(amazon_data)) * 100, 2)

missing_summary = pd.DataFrame({
    'Missing Count' : missing_count,
    'Missing %'     : missing_percentage
})

print("\nMISSING VALUES:")
print(missing_summary[missing_summary['Missing Count'] > 0])


# =====================
# STEP 3: DATA CLEANING
# # ===================
print("\n" + "=" * 60)
print("STEP 3: DATA CLEANING")
print("=" * 60)

# REMOVE RUPEE SYMBOL AND COMMAS FROM PRICE COLUMNS
amazon_data['discounted_price_clean'] = (
    amazon_data['discounted_price']
    .str.replace('₹', '', regex=False)
    .str.replace(',', '', regex=False)
)

amazon_data['discounted_price_clean'] = pd.to_numeric(
    amazon_data['discounted_price_clean'], errors='coerce'
)

amazon_data['actual_price_clean'] = (
    amazon_data['actual_price']
    .str.replace('₹', '', regex=False)
    .str.replace(',', '', regex=False)
)

amazon_data['actual_price_clean'] = pd.to_numeric(
    amazon_data['actual_price_clean'], errors='coerce'
)

# REMOVE PERCENTAGE SIGN FROM DISCOUNT COLUMN
amazon_data['discount_percentage_clean'] = (
    amazon_data['discount_percentage']
    .str.replace('%', '', regex=False)
)
amazon_data['discount_percentage_clean'] = pd.to_numeric(
    amazon_data['discount_percentage_clean'], errors='coerce'
)

# CONVERT RATING TO NUMERIC
amazon_data['rating_clean'] = pd.to_numeric(
    amazon_data['rating'], errors='coerce'
)

# REMOVE COMMAS FROM RATING COUNT
amazon_data['rating_count_clean'] = (
    amazon_data['rating_count']
    .str.replace(',', '', regex=False)
)
amazon_data['rating_count_clean'] = pd.to_numeric(
    amazon_data['rating_count_clean'], errors='coerce'
)

# EXTRACT MAIN CATEGORY FROM PIPE-SEPARATED CATEGORY STRING
amazon_data['main_category'] = (
    amazon_data['category']
    .str.split('|')
    .str[0]
    .str.strip()
)

# EXTRACT SUB CATEGORY (SECOND LEVEL)
amazon_data['sub_category'] = (
    amazon_data['category']
    .str.split('|')
    .str[1]
    .str.strip()
)

# CALCULATE MONEY SAVED
amazon_data['money_saved'] = (
    amazon_data['actual_price_clean'] - amazon_data['discounted_price_clean']
)

# REMOVE DUPLICATES
duplicate_rows = amazon_data.duplicated().sum()
amazon_data.drop_duplicates(inplace=True)

print(f"Duplicate Rows Removed : {duplicate_rows}")
print(f"Remaining Rows         : {len(amazon_data)}")
# print("CLEANING COMPLETE!")


# ===============================
# STEP 4: TOP CATEGORIES ANALYSIS
# ===============================
print("\n" + "=" * 60)
print("STEP 4: TOP CATEGORIES ANALYSIS")
print("=" * 60)

top_categories       = amazon_data['main_category'].value_counts().head(10)
top_categories_pct   = np.round(top_categories / len(amazon_data) * 100, 1)

print(top_categories)

# PROFESSIONAL HORIZONTAL BAR CHART
fig, axis = plt.subplots(figsize=(14, 8), facecolor=COLOR_DARK)
axis.set_facecolor(COLOR_SURFACE)

# CREATE GRADIENT-LIKE COLORS
bar_colors = [COLOR_ORANGE if i == 0 else COLOR_BLUE
              for i in range(len(top_categories))]

bars = axis.barh(
    top_categories.index[::-1],
    top_categories.values[::-1],
    color=bar_colors[::-1],
    edgecolor='none',
    height=0.6
)

# ADD VALUE LABELS INSIDE BARS
for bar, value, pct in zip(bars, top_categories.values[::-1],
                           top_categories_pct.values[::-1]):
    axis.text(
        bar.get_width() - 5, bar.get_y() + bar.get_height() / 2,
        f'{value} products ({pct}%)',
        va='center', ha='right',
        color='white', fontweight='bold', fontsize=10
    )

axis.set_title('📦 Top 10 Product Categories on Amazon India',
               fontsize=16, fontweight='bold', color='white',
               pad=20)
axis.set_xlabel('Number of Products', fontsize=12)
axis.grid(axis='x', alpha=0.3)
axis.spines['top'].set_visible(False)
axis.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('01_top_categories.png', dpi=180, bbox_inches='tight',
            facecolor=COLOR_DARK)
plt.show()
print("SAVED: 01_top_categories.png")


# ===========================
# STEP 5: RATING DISTRIBUTION
# ===========================
print("\n" + "=" * 60)
print("STEP 5: RATING DISTRIBUTION ANALYSIS")
print("=" * 60)

clean_ratings    = amazon_data['rating_clean'].dropna()
average_rating   = np.mean(clean_ratings)
median_rating    = np.median(clean_ratings)
total_rated      = len(clean_ratings)

print(f"Average Rating : {average_rating:.2f}")
print(f"Median Rating  : {median_rating:.2f}")
print(f"Total Products : {total_rated}")

# HISTOGRAM WITH MEAN LINE
fig, axis = plt.subplots(figsize=(12, 7), facecolor=COLOR_DARK)
axis.set_facecolor(COLOR_SURFACE)

# DRAW HISTOGRAM
rating_counts, bin_edges, patches = axis.hist(
    clean_ratings, bins=20,
    color=COLOR_ORANGE, edgecolor=COLOR_DARK,
    linewidth=0.8, alpha=0.85
)

# HIGHLIGHT BARS ABOVE AVERAGE
for patch, left_edge in zip(patches, bin_edges[:-1]):
    if left_edge >= average_rating:
        patch.set_facecolor(COLOR_GREEN)

# MEAN AND MEDIAN LINES
axis.axvline(average_rating, color=COLOR_RED, linestyle='--',
             linewidth=2, label=f'Mean: {average_rating:.2f}')
axis.axvline(median_rating, color='#00BFFF', linestyle='-.',
             linewidth=2, label=f'Median: {median_rating:.2f}')

axis.set_title('⭐ Product Rating Distribution',
               fontsize=16, fontweight='bold', color='white', pad=20)
axis.set_xlabel('Rating', fontsize=12)
axis.set_ylabel('Number of Products', fontsize=12)
axis.legend(fontsize=11, facecolor=COLOR_SURFACE, labelcolor='white')
axis.grid(axis='y', alpha=0.3)
axis.spines['top'].set_visible(False)
axis.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('02_rating_distribution.png', dpi=180, bbox_inches='tight',
            facecolor=COLOR_DARK)
plt.show()
print("SAVED: 02_rating_distribution.png")


# ====================================
# STEP 6: DISCOUNT PERCENTAGE ANALYSIS
# ====================================
print("\n" + "=" * 60)
print("STEP 6: DISCOUNT PERCENTAGE ANALYSIS")
print("=" * 60)

clean_discounts      = amazon_data['discount_percentage_clean'].dropna()
average_discount     = np.mean(clean_discounts)
max_discount         = np.max(clean_discounts)
min_discount         = np.min(clean_discounts)
discount_25th        = np.percentile(clean_discounts, 25)
discount_75th        = np.percentile(clean_discounts, 75)

print(f"Average Discount  : {average_discount:.1f}%")
print(f"Max Discount      : {max_discount:.0f}%")
print(f"Min Discount      : {min_discount:.0f}%")
print(f"25th Percentile   : {discount_25th:.0f}%")
print(f"75th Percentile   : {discount_75th:.0f}%")

# BOX PLOT BY CATEGORY
top5_categories  = amazon_data['main_category'].value_counts().head(5).index
category_filter  = amazon_data[amazon_data['main_category'].isin(top5_categories)]

discount_by_category = [
    category_filter[category_filter['main_category'] == cat]
    ['discount_percentage_clean'].dropna().values
    for cat in top5_categories
]

fig, axis = plt.subplots(figsize=(14, 8), facecolor=COLOR_DARK)
axis.set_facecolor(COLOR_SURFACE)

box_plot = axis.boxplot(
    discount_by_category,
    patch_artist=True,
    notch=True,
    vert=True,
    widths=0.5,
    medianprops=dict(color=COLOR_ORANGE, linewidth=2.5),
    whiskerprops=dict(color=COLOR_MUTED, linewidth=1.5),
    capprops=dict(color=COLOR_MUTED, linewidth=1.5),
    flierprops=dict(marker='o', markerfacecolor=COLOR_RED,
                   markersize=4, alpha=0.5)
)

box_colors = [COLOR_ORANGE, COLOR_BLUE, COLOR_GREEN, COLOR_RED, '#9B59B6']
for patch, color in zip(box_plot['boxes'], box_colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

# SHORTEN LONG CATEGORY NAMES
short_names = [name[:20] + '...' if len(name) > 20 else name
               for name in top5_categories]
axis.set_xticklabels(short_names, rotation=15, ha='right', fontsize=10)

axis.set_title('🏷️ Discount % Distribution by Top Categories',
               fontsize=16, fontweight='bold', color='white', pad=20)
axis.set_ylabel('Discount Percentage (%)', fontsize=12)
axis.grid(axis='y', alpha=0.3)
axis.spines['top'].set_visible(False)
axis.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('03_discount_by_category.png', dpi=180, bbox_inches='tight',
            facecolor=COLOR_DARK)
plt.show()
print("SAVED: 03_discount_by_category.png")


# ========================================
# STEP 7: ACTUAL PRICE vs DISCOUNTED PRICE
# ========================================
print("\n" + "=" * 60)
print("STEP 7: ACTUAL PRICE vs DISCOUNTED PRICE")
print("=" * 60)

# FILTER OUT EXTREME PRICE OUTLIERS FOR BETTER VISUALIZATION
price_filter = amazon_data[
    (amazon_data['actual_price_clean'] < 50000) &
    (amazon_data['discounted_price_clean'] < 50000)
].dropna(subset=['actual_price_clean', 'discounted_price_clean'])

actual_prices     = price_filter['actual_price_clean'].values
discounted_prices = price_filter['discounted_price_clean'].values
discount_colors   = price_filter['discount_percentage_clean'].values

print(f"Products Plotted : {len(price_filter)}")

fig, axis = plt.subplots(figsize=(12, 8), facecolor=COLOR_DARK)
axis.set_facecolor(COLOR_SURFACE)

# SCATTER PLOT WITH COLOR BASED ON DISCOUNT %
scatter = axis.scatter(
    actual_prices, discounted_prices,
    c=discount_colors, cmap='RdYlGn',
    alpha=0.6, s=40, edgecolors='none'
)

# DIAGONAL LINE (IF NO DISCOUNT — PRICE WOULD BE SAME)
max_price = max(actual_prices.max(), discounted_prices.max())
axis.plot([0, max_price], [0, max_price],
          color=COLOR_MUTED, linestyle='--',
          linewidth=1.5, label='No Discount Line')

# COLOR BAR FOR DISCOUNT %
color_bar = plt.colorbar(scatter, ax=axis)
color_bar.set_label('Discount %', color='white', fontsize=11)
color_bar.ax.yaxis.set_tick_params(color='white')
plt.setp(color_bar.ax.yaxis.get_ticklabels(), color='white')

axis.set_title('💰 Actual Price vs Discounted Price\n(Color = Discount %)',
               fontsize=15, fontweight='bold', color='white', pad=20)
axis.set_xlabel('Actual Price (₹)', fontsize=12)
axis.set_ylabel('Discounted Price (₹)', fontsize=12)
axis.legend(fontsize=10, facecolor=COLOR_SURFACE, labelcolor='white')
axis.grid(alpha=0.2)
axis.spines['top'].set_visible(False)
axis.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('04_price_comparison.png', dpi=180, bbox_inches='tight',
            facecolor=COLOR_DARK)
plt.show()
print("SAVED: 04_price_comparison.png")


# =====================================
# STEP 8: TOP 10 MOST REVIEWED PRODUCTS
# =====================================
print("\n" + "=" * 60)
print("STEP 8: TOP 10 MOST REVIEWED PRODUCTS")
print("=" * 60)

most_reviewed_products = (
    amazon_data.nlargest(10, 'rating_count_clean')
    [['product_name', 'rating_count_clean', 'rating_clean']]
    .reset_index(drop=True)
)

# SHORTEN PRODUCT NAMES FOR DISPLAY
most_reviewed_products['short_name'] = (
    most_reviewed_products['product_name']
    .str[:35] + '...'
)

print(most_reviewed_products[['short_name', 'rating_count_clean', 'rating_clean']])

fig, axis = plt.subplots(figsize=(14, 8), facecolor=COLOR_DARK)
axis.set_facecolor(COLOR_SURFACE)

review_bar_colors = [
    COLOR_ORANGE if r >= 4.0 else COLOR_BLUE
    for r in most_reviewed_products['rating_clean']
]

bars = axis.barh(
    most_reviewed_products['short_name'][::-1],
    most_reviewed_products['rating_count_clean'][::-1],
    color=review_bar_colors[::-1],
    edgecolor='none', height=0.6
)

for bar, rating in zip(bars, most_reviewed_products['rating_clean'][::-1]):
    axis.text(
        bar.get_width() + 500,
        bar.get_y() + bar.get_height() / 2,
        f'⭐ {rating}',
        va='center', color=COLOR_ORANGE,
        fontweight='bold', fontsize=10
    )

axis.set_title('📝 Top 10 Most Reviewed Products',
               fontsize=16, fontweight='bold', color='white', pad=20)
axis.set_xlabel('Number of Reviews', fontsize=12)
axis.grid(axis='x', alpha=0.3)
axis.spines['top'].set_visible(False)
axis.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('05_most_reviewed.png', dpi=180, bbox_inches='tight',
            facecolor=COLOR_DARK)
plt.show()
print("SAVED: 05_most_reviewed.png")


# ======================================
# STEP 9: RATING vs DISCOUNT CORRELATION
# ======================================
print("\n" + "=" * 60)
print("STEP 9: RATING vs DISCOUNT CORRELATION")
print("=" * 60)

# FILTER VALID ROWS FOR CORRELATION
correlation_data = amazon_data.dropna(
    subset=['rating_clean', 'discount_percentage_clean']
)

rating_array   = correlation_data['rating_clean'].values
discount_array = correlation_data['discount_percentage_clean'].values

# NUMPY CORRELATION
correlation_matrix  = np.corrcoef(rating_array, discount_array)
correlation_value   = correlation_matrix[0, 1]

print(f"Correlation (Rating vs Discount) : {correlation_value:.4f}")

# TREND LINE USING NUMPY POLYFIT
trend_coefficients = np.polyfit(discount_array, rating_array, 1)
trend_line_values  = np.poly1d(trend_coefficients)
x_trend_values     = np.linspace(discount_array.min(), discount_array.max(), 100)

fig, axis = plt.subplots(figsize=(12, 7), facecolor=COLOR_DARK)
axis.set_facecolor(COLOR_SURFACE)

axis.scatter(
    discount_array, rating_array,
    color=COLOR_ORANGE, alpha=0.4,
    s=30, edgecolors='none', label='Products'
)

axis.plot(
    x_trend_values, trend_line_values(x_trend_values),
    color=COLOR_RED, linewidth=2.5,
    label=f'Trend Line (r = {correlation_value:.3f})'
)

axis.set_title('📊 Rating vs Discount % — Is Higher Discount = Better Rating?',
               fontsize=14, fontweight='bold', color='white', pad=20)
axis.set_xlabel('Discount Percentage (%)', fontsize=12)
axis.set_ylabel('Product Rating', fontsize=12)
axis.legend(fontsize=11, facecolor=COLOR_SURFACE, labelcolor='white')
axis.grid(alpha=0.2)
axis.spines['top'].set_visible(False)
axis.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('06_rating_vs_discount.png', dpi=180, bbox_inches='tight',
            facecolor=COLOR_DARK)
plt.show()
print("SAVED: 06_rating_vs_discount.png")


# =================================
# STEP 10: PRICE RANGE SEGMENTATION
# =================================
print("\n" + "=" * 60)
print("STEP 10: PRICE RANGE SEGMENTATION")
print("=" * 60)

# DEFINE PRICE SEGMENTS
price_bins   = [0, 500, 1000, 5000, 10000, 100000]
price_labels = ['Budget\n(₹0-500)', 'Economy\n(₹500-1K)',
                'Mid-Range\n(₹1K-5K)', 'Premium\n(₹5K-10K)',
                'Luxury\n(₹10K+)']

amazon_data['price_segment'] = pd.cut(
    amazon_data['discounted_price_clean'],
    bins=price_bins,
    labels=price_labels
)

price_segment_counts = amazon_data['price_segment'].value_counts().sort_index()
print(price_segment_counts)

# DONUT CHART
fig, axis = plt.subplots(figsize=(10, 8), facecolor=COLOR_DARK)
axis.set_facecolor(COLOR_DARK)

donut_colors    = [COLOR_GREEN, COLOR_ORANGE, COLOR_BLUE, COLOR_RED, '#9B59B6']
wedges, texts, autotexts = axis.pie(
    price_segment_counts.values,
    labels=price_segment_counts.index,
    autopct='%1.1f%%',
    colors=donut_colors,
    startangle=90,
    pctdistance=0.75,
    wedgeprops=dict(width=0.5, edgecolor=COLOR_DARK, linewidth=3),
    textprops={'color': 'white', 'fontsize': 10}
)

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(11)

# CENTER TEXT
axis.text(0, 0, f'{len(amazon_data)}\nProducts',
          ha='center', va='center',
          fontsize=16, fontweight='bold', color='white')

axis.set_title('💵 Product Price Segment Distribution',
               fontsize=16, fontweight='bold', color='white', pad=20)

plt.tight_layout()
plt.savefig('07_price_segments.png', dpi=180, bbox_inches='tight',
            facecolor=COLOR_DARK)
plt.show()
print("SAVED: 07_price_segments.png")


# ===================================
# STEP 11: AVERAGE RATING BY CATEGORY
# ===================================
print("\n" + "=" * 60)
print("STEP 11: AVERAGE RATING BY CATEGORY")
print("=" * 60)

average_rating_by_category = (
    amazon_data.groupby('main_category')['rating_clean']
    .mean()
    .dropna()
    .sort_values(ascending=False)
    .head(10)
)
average_rating_by_category = np.round(average_rating_by_category, 2)
print(average_rating_by_category)

fig, axis = plt.subplots(figsize=(13, 7), facecolor=COLOR_DARK)
axis.set_facecolor(COLOR_SURFACE)

rating_bar_colors = [
    COLOR_GREEN if r >= 4.0 else
    COLOR_ORANGE if r >= 3.5 else COLOR_RED
    for r in average_rating_by_category.values
]

bars = axis.barh(
    average_rating_by_category.index[::-1],
    average_rating_by_category.values[::-1],
    color=rating_bar_colors[::-1],
    edgecolor='none', height=0.6
)

for bar, val in zip(bars, average_rating_by_category.values[::-1]):
    axis.text(
        bar.get_width() + 0.01,
        bar.get_y() + bar.get_height() / 2,
        f'⭐ {val}',
        va='center', color='white',
        fontweight='bold', fontsize=11
    )

axis.set_xlim(0, 5.5)
axis.axvline(4.0, color=COLOR_MUTED, linestyle='--',
             linewidth=1.5, alpha=0.7, label='4.0 Threshold')
axis.set_title('⭐ Average Rating by Category\n🟢 ≥4.0  🟠 3.5–4.0  🔴 <3.5',
               fontsize=14, fontweight='bold', color='white', pad=20)
axis.set_xlabel('Average Rating', fontsize=12)
axis.legend(fontsize=10, facecolor=COLOR_SURFACE, labelcolor='white')
axis.grid(axis='x', alpha=0.3)
axis.spines['top'].set_visible(False)
axis.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('08_avg_rating_by_category.png', dpi=180, bbox_inches='tight',
            facecolor=COLOR_DARK)
plt.show()
print("SAVED: 08_avg_rating_by_category.png")


# =============================
# STEP 12: MONEY SAVED ANALYSIS
# =============================
print("\n" + "=" * 60)
print("STEP 12: MONEY SAVED BY CATEGORY")
print("=" * 60)

avg_money_saved_by_category = (
    amazon_data.groupby('main_category')['money_saved']
    .mean()
    .dropna()
    .sort_values(ascending=False)
    .head(10)
)
print(avg_money_saved_by_category)

fig, axis = plt.subplots(figsize=(13, 7), facecolor=COLOR_DARK)
axis.set_facecolor(COLOR_SURFACE)

money_colors = [COLOR_GREEN if i < 3 else COLOR_ORANGE
                for i in range(len(avg_money_saved_by_category))]

bars = axis.bar(
    range(len(avg_money_saved_by_category)),
    avg_money_saved_by_category.values,
    color=money_colors,
    edgecolor='none', width=0.6
)

for bar, val in zip(bars, avg_money_saved_by_category.values):
    axis.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 20,
        f'₹{val:.0f}',
        ha='center', color='white',
        fontweight='bold', fontsize=10
    )

short_category_names = [name[:15] + '..' if len(name) > 15 else name
                        for name in avg_money_saved_by_category.index]
axis.set_xticks(range(len(avg_money_saved_by_category)))
axis.set_xticklabels(short_category_names, rotation=30, ha='right', fontsize=10)

axis.set_title('💸 Average Money Saved by Category\n(Actual Price - Discounted Price)',
               fontsize=14, fontweight='bold', color='white', pad=20)
axis.set_ylabel('Average Savings (₹)', fontsize=12)
axis.grid(axis='y', alpha=0.3)
axis.spines['top'].set_visible(False)
axis.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('09_money_saved.png', dpi=180, bbox_inches='tight',
            facecolor=COLOR_DARK)
plt.show()
print("SAVED: 09_money_saved.png")


# =========================================
# STEP 13: DISCOUNT PERCENTAGE DISTRIBUTION
# =========================================
print("\n" + "=" * 60)
print("STEP 13: DISCOUNT PERCENTAGE DISTRIBUTION")
print("=" * 60)

clean_discount_values = amazon_data['discount_percentage_clean'].dropna()

fig, axis = plt.subplots(figsize=(12, 7), facecolor=COLOR_DARK)
axis.set_facecolor(COLOR_SURFACE)

n, bins, patches = axis.hist(
    clean_discount_values, bins=25,
    color=COLOR_BLUE, edgecolor=COLOR_DARK,
    linewidth=0.8, alpha=0.85
)

# HIGHLIGHT HIGH DISCOUNT BARS (>= 50%)
for patch, left_edge in zip(patches, bins[:-1]):
    if left_edge >= 50:
        patch.set_facecolor(COLOR_ORANGE)
    if left_edge >= 75:
        patch.set_facecolor(COLOR_GREEN)

avg_discount_value = np.mean(clean_discount_values)
axis.axvline(avg_discount_value, color=COLOR_RED,
             linestyle='--', linewidth=2,
             label=f'Average: {avg_discount_value:.1f}%')

axis.set_title('🏷️ Discount % Distribution\n🔵 <50%  🟠 50–75%  🟢 >75%',
               fontsize=14, fontweight='bold', color='white', pad=20)
axis.set_xlabel('Discount Percentage (%)', fontsize=12)
axis.set_ylabel('Number of Products', fontsize=12)
axis.legend(fontsize=11, facecolor=COLOR_SURFACE, labelcolor='white')
axis.grid(axis='y', alpha=0.3)
axis.spines['top'].set_visible(False)
axis.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('10_discount_distribution.png', dpi=180, bbox_inches='tight',
            facecolor=COLOR_DARK)
plt.show()
print("SAVED: 10_discount_distribution.png")


# ============================================================
# STEP 14: FINAL INSIGHTS SUMMARY
# PURE PANDAS & NUMPY — AGGREGATE ALL KEY NUMBERS
# ============================================================
print("\n" + "=" * 60)
print("STEP 14: FINAL INSIGHTS SUMMARY")
print("=" * 60)

total_products          = len(amazon_data)
total_categories        = amazon_data['main_category'].nunique()
top_category_name       = amazon_data['main_category'].value_counts().idxmax()
overall_avg_rating      = np.round(np.mean(amazon_data['rating_clean'].dropna()), 2)
overall_avg_discount    = np.round(np.mean(amazon_data['discount_percentage_clean'].dropna()), 1)
overall_avg_price       = np.round(np.mean(amazon_data['discounted_price_clean'].dropna()), 0)
overall_avg_savings     = np.round(np.mean(amazon_data['money_saved'].dropna()), 0)
highest_discount_pct    = np.max(amazon_data['discount_percentage_clean'].dropna())
most_reviewed_product   = amazon_data.nlargest(1, 'rating_count_clean')['product_name'].values[0][:40]
best_rated_category     = average_rating_by_category.idxmax()

print(f"""
🛒 AMAZON INDIA EDA — FINAL SUMMARY
{'=' * 55}
📦 Total Products         : {total_products:,}
🗂️  Total Categories       : {total_categories}
🏆 Top Category           : {top_category_name}
⭐ Overall Avg Rating     : {overall_avg_rating}
🏷️  Avg Discount           : {overall_avg_discount}%
💰 Avg Discounted Price   : ₹{overall_avg_price:,.0f}
💸 Avg Money Saved        : ₹{overall_avg_savings:,.0f}
🔥 Highest Discount       : {highest_discount_pct:.0f}%
📝 Most Reviewed Product  : {most_reviewed_product}...
🌟 Best Rated Category    : {best_rated_category}
{'=' * 55}
✅ ALL 10 CHARTS SAVED SUCCESSFULLY!
""")