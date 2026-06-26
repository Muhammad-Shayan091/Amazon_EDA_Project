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
fig, axis = plt.subplots(figsize=(16, 8), facecolor=COLOR_DARK)
plt.subplots_adjust(left=0.35)
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

axis.set_xlim(0, top_categories.max() * 1.15)

# ADD VALUE LABELS INSIDE BARS
for bar, value, pct in zip(
        bars,
        top_categories.values[::-1],
        top_categories_pct.values[::-1]):

    width = bar.get_width()

    if width > top_categories.max() * 0.15:
        x_pos = width - 5
        ha = 'right'
    else:
        x_pos = width + 5
        ha = 'left'

    axis.text(
        x_pos,
        bar.get_y() + bar.get_height() / 2,
        f'{value} products ({pct}%)',
        va='center',
        ha=ha,
        color='white',
        fontweight='bold',
        fontsize=10
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
# STEP 15: RATING QUALITY SEGMENTS
# WHAT IT SHOWS: HOW MANY PRODUCTS FALL IN POOR, AVERAGE,
# GOOD, EXCELLENT RATING CATEGORIES
# ============================================================
print("\n" + "=" * 60)
print("STEP 15: RATING QUALITY SEGMENTS")
print("=" * 60)

# DEFINE RATING QUALITY BUCKETS
rating_segment_bins   = [0, 3.0, 3.5, 4.0, 4.5, 5.0]
rating_segment_labels = ['Poor\n(<3.0)', 'Below Avg\n(3.0-3.5)',
                          'Average\n(3.5-4.0)', 'Good\n(4.0-4.5)',
                          'Excellent\n(4.5-5.0)']

amazon_data['rating_segment'] = pd.cut(
    amazon_data['rating_clean'],
    bins=rating_segment_bins,
    labels=rating_segment_labels
)

rating_segment_counts = amazon_data['rating_segment'].value_counts().sort_index()
print(rating_segment_counts)

# DONUT CHART
fig, axis = plt.subplots(figsize=(10, 8), facecolor=COLOR_DARK)
axis.set_facecolor(COLOR_DARK)

segment_colors = [COLOR_RED, '#FF6B35', COLOR_ORANGE, COLOR_BLUE, COLOR_GREEN]

wedges, texts, autotexts = axis.pie(
    rating_segment_counts.values,
    labels=rating_segment_counts.index,
    autopct='%1.1f%%',
    colors=segment_colors,
    startangle=90,
    pctdistance=0.78,
    wedgeprops=dict(width=0.5, edgecolor=COLOR_DARK, linewidth=3),
    textprops={'color': 'white', 'fontsize': 10}
)

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(11)

# CENTER LABEL
axis.text(0, 0, f'{len(amazon_data)}\nProducts',
          ha='center', va='center',
          fontsize=16, fontweight='bold', color='white')

axis.set_title('⭐ Product Rating Quality Segments\n🔴 Poor  🟠 Below Avg  🔵 Average  🟢 Good  ✅ Excellent',
               fontsize=14, fontweight='bold', color='white', pad=20)

plt.tight_layout()
plt.savefig('11_rating_segments.png', dpi=180, bbox_inches='tight',
            facecolor=COLOR_DARK)
plt.show()
print("SAVED: 11_rating_segments.png")
print("📌 INSIGHT: Majority of Amazon products fall in the 'Good (4.0-4.5)' category,")
print("   meaning Amazon maintains high quality standards across its listings.")


# ============================================================
# STEP 16: BEST VALUE PRODUCTS ANALYSIS
# WHAT IT SHOWS: PRODUCTS WITH HIGH RATING + HIGH DISCOUNT
# value_score = rating * log(discount) — CUSTOM METRIC
# np.log1p() SMOOTHS LARGE DISCOUNT VALUES
# CHART TYPE: SCATTER — SHOWS RATING VS DISCOUNT RELATIONSHIP
# ============================================================
print("\n" + "=" * 60)
print("STEP 16: BEST VALUE PRODUCTS (HIGH RATING + HIGH DISCOUNT)")
print("=" * 60)

# CREATE VALUE SCORE — HIGHER MEANS BETTER DEAL
amazon_data['value_score'] = (
    amazon_data['rating_clean'] *
    np.log1p(amazon_data['discount_percentage_clean'])
)

top_value_products = amazon_data.nlargest(15, 'value_score')[
    ['product_name', 'rating_clean', 'discount_percentage_clean',
     'discounted_price_clean', 'value_score']
].reset_index(drop=True)

top_value_products['short_name'] = top_value_products['product_name'].str[:30] + '..'
print(top_value_products[['short_name', 'rating_clean',
                           'discount_percentage_clean', 'discounted_price_clean']])

# SCATTER PLOT
scatter_data = amazon_data.dropna(
    subset=['rating_clean', 'discount_percentage_clean', 'value_score']
)

fig, axis = plt.subplots(figsize=(13, 8), facecolor=COLOR_DARK)
axis.set_facecolor(COLOR_SURFACE)

scatter = axis.scatter(
    scatter_data['discount_percentage_clean'],
    scatter_data['rating_clean'],
    c=scatter_data['value_score'],
    cmap='YlOrRd',
    alpha=0.7, s=60, edgecolors='none'
)

# HIGHLIGHT TOP VALUE ZONE
axis.axhline(4.0, color=COLOR_GREEN, linestyle='--',
             linewidth=1.5, alpha=0.8, label='Good Rating (4.0+)')
axis.axvline(50, color=COLOR_ORANGE, linestyle='--',
             linewidth=1.5, alpha=0.8, label='High Discount (50%+)')

# ANNOTATE TOP VALUE ZONE
axis.text(70, 4.7, '🏆 BEST VALUE\nZONE', fontsize=13,
          color=COLOR_GREEN, fontweight='bold',
          bbox=dict(boxstyle='round,pad=0.4', facecolor='#1a2a1a',
                    edgecolor=COLOR_GREEN, alpha=0.8))

color_bar = plt.colorbar(scatter, ax=axis)
color_bar.set_label('Value Score', color='white', fontsize=11)
color_bar.ax.yaxis.set_tick_params(color='white')
plt.setp(color_bar.ax.yaxis.get_ticklabels(), color='white')

axis.set_title('🏆 Best Value Products\n(High Rating + High Discount = Best Deal)',
               fontsize=15, fontweight='bold', color='white', pad=20)
axis.set_xlabel('Discount Percentage (%)', fontsize=12)
axis.set_ylabel('Product Rating', fontsize=12)
axis.legend(fontsize=10, facecolor=COLOR_SURFACE, labelcolor='white')
axis.grid(alpha=0.2)
axis.spines['top'].set_visible(False)
axis.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('12_best_value_products.png', dpi=180, bbox_inches='tight',
            facecolor=COLOR_DARK)
plt.show()
print("SAVED: 12_best_value_products.png")
print("📌 INSIGHT: Products in the TOP-RIGHT zone (high rating + high discount)")
print("   represent the best deals on Amazon India.")


# ===================================================
# STEP 17: TOP SUB-CATEGORIES ANALYSIS
# WHAT IT SHOWS: WHICH SUB-CATEGORY HAS MOST PRODUCTS
# ===================================================
print("\n" + "=" * 60)
print("STEP 17: TOP SUB-CATEGORIES ANALYSIS")
print("=" * 60)

top_sub_categories       = amazon_data['sub_category'].value_counts().head(10)
top_sub_categories_pct   = np.round(top_sub_categories / len(amazon_data) * 100, 1)
print(top_sub_categories)

fig, axis = plt.subplots(figsize=(16, 8), facecolor=COLOR_DARK)
plt.subplots_adjust(left=0.35)
axis.set_facecolor(COLOR_SURFACE)

gradient_colors = [
    COLOR_ORANGE, '#FF8C00', '#FFA500', COLOR_BLUE, '#1A8FE3',
    '#2196F3', COLOR_GREEN, '#26A65B', '#27AE60', '#2ECC71'
]

bars = axis.barh(
    top_sub_categories.index[::-1],
    top_sub_categories.values[::-1],
    color=gradient_colors[::-1],
    edgecolor='none', height=0.6
)

axis.set_xlim(0, top_sub_categories.max() * 1.15)

for bar, val, pct in zip(
        bars,
        top_sub_categories.values[::-1],
        top_sub_categories_pct.values[::-1]):

    width = bar.get_width()

    if width > 50:
        x_pos = width - 3
        ha = 'right'
    else:
        x_pos = width + 3
        ha = 'left'

    axis.text(
        x_pos,
        bar.get_y() + bar.get_height() / 2,
        f'{val} ({pct}%)',
        va='center',
        ha=ha,
        color='white',
        fontweight='bold',
        fontsize=10
    )

axis.set_title('📂 Top 10 Sub-Categories on Amazon India',
               fontsize=16, fontweight='bold', color='white', pad=20)
axis.set_xlabel('Number of Products', fontsize=12)
axis.grid(axis='x', alpha=0.3)
axis.spines['top'].set_visible(False)
axis.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('13_top_subcategories.png', dpi=180, bbox_inches='tight',
            facecolor=COLOR_DARK)
plt.tight_layout()
plt.show()
print("SAVED: 13_top_subcategories.png")
print("📌 INSIGHT: Accessories & Peripherals is the largest sub-category,")
print("   showing strong demand for electronic accessories on Amazon India.")


# =======================================================
# STEP 18: HIGH DISCOUNT PRODUCTS ANALYSIS (>= 70%)
# WHAT IT SHOWS: WHICH CATEGORIES OFFER MASSIVE DISCOUNTS
# =======================================================
print("\n" + "=" * 60)
print("STEP 18: HIGH DISCOUNT PRODUCTS ANALYSIS (70%+ OFF)")
print("=" * 60)

high_discount_products    = amazon_data[amazon_data['discount_percentage_clean'] >= 70]
high_discount_by_category = high_discount_products['main_category'].value_counts()

print(f"Total Products with 70%+ Discount: {len(high_discount_products)}")
print(high_discount_by_category)

fig, axis = plt.subplots(figsize=(12, 7), facecolor=COLOR_DARK)
axis.set_facecolor(COLOR_SURFACE)

bars = axis.bar(
    range(len(high_discount_by_category)),
    high_discount_by_category.values,
    color=[COLOR_RED, COLOR_ORANGE, COLOR_BLUE, '#9B59B6', COLOR_GREEN]
    [:len(high_discount_by_category)],
    edgecolor='none', width=0.6
)

for bar, val in zip(bars, high_discount_by_category.values):
    axis.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        str(val),
        ha='center', color='white',
        fontweight='bold', fontsize=12
    )

