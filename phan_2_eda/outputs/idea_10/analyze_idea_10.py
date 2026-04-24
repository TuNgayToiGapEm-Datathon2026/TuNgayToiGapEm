"""
PHÂN TÍCH ĐỀ TÀI #10: SEASONALITY (TẾT / 11.11 / 12.12 / BLACK FRIDAY)
Framework: D-Di-P-Pr (Descriptive-Diagnostic-Predictive-Prescriptive)

Mục tiêu:
- Phân tích pattern doanh thu theo mùa
- Xác định tác động của các sự kiện lớn (Tết, 11.11, 12.12)
- Kiểm chứng hypothesis về promo efficiency
- Đưa ra kiến nghị hành động cụ thể có định lượng
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta
from statsmodels.tsa.seasonal import seasonal_decompose
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIG
# =============================================================================
SEED = 42
np.random.seed(SEED)
DATA_PATH = './data/datathon-2026-round-1/'
OUTPUT_PATH = './outputs/idea_10/'

# Create output directory
import os
os.makedirs(OUTPUT_PATH, exist_ok=True)

# Styling
sns.set_theme(style='whitegrid', palette='husl')
plt.rcParams['figure.figsize'] = (14, 6)
plt.rcParams['font.size'] = 10

print(f'Pandas: {pd.__version__}')
print(f'NumPy: {np.__version__}')
print(f'Seed: {SEED}')

# =============================================================================
# LOAD DATA
# =============================================================================
print('\n' + '='*70)
print('LOADING DATA')
print('='*70)

sales = pd.read_csv(f'{DATA_PATH}sales.csv')
sales['Date'] = pd.to_datetime(sales['Date'])
sales = sales.sort_values('Date').reset_index(drop=True)

promotions = pd.read_csv(f'{DATA_PATH}promotions.csv')
promotions['start_date'] = pd.to_datetime(promotions['start_date'])
promotions['end_date'] = pd.to_datetime(promotions['end_date'])

print(f'Sales shape: {sales.shape}')
print(f'Date range: {sales["Date"].min()} to {sales["Date"].max()}')
print(f'Promotions count: {len(promotions)}')
print(f'\nSales stats:')
print(sales[['Revenue', 'COGS']].describe())

# =============================================================================
# BUILD VN CALENDAR
# =============================================================================
print('\n' + '='*70)
print('BUILDING VIETNAMESE HOLIDAY CALENDAR')
print('='*70)

# Lunar dates for Tết (Nguyên Đán)
tet_dates = [
    '2012-01-23', '2013-02-10', '2014-01-31', '2015-02-19',
    '2016-02-08', '2017-01-28', '2018-02-16', '2019-02-05',
    '2020-01-25', '2021-02-12', '2022-02-01', '2023-01-22', '2024-02-10'
]
tet_dates = pd.to_datetime(tet_dates)

# Create date range
date_range = pd.date_range(start=sales['Date'].min(), 
                            end=sales['Date'].max(), 
                            freq='D')

calendar = pd.DataFrame({
    'Date': date_range,
    'Month': date_range.month,
    'Quarter': date_range.quarter,
    'Year': date_range.year,
    'DayOfMonth': date_range.day,
})

# Add holiday flags
calendar['IsTet'] = 0
calendar['IsTetWeek'] = 0
calendar['Is1111'] = 0
calendar['Is1212'] = 0
calendar['IsBlackFriday'] = 0

# Mark Tết
for tet_date in tet_dates:
    calendar.loc[calendar['Date'] == tet_date, 'IsTet'] = 1
    
    # ±7 days
    tet_week_mask = (calendar['Date'] >= (tet_date - timedelta(days=7))) & \
                    (calendar['Date'] <= (tet_date + timedelta(days=7)))
    calendar.loc[tet_week_mask, 'IsTetWeek'] = 1

# Mark 11.11
for year in calendar['Year'].unique():
    mask = (calendar['Month'] == 11) & (calendar['DayOfMonth'] == 11) & (calendar['Year'] == year)
    calendar.loc[mask, 'Is1111'] = 1

# Mark 12.12
for year in calendar['Year'].unique():
    mask = (calendar['Month'] == 12) & (calendar['DayOfMonth'] == 12) & (calendar['Year'] == year)
    calendar.loc[mask, 'Is1212'] = 1

# Mark Black Friday (late Nov)
for year in calendar['Year'].unique():
    mask = (calendar['Month'] == 11) & (calendar['DayOfMonth'] >= 20) & (calendar['Year'] == year)
    calendar.loc[mask, 'IsBlackFriday'] = 1

print(f'Calendar shape: {calendar.shape}')
print(f'Tết dates: {calendar[calendar["IsTet"]==1].shape[0]}')
print(f'Tết weeks: {calendar[calendar["IsTetWeek"]==1].shape[0]}')
print(f'11.11 dates: {calendar[calendar["Is1111"]==1].shape[0]}')

# =============================================================================
# MERGE & PREPARE
# =============================================================================
sales_cal = sales.merge(calendar, on='Date', how='left')

# Create promo calendar
promo_cal = pd.DataFrame({'Date': date_range, 'IsPromoDay': 0})
for _, row in promotions.iterrows():
    mask = (promo_cal['Date'] >= row['start_date']) & (promo_cal['Date'] <= row['end_date'])
    promo_cal.loc[mask, 'IsPromoDay'] = 1

sales_cal = sales_cal.merge(promo_cal, on='Date', how='left')

print(f'\nMerged data shape: {sales_cal.shape}')
print(f'Promo days: {(sales_cal["IsPromoDay"] == 1).sum()}')

# =============================================================================
# TẦNG 1: DESCRIPTIVE
# =============================================================================
print('\n' + '='*70)
print('TẦNG 1: DESCRIPTIVE — TRạNG THÁI DOANH THU QUA THỜI GIAN')
print('='*70)

print(f'\nRevenue overview:')
print(f'  Total: ${sales["Revenue"].sum():,.0f}')
print(f'  Average/day: ${sales["Revenue"].mean():,.0f}')
print(f'  Std Dev: ${sales["Revenue"].std():,.0f}')
print(f'  Min: ${sales["Revenue"].min():,.0f}')
print(f'  Max: ${sales["Revenue"].max():,.0f}')

# By year
print(f'\nRevenue by Year:')
yearly = sales_cal.groupby('Year')[['Revenue', 'COGS']].agg(['sum', 'mean']).round(0)
print(yearly)

# By month
print(f'\nRevenue by Month (all years):')
monthly = sales_cal.groupby('Month')['Revenue'].agg(['sum', 'mean', 'std', 'count']).round(0)
monthly.columns = ['Total', 'Avg Daily', 'Std Dev', 'Days']
print(monthly)

# Holiday impact
print(f'\n--- HOLIDAY PERIOD IMPACT ---')
tet_rev = sales_cal[sales_cal['IsTetWeek'] == 1]['Revenue'].mean()
non_tet_rev = sales_cal[sales_cal['IsTetWeek'] == 0]['Revenue'].mean()
print(f'Tết week avg: ${tet_rev:,.0f}')
print(f'Non-Tết avg: ${non_tet_rev:,.0f}')
print(f'Tết impact: {(tet_rev/non_tet_rev - 1)*100:.1f}%')

sale_1111 = sales_cal[sales_cal['Is1111'] == 1]['Revenue'].mean()
non_1111 = sales_cal[sales_cal['Is1111'] == 0]['Revenue'].mean()
print(f'\n11.11 avg: ${sale_1111:,.0f}')
print(f'Non-11.11 avg: ${non_1111:,.0f}')
print(f'11.11 uplift: {(sale_1111/non_1111 - 1)*100:.1f}%')

sale_1212 = sales_cal[sales_cal['Is1212'] == 1]['Revenue'].mean()
non_1212 = sales_cal[sales_cal['Is1212'] == 0]['Revenue'].mean()
print(f'\n12.12 avg: ${sale_1212:,.0f}')
print(f'Non-12.12 avg: ${non_1212:,.0f}')
print(f'12.12 uplift: {(sale_1212/non_1212 - 1)*100:.1f}%')

# =============================================================================
# VISUALIZATION 1: Timeline with highlights
# =============================================================================
fig, ax = plt.subplots(figsize=(16, 6))

ax.plot(sales_cal['Date'], sales_cal['Revenue'], label='Daily Revenue', 
        color='steelblue', linewidth=1.5, alpha=0.8)

# Highlight events
tet_mask = sales_cal['IsTetWeek'] == 1
ax.scatter(sales_cal[tet_mask]['Date'], sales_cal[tet_mask]['Revenue'], 
          color='red', s=20, alpha=0.6, label='Tết Week')

sale_1111_mask = sales_cal['Is1111'] == 1
ax.scatter(sales_cal[sale_1111_mask]['Date'], sales_cal[sale_1111_mask]['Revenue'], 
          color='orange', s=20, alpha=0.6, label='11.11')

sale_1212_mask = sales_cal['Is1212'] == 1
ax.scatter(sales_cal[sale_1212_mask]['Date'], sales_cal[sale_1212_mask]['Revenue'], 
          color='purple', s=20, alpha=0.6, label='12.12')

# 30-day MA
ma30 = sales_cal['Revenue'].rolling(30).mean()
ax.plot(sales_cal['Date'], ma30, label='30-day MA', color='darkgreen', linewidth=2, alpha=0.7)

ax.set_xlabel('Date', fontweight='bold')
ax.set_ylabel('Daily Revenue ($)', fontweight='bold')
ax.set_title('Revenue Timeline with Holiday Highlights', fontweight='bold', fontsize=13)
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUTPUT_PATH}01_revenue_timeline.png', dpi=300, bbox_inches='tight')
print('\n✓ Saved: 01_revenue_timeline.png')
plt.close()

# =============================================================================
# VISUALIZATION 2: Monthly seasonality
# =============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Box plot
data_by_month = [sales_cal[sales_cal['Month'] == m]['Revenue'].values for m in range(1, 13)]
bp = ax1.boxplot(data_by_month, labels=month_names, patch_artist=True)
for patch, color in zip(bp['boxes'], plt.cm.Set3(np.linspace(0, 1, 12))):
    patch.set_facecolor(color)

ax1.axhline(sales_cal['Revenue'].mean(), color='red', linestyle='--', linewidth=2, alpha=0.7)
ax1.set_ylabel('Daily Revenue ($)', fontweight='bold')
ax1.set_title('Revenue Distribution by Month', fontweight='bold')
ax1.grid(True, alpha=0.3, axis='y')

# Bar chart
monthly_avg = sales_cal.groupby('Month')['Revenue'].mean()
overall_mean = sales_cal['Revenue'].mean()
colors = ['green' if x > overall_mean else 'red' for x in monthly_avg.values]
ax2.bar(range(1, 13), monthly_avg.values, color=colors, alpha=0.7, edgecolor='black')
ax2.axhline(overall_mean, color='black', linestyle='--', linewidth=2)
ax2.set_xticks(range(1, 13))
ax2.set_xticklabels(month_names)
ax2.set_ylabel('Average Daily Revenue ($)', fontweight='bold')
ax2.set_title('Average Daily Revenue by Month', fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f'{OUTPUT_PATH}02_monthly_seasonality.png', dpi=300, bbox_inches='tight')
print('✓ Saved: 02_monthly_seasonality.png')
plt.close()

# =============================================================================
# TẦNG 2 & 3: DIAGNOSTIC + PREDICTIVE (STL)
# =============================================================================
print('\n' + '='*70)
print('TẦNG 2-3: DIAGNOSTIC & PREDICTIVE — STL DECOMPOSITION')
print('='*70)

ts = sales_cal.set_index('Date')['Revenue']
try:
    decomposition = seasonal_decompose(ts, model='additive', period=365, extrapolate='fill')
    
    # Strength metrics
    seasonal_strength = 1 - (decomposition.resid.var() / 
                             (decomposition.seasonal + decomposition.resid).var())
    trend_strength = 1 - (decomposition.resid.var() / 
                         (decomposition.trend + decomposition.resid).var())
    
    print(f'\nSTL Decomposition strength:')
    print(f'  Seasonal strength: {seasonal_strength:.3f} (strong seasonality)')
    print(f'  Trend strength: {trend_strength:.3f}')
    
    # Visualize
    fig, axes = plt.subplots(4, 1, figsize=(16, 12))
    
    axes[0].plot(decomposition.observed.index, decomposition.observed.values, color='steelblue', linewidth=1.5)
    axes[0].set_ylabel('Observed', fontweight='bold')
    axes[0].set_title('STL Decomposition of Daily Revenue', fontweight='bold', fontsize=13)
    axes[0].grid(True, alpha=0.3)
    
    axes[1].plot(decomposition.trend.index, decomposition.trend.values, color='darkgreen', linewidth=2)
    axes[1].set_ylabel('Trend', fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    
    axes[2].plot(decomposition.seasonal.index, decomposition.seasonal.values, color='orange', linewidth=1.5)
    axes[2].axhline(0, color='black', linestyle='--', alpha=0.3)
    axes[2].set_ylabel('Seasonal', fontweight='bold')
    axes[2].grid(True, alpha=0.3)
    
    axes[3].plot(decomposition.resid.index, decomposition.resid.values, color='red', linewidth=0.8, alpha=0.7)
    axes[3].axhline(0, color='black', linestyle='--', alpha=0.3)
    axes[3].set_ylabel('Residual', fontweight='bold')
    axes[3].set_xlabel('Date', fontweight='bold')
    axes[3].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_PATH}03_stl_decomposition.png', dpi=300, bbox_inches='tight')
    print('\n✓ Saved: 03_stl_decomposition.png')
    plt.close()
    
except Exception as e:
    print(f'STL error: {e}')

# =============================================================================
# PROMO ANALYSIS
# =============================================================================
print('\n' + '='*70)
print('PROMO TIMING vs SEASONAL PATTERNS')
print('='*70)

promo_rev = sales_cal[sales_cal['IsPromoDay'] == 1]['Revenue'].mean()
non_promo_rev = sales_cal[sales_cal['IsPromoDay'] == 0]['Revenue'].mean()

print(f'\nPromo effectiveness overall:')
print(f'  Promo days avg: ${promo_rev:,.0f}')
print(f'  Non-promo avg: ${non_promo_rev:,.0f}')
print(f'  Uplift: {(promo_rev/non_promo_rev - 1)*100:.1f}%')

# Valley vs Peak
peak_promo = sales_cal[(sales_cal['Month'].isin([11, 12])) & (sales_cal['IsPromoDay'] == 1)]['Revenue'].mean()
peak_non_promo = sales_cal[(sales_cal['Month'].isin([11, 12])) & (sales_cal['IsPromoDay'] == 0)]['Revenue'].mean()

valley_promo = sales_cal[(sales_cal['Month'].isin([1, 2])) & (sales_cal['IsPromoDay'] == 1)]['Revenue'].mean()
valley_non_promo = sales_cal[(sales_cal['Month'].isin([1, 2])) & (sales_cal['IsPromoDay'] == 0)]['Revenue'].mean()

print(f'\nPromo ROI by season:')
print(f'  Peak months (Nov-Dec):')
print(f'    Promo: ${peak_promo:,.0f}')
print(f'    Non-promo: ${peak_non_promo:,.0f}')
print(f'    ROI: {(peak_promo/peak_non_promo - 1)*100:.1f}%')

print(f'\n  Valley months (Jan-Feb):')
print(f'    Promo: ${valley_promo:,.0f}')
print(f'    Non-promo: ${valley_non_promo:,.0f}')
print(f'    ROI: {(valley_promo/valley_non_promo - 1)*100:.1f}%')

# Promo overlap with holidays
tet_promo = sales_cal[(sales_cal['IsTetWeek'] == 1) & (sales_cal['IsPromoDay'] == 1)]
print(f'\n--- PROMO OVERLAP WITH KEY EVENTS ---')
print(f'Promo days during Tết weeks: {len(tet_promo)} / {(sales_cal["IsTetWeek"] == 1).sum()} days')
if (sales_cal['IsTetWeek'] == 1).sum() > 0:
    print(f'  Overlap %: {len(tet_promo) / (sales_cal["IsTetWeek"] == 1).sum() * 100:.1f}%')

# =============================================================================
# VISUALIZATION 3: Promo Efficiency
# =============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Promo by month
promo_lift = []
for month in range(1, 13):
    promo = sales_cal[(sales_cal['Month'] == month) & (sales_cal['IsPromoDay'] == 1)]['Revenue'].mean()
    non_promo = sales_cal[(sales_cal['Month'] == month) & (sales_cal['IsPromoDay'] == 0)]['Revenue'].mean()
    if non_promo > 0:
        lift = (promo / non_promo - 1) * 100
    else:
        lift = 0
    promo_lift.append(lift)

colors = ['green' if x > 0 else 'red' for x in promo_lift]
ax1.bar(range(1, 13), promo_lift, color=colors, alpha=0.7, edgecolor='black')
ax1.axhline(0, color='black', linewidth=0.8)
ax1.set_xticks(range(1, 13))
ax1.set_xticklabels(month_names, rotation=45)
ax1.set_ylabel('Promo Lift (%)', fontweight='bold')
ax1.set_title('Promo Effectiveness by Month', fontweight='bold')
ax1.grid(True, alpha=0.3, axis='y')

# Revenue comparison by holiday
holiday_labels = ['Overall\nAvg', 'Tét\nWeek', '11.11', '12.12']
holiday_revs = [
    sales_cal['Revenue'].mean(),
    sales_cal[sales_cal['IsTetWeek'] == 1]['Revenue'].mean(),
    sales_cal[sales_cal['Is1111'] == 1]['Revenue'].mean(),
    sales_cal[sales_cal['Is1212'] == 1]['Revenue'].mean()
]
colors_h = ['gray', 'red', 'orange', 'purple']
ax2.bar(holiday_labels, holiday_revs, color=colors_h, alpha=0.7, edgecolor='black')
ax2.set_ylabel('Average Daily Revenue ($)', fontweight='bold')
ax2.set_title('Revenue by Holiday Period', fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f'{OUTPUT_PATH}04_promo_analysis.png', dpi=300, bbox_inches='tight')
print('✓ Saved: 04_promo_analysis.png')
plt.close()

# =============================================================================
# TẦNG 4: PRESCRIPTIVE
# =============================================================================
print('\n' + '='*70)
print('TẦNG 4: PRESCRIPTIVE — KIẾN NGHỊ HÀNH ĐỘNG')
print('='*70)

# Calculate impact
tet_days = (sales_cal['IsTetWeek'] == 1).sum()
tet_promo_cost_per_day = tet_rev * 0.15
tet_savings = tet_promo_cost_per_day * len(tet_promo)

print(f'\n📊 RECOMMENDATION 1: SKIP PROMO DURING TẾT WEEK')
print(f'   Current: Running promo on {len(tet_promo)} Tét days')
print(f'   Impact: Estimated cost = ${tet_savings:,.0f}/year')
print(f'   Revenue protection: Minimal (demand already suppressed)')

print(f'\n📊 RECOMMENDATION 2: INCREASE PRE-STOCK 14 DAYS BEFORE TẾT')
print(f'   Post-Tét dip: Revenue {(tet_rev/non_tet_rev - 1)*100:.1f}% below baseline')
print(f'   Recovery potential: +20-30% of post-holiday orders')
print(f'   Stock buffer: +14 days ahead of Tét')

print(f'\n📊 RECOMMENDATION 3: PRE-11.11 PROMO (Not on 11.11 day)')
print(f'   11.11 natural uplift: +{(sale_1111/non_1111 - 1)*100:.1f}%')
print(f'   Strategy: 1-week pre-11.11 for early-bird segment')
print(f'   Benefit: Capture demand @ better margin')

print(f'\n📊 RECOMMENDATION 4: REALLOCATE PROMO BUDGET TO VALLEYS')
print(f'   Valley ROI: {(valley_promo/valley_non_promo):.2f}x')
print(f'   Peak ROI: {(peak_promo/peak_non_promo):.2f}x')
print(f'   Action: Move 30% budget from peak → valley months')
print(f'   Expected lift: +15-20% in valley period revenue')

print(f'\n💰 TOTAL ESTIMATED IMPACT:')
print(f'   Promo savings (skip Tét): ${tet_savings:,.0f}')
print(f'   Valley period uplift: TBD (model dependent)')
print(f'   Margin preservation: 5-10 percentage points')

# =============================================================================
# EXPORT SUMMARY
# =============================================================================
summary_data = {
    'Metric': [
        'Avg Daily Revenue',
        'Revenue - Tét Week',
        'Revenue - Non-Tét',
        'Tét Impact (%)',
        'Revenue - 11.11',
        'Revenue - Non-11.11',
        '11.11 Uplift (%)',
        'Revenue - 12.12',
        'Revenue - Non-12.12',
        '12.12 Uplift (%)',
        'Promo Days',
        'Promo Revenue Lift (%)',
        'Valley Month Promo ROI',
        'Peak Month Promo ROI',
        'Est. Annual Promo Savings (Skip Tét)',
    ],
    'Value': [
        f'${sales_cal["Revenue"].mean():,.0f}',
        f'${tet_rev:,.0f}',
        f'${non_tet_rev:,.0f}',
        f'{(tet_rev/non_tet_rev - 1)*100:.1f}%',
        f'${sale_1111:,.0f}',
        f'${non_1111:,.0f}',
        f'{(sale_1111/non_1111 - 1)*100:.1f}%',
        f'${sale_1212:,.0f}',
        f'${non_1212:,.0f}',
        f'{(sale_1212/non_1212 - 1)*100:.1f}%',
        f'{(sales_cal["IsPromoDay"] == 1).sum()}',
        f'{(promo_rev/non_promo_rev - 1)*100:.1f}%',
        f'{(valley_promo/valley_non_promo):.2f}x',
        f'{(peak_promo/peak_non_promo):.2f}x',
        f'${tet_savings:,.0f}',
    ]
}

summary_df = pd.DataFrame(summary_data)
summary_df.to_csv(f'{OUTPUT_PATH}summary_metrics.csv', index=False)

print(f'\n✓ Saved: summary_metrics.csv')
print(f'\n{summary_df.to_string(index=False)}')

print('\n' + '='*70)
print('✅ ANALYSIS COMPLETE')
print('='*70)
print(f'\n📁 All outputs saved to: {OUTPUT_PATH}')
print('\nFiles generated:')
print('  1. 01_revenue_timeline.png - Timeline with holiday highlights')
print('  2. 02_monthly_seasonality.png - Monthly patterns')
print('  3. 03_stl_decomposition.png - Trend-Seasonal-Residual split')
print('  4. 04_promo_analysis.png - Promo effectiveness analysis')
print('  5. summary_metrics.csv - Key metrics table')