short_names = [name[:15] + '..' if len(name) > 15
               else name for name in high_discount_by_category.index]
axis.set_xticks(range(len(high_discount_by_category)))
axis.set_xticklabels(short_names, rotation=20, ha='right', fontsize=11)

axis.set_title('🔥 Categories with Highest Discounts (70%+ OFF)',
               fontsize=15, fontweight='bold', color='white', pad=20)
axis.set_ylabel('Number of Products', fontsize=12)
axis.grid(axis='y', alpha=0.3)
axis.spines['top'].set_visible(False)
axis.spines['right'].set_visible(False)

axis.set_xticklabels(axis.get_xticklabels(), rotation=0, ha='center', fontsize=9)
plt.tight_layout()
plt.savefig('14_high_discount_products.png', dpi=180, bbox_inches='tight',
            facecolor=COLOR_DARK)
plt.show()
print("SAVED: 14_high_discount_products.png")
print("📌 INSIGHT: Electronics and Computers lead in 70%+ discounts,")
print("   making them the best categories for deal hunters on Amazon.")


# ========================================================
# STEP 19: PRICE vs RATING RELATIONSHIP
# WHAT IT SHOWS: DO EXPENSIVE PRODUCTS GET BETTER RATINGS?
# ========================================================
print("\n" + "=" * 60)
print("STEP 19: DOES PRICE AFFECT RATING?")
print("=" * 60)

price_rating_data = amazon_data.dropna(
    subset=['discounted_price_clean', 'rating_clean']
)

# FILTER EXTREME PRICES
price_rating_filtered = price_rating_data[
    price_rating_data['discounted_price_clean'] < 20000
]

price_values  = price_rating_filtered['discounted_price_clean'].values
rating_values = price_rating_filtered['rating_clean'].values

price_rating_correlation = np.corrcoef(price_values, rating_values)[0, 1]
print(f"Price vs Rating Correlation: {price_rating_correlation:.4f}")

# TREND LINE
trend_poly   = np.polyfit(price_values, rating_values, 1)
trend_line   = np.poly1d(trend_poly)
x_trend      = np.linspace(price_values.min(), price_values.max(), 100)

fig, axis = plt.subplots(figsize=(13, 7), facecolor=COLOR_DARK)
axis.set_facecolor(COLOR_SURFACE)

scatter = axis.scatter(
    price_values, rating_values,
    c=price_values, cmap='coolwarm',
    alpha=0.5, s=40, edgecolors='none'
)

axis.plot(x_trend, trend_line(x_trend),
          color=COLOR_ORANGE, linewidth=2.5,
          label=f'Trend Line (r = {price_rating_correlation:.3f})')

color_bar = plt.colorbar(scatter, ax=axis)
color_bar.set_label('Price (₹)', color='white', fontsize=11)
color_bar.ax.yaxis.set_tick_params(color='white')
plt.setp(color_bar.ax.yaxis.get_ticklabels(), color='white')

axis.set_title('💰 Does Price Affect Rating?\n(Higher Price = Better Rating?)',
               fontsize=15, fontweight='bold', color='white', pad=20)
axis.set_xlabel('Discounted Price (₹)', fontsize=12)
axis.set_ylabel('Product Rating', fontsize=12)
axis.legend(fontsize=11, facecolor=COLOR_SURFACE, labelcolor='white')
axis.grid(alpha=0.2)
axis.spines['top'].set_visible(False)
axis.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('15_price_vs_rating.png', dpi=180, bbox_inches='tight',
            facecolor=COLOR_DARK)
plt.show()
print("SAVED: 15_price_vs_rating.png")
print("📌 INSIGHT: Price and Rating show almost no correlation,")
print("   meaning expensive products are NOT necessarily better rated!")


# ========================================================
# STEP 20: AVERAGE DISCOUNT BY CATEGORY — RANKED
# WHAT IT SHOWS: WHICH CATEGORY GIVES MOST DISCOUNT ON AVG
# ========================================================
print("\n" + "=" * 60)
print("STEP 20: AVERAGE DISCOUNT % BY CATEGORY")
print("=" * 60)

avg_discount_by_category = (
    amazon_data.groupby('main_category')['discount_percentage_clean']
    .mean()
    .dropna()
    .sort_values(ascending=False)
)
avg_discount_by_category = np.round(avg_discount_by_category, 1)
print(avg_discount_by_category)

fig, axis = plt.subplots(figsize=(13, 7), facecolor=COLOR_DARK)
axis.set_facecolor(COLOR_SURFACE)

discount_bar_colors = [
    COLOR_GREEN if d >= 50 else
    COLOR_ORANGE if d >= 30 else COLOR_RED
    for d in avg_discount_by_category.values
]

bars = axis.barh(
    avg_discount_by_category.index[::-1],
    avg_discount_by_category.values[::-1],
    color=discount_bar_colors[::-1],
    edgecolor='none', height=0.6
)

for bar, val in zip(bars, avg_discount_by_category.values[::-1]):
    axis.text(
        bar.get_width() + 0.5,
        bar.get_y() + bar.get_height() / 2,
        f'{val}%',
        va='center', color='white',
        fontweight='bold', fontsize=11
    )

axis.axvline(50, color=COLOR_MUTED, linestyle='--',
             linewidth=1.5, alpha=0.7, label='50% Threshold')
axis.set_title('🏷️ Average Discount % by Category\n🟢 ≥50%  🟠 30–50%  🔴 <30%',
               fontsize=14, fontweight='bold', color='white', pad=20)
axis.set_xlabel('Average Discount (%)', fontsize=12)
axis.legend(fontsize=10, facecolor=COLOR_SURFACE, labelcolor='white')
axis.grid(axis='x', alpha=0.3)
axis.spines['top'].set_visible(False)
axis.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('16_avg_discount_by_category.png', dpi=180, bbox_inches='tight',
            facecolor=COLOR_DARK)
plt.show()
print("SAVED: 16_avg_discount_by_category.png")
print("📌 INSIGHT: Home Improvement & Computers offer the highest average discounts,")
print("   making them the best categories to shop during sales.")


# ============================================================
# STEP 21: REVIEW COUNT vs RATING
# WHAT IT SHOWS: DO MORE REVIEWED PRODUCTS HAVE BETTER RATINGS?
# POPULAR PRODUCTS MAY OR MAY NOT BE HIGHLY RATED
# ============================================================
print("\n" + "=" * 60)
print("STEP 21: REVIEW COUNT vs RATING ANALYSIS")
print("=" * 60)

review_rating_data = amazon_data.dropna(
    subset=['rating_count_clean', 'rating_clean']
)

# FILTER EXTREME REVIEW COUNTS
review_rating_filtered = review_rating_data[
    review_rating_data['rating_count_clean'] < 200000
]

review_counts  = review_rating_filtered['rating_count_clean'].values
rating_vals    = review_rating_filtered['rating_clean'].values

review_rating_corr = np.corrcoef(review_counts, rating_vals)[0, 1]
print(f"Review Count vs Rating Correlation: {review_rating_corr:.4f}")

fig, axis = plt.subplots(figsize=(13, 7), facecolor=COLOR_DARK)
axis.set_facecolor(COLOR_SURFACE)

scatter = axis.scatter(
    review_counts, rating_vals,
    c=rating_vals, cmap='RdYlGn',
    alpha=0.6, s=50, edgecolors='none',
    vmin=2, vmax=5
)

color_bar = plt.colorbar(scatter, ax=axis)
color_bar.set_label('Rating', color='white', fontsize=11)
color_bar.ax.yaxis.set_tick_params(color='white')
plt.setp(color_bar.ax.yaxis.get_ticklabels(), color='white')

axis.set_title('📊 Review Count vs Rating\n(Does Popularity = Quality?)',
               fontsize=15, fontweight='bold', color='white', pad=20)
axis.set_xlabel('Number of Reviews', fontsize=12)
axis.set_ylabel('Product Rating', fontsize=12)
axis.grid(alpha=0.2)
axis.spines['top'].set_visible(False)
axis.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('17_reviews_vs_rating.png', dpi=180, bbox_inches='tight',
            facecolor=COLOR_DARK)
plt.show()
print("SAVED: 17_reviews_vs_rating.png")
print("📌 INSIGHT: Products with more reviews tend to cluster around 4.0 rating,")
print("   suggesting popular products maintain consistent quality.")


# ============================================================
# STEP 22: TOP 8 HIGHEST RATED PRODUCTS
# WHAT IT SHOWS: HIGHEST RATED PRODUCTS WITH AT LEAST 100 REVIEWS
# ============================================================

print("\n" + "=" * 60)
print("STEP 22: TOP 8 HIGHEST RATED PRODUCTS")
print("=" * 60)

# Filter products with at least 100 reviews
credible_products = amazon_data[
    amazon_data['rating_count_clean'] >= 100
].copy()

# Remove duplicate products
credible_products = credible_products.drop_duplicates(subset='product_name')

# Top 8 highest-rated products
top_rated_products = (
    credible_products
    .sort_values(
        ['rating_clean', 'rating_count_clean'],
        ascending=[False, False]
    )
    .head(8)
    .reset_index(drop=True)
)

# Short names
top_rated_products['short_name'] = (
    top_rated_products['product_name']
    .str.slice(0, 35)
    .str.rstrip() + "..."
)

print(
    top_rated_products[
        ['short_name', 'rating_clean', 'rating_count_clean']
    ].to_string(index=False)
)

# Figure
fig, axis = plt.subplots(figsize=(15, 7), facecolor=COLOR_DARK)
axis.set_facecolor(COLOR_SURFACE)

# Bar colors
colors = [
    COLOR_ORANGE if i == 0 else
    COLOR_BLUE if i < 3 else
    COLOR_GREEN
    for i in range(len(top_rated_products))
]

bars = axis.barh(
    top_rated_products['short_name'],
    top_rated_products['rating_clean'],
    color=colors,
    edgecolor='none',
    height=0.6
)

# Highest at top
axis.invert_yaxis()

# Data labels
for bar, rating, count in zip(
    bars,
    top_rated_products['rating_clean'],
    top_rated_products['rating_count_clean']
):
    axis.annotate(
        f"⭐ {rating:.1f} ({int(count):,} reviews)",
        xy=(bar.get_width(), bar.get_y() + bar.get_height()/2),
        xytext=(8, 0),
        textcoords="offset points",
        va="center",
        ha="left",
        fontsize=9,
        fontweight="bold",
        color="white",
        clip_on=False
    )

# Formatting
axis.set_xlim(0, 5.2)

axis.set_title(
    "🥇 Top 8 Highest Rated Products\n(Min. 100 Reviews for Credibility)",
    fontsize=14,
    fontweight='bold',
    color='white',
    pad=20
)

axis.set_xlabel("Rating", fontsize=12, color='white')
axis.set_ylabel("")

axis.grid(axis='x', alpha=0.3)

axis.tick_params(axis='x', colors='white')
axis.tick_params(axis='y', colors='white')

axis.spines['top'].set_visible(False)
axis.spines['right'].set_visible(False)

plt.subplots_adjust(right=0.84)
plt.tight_layout()

plt.savefig(
    "18_top_rated_products.png",
    dpi=180,
    bbox_inches='tight',
    facecolor=COLOR_DARK
)

plt.show()

print("SAVED: 18_top_rated_products.png")
print("📌 INSIGHT: The top-rated products (minimum 100 reviews) span multiple categories,")
print("   indicating that outstanding customer satisfaction is achieved across diverse product types.")


# ============================================================
# STEP 23: CATEGORY-WISE AVERAGE ACTUAL PRICE
# WHAT IT SHOWS: WHICH CATEGORY IS MOST EXPENSIVE ORIGINALLY
# groupby().mean() CALCULATES AVG ORIGINAL PRICE PER CATEGORY
# CHART TYPE: GROUPED BAR — ACTUAL vs DISCOUNTED COMPARISON
# ============================================================
print("\n" + "=" * 60)
print("STEP 23: ACTUAL vs DISCOUNTED PRICE BY CATEGORY")
print("=" * 60)

price_comparison_by_category = amazon_data.groupby('main_category').agg(
    avg_actual_price      = ('actual_price_clean', 'mean'),
    avg_discounted_price  = ('discounted_price_clean', 'mean')
).dropna().sort_values('avg_actual_price', ascending=False)

price_comparison_by_category = np.round(price_comparison_by_category, 0)
print(price_comparison_by_category)

fig, axis = plt.subplots(figsize=(14, 8), facecolor=COLOR_DARK)
axis.set_facecolor(COLOR_SURFACE)

x_positions      = np.arange(len(price_comparison_by_category))
bar_width        = 0.35

actual_bars      = axis.bar(
    x_positions - bar_width / 2,
    price_comparison_by_category['avg_actual_price'],
    bar_width, label='Actual Price',
    color=COLOR_RED, edgecolor='none', alpha=0.85
)
discounted_bars  = axis.bar(
    x_positions + bar_width / 2,
    price_comparison_by_category['avg_discounted_price'],
    bar_width, label='Discounted Price',
    color=COLOR_GREEN, edgecolor='none', alpha=0.85
)

short_category_names = [name[:12] + '..' if len(name) > 12
                        else name for name in
                        price_comparison_by_category.index]
axis.set_xticks(x_positions)
axis.set_xticklabels(short_category_names, rotation=25,
                     ha='right', fontsize=10)

axis.set_title('💰 Avg Actual vs Discounted Price by Category',
               fontsize=15, fontweight='bold', color='white', pad=20)
axis.set_ylabel('Average Price (₹)', fontsize=12)
axis.legend(fontsize=11, facecolor=COLOR_SURFACE, labelcolor='white')
axis.grid(axis='y', alpha=0.3)
axis.spines['top'].set_visible(False)
axis.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('19_actual_vs_discounted_price.png', dpi=180,
            bbox_inches='tight', facecolor=COLOR_DARK)
plt.show()
print("SAVED: 19_actual_vs_discounted_price.png")
print("📌 INSIGHT: Electronics has the highest original price but also")
print("   the biggest gap after discount — best savings opportunity!")


# ============================================================
# STEP 24: UPDATED FINAL INSIGHTS SUMMARY
# PURE PANDAS & NUMPY — ALL KEY NUMBERS IN ONE PLACE
# ============================================================
print("\n" + "=" * 60)
print("STEP 24: FINAL INSIGHTS SUMMARY")
print("=" * 60)

# CALCULATE ALL SUMMARY METRICS
total_products_count      = len(amazon_data)
total_categories_count    = amazon_data['main_category'].nunique()
top_category_name         = amazon_data['main_category'].value_counts().idxmax()
top_subcategory_name      = amazon_data['sub_category'].value_counts().idxmax()
overall_avg_rating        = np.round(np.mean(amazon_data['rating_clean'].dropna()), 2)
overall_avg_discount      = np.round(np.mean(amazon_data['discount_percentage_clean'].dropna()), 1)
overall_avg_actual_price  = np.round(np.mean(amazon_data['actual_price_clean'].dropna()), 0)
overall_avg_disc_price    = np.round(np.mean(amazon_data['discounted_price_clean'].dropna()), 0)
overall_avg_savings       = np.round(np.mean(amazon_data['money_saved'].dropna()), 0)
highest_discount_product  = amazon_data.nlargest(1, 'discount_percentage_clean')['discount_percentage_clean'].values[0]
most_reviewed_product     = amazon_data.nlargest(1, 'rating_count_clean')['product_name'].values[0][:40]
best_rated_category_name  = amazon_data.groupby('main_category')['rating_clean'].mean().idxmax()
best_discount_category    = amazon_data.groupby('main_category')['discount_percentage_clean'].mean().idxmax()
excellent_products_count  = len(amazon_data[amazon_data['rating_clean'] >= 4.5])
budget_products_count     = len(amazon_data[amazon_data['discounted_price_clean'] <= 500])
high_discount_count       = len(amazon_data[amazon_data['discount_percentage_clean'] >= 70])
price_rating_corr_val     = np.round(np.corrcoef(
    amazon_data.dropna(subset=['discounted_price_clean','rating_clean'])['discounted_price_clean'],
    amazon_data.dropna(subset=['discounted_price_clean','rating_clean'])['rating_clean']
)[0,1], 3)

print(f"""
🛒 AMAZON INDIA EDA — COMPLETE FINAL SUMMARY
{'=' * 60}
📦 GENERAL
   Total Products Analyzed   : {total_products_count:,}
   Total Main Categories     : {total_categories_count}
   Top Category              : {top_category_name}
   Top Sub-Category          : {top_subcategory_name}

⭐ RATINGS
   Overall Average Rating    : {overall_avg_rating} / 5.0
   Excellent Products (4.5+) : {excellent_products_count}
   Best Rated Category       : {best_rated_category_name}

🏷️  DISCOUNTS
   Average Discount          : {overall_avg_discount}%
   Highest Discount          : {highest_discount_product:.0f}%
   Best Discount Category    : {best_discount_category}
   Products with 70%+ Off    : {high_discount_count}

💰 PRICING
   Avg Original Price        : ₹{overall_avg_actual_price:,.0f}
   Avg Discounted Price      : ₹{overall_avg_disc_price:,.0f}
   Avg Money Saved           : ₹{overall_avg_savings:,.0f}
   Budget Products (≤₹500)   : {budget_products_count}

📊 CORRELATIONS
   Price vs Rating           : {price_rating_corr_val} (Almost No Link)
   Most Reviewed Product     : {most_reviewed_product}...

{'=' * 60}

""")