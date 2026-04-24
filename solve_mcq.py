import pandas as pd
import numpy as np
import os

SEED = 42
np.random.seed(SEED)

print(f"Pandas version: {pd.__version__}")
print(f"Numpy version: {np.__version__}")

# Absolute path for reproducibility across working directories
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.join(_SCRIPT_DIR, 'dataset-datathon-2026-round-1') + os.sep

# Load data
orders = pd.read_csv(base_path + 'orders.csv', parse_dates=['order_date'])
products = pd.read_csv(base_path + 'products.csv')
returns = pd.read_csv(base_path + 'returns.csv')
web_traffic = pd.read_csv(base_path + 'web_traffic.csv')
order_items = pd.read_csv(base_path + 'order_items.csv', low_memory=False)
customers = pd.read_csv(base_path + 'customers.csv')
geography = pd.read_csv(base_path + 'geography.csv')
payments = pd.read_csv(base_path + 'payments.csv')

def format_vnd(value):
    """Format number to VND using comma as thousands separator (clear, no ambiguity)"""
    return f"{value:,.0f} VND"

print("--- MCQ ANSWERS & A/B/C/D MAPPING ---")

# Q1: Inter-order gap
multi_order_customers = orders['customer_id'].value_counts()
multi_order_customers = multi_order_customers[multi_order_customers > 1].index
multi_orders = orders[orders['customer_id'].isin(multi_order_customers)].sort_values(['customer_id', 'order_date'])
multi_orders['prev_order_date'] = multi_orders.groupby('customer_id')['order_date'].shift(1)
multi_orders['gap'] = (multi_orders['order_date'] - multi_orders['prev_order_date']).dt.days
q1_ans = multi_orders['gap'].median()
q1_choices = {30: 'A', 90: 'B', 180: 'C', 365: 'D'}
closest_q1 = min(q1_choices.keys(), key=lambda x: abs(x - q1_ans))
print(f"Q1: Median gap = {q1_ans} days -> CHỌN ĐÁP ÁN: {q1_choices[closest_q1]}")

# Q2: Gross margin
products['margin'] = (products['price'] - products['cogs']) / products['price']
q2_ans = products.groupby('segment')['margin'].mean().idxmax()
q2_choices = {'Premium': 'A', 'Performance': 'B', 'Activewear': 'C', 'Standard': 'D'}
print(f"Q2: Highest margin segment = {q2_ans} -> CHỌN ĐÁP ÁN: {q2_choices.get(q2_ans, 'Không có trong đáp án')}")

# Q3: Streetwear return reason
ret_prod = returns.merge(products, on='product_id')
streetwear_rets = ret_prod[ret_prod['category'] == 'Streetwear']
q3_ans = streetwear_rets['return_reason'].value_counts().idxmax()
q3_choices = {'defective': 'A', 'wrong_size': 'B', 'changed_mind': 'C', 'not_as_described': 'D'}
print(f"Q3: Most common return reason for Streetwear = {q3_ans} -> CHỌN ĐÁP ÁN: {q3_choices.get(q3_ans, 'Không có trong đáp án')}")

# Q4: Lowest bounce rate traffic source
q4_ans = web_traffic.groupby('traffic_source')['bounce_rate'].mean().idxmin()
q4_choices = {'organic_search': 'A', 'paid_search': 'B', 'email_campaign': 'C', 'social_media': 'D'}
print(f"Q4: Lowest bounce rate traffic source = {q4_ans} -> CHỌN ĐÁP ÁN: {q4_choices.get(q4_ans, 'Không có trong đáp án')}")

# Q5: Promo percentage
promo_pct = (order_items['promo_id'].notnull().sum() / len(order_items)) * 100
q5_choices = {12: 'A', 25: 'B', 39: 'C', 54: 'D'}
closest_q5 = min(q5_choices.keys(), key=lambda x: abs(x - promo_pct))
print(f"Q5: Promo percentage = {promo_pct:.2f}% -> CHỌN ĐÁP ÁN: {q5_choices[closest_q5]}")

# Q6: Age group with highest average orders per customer
valid_cust = customers[customers['age_group'].notnull()]
cust_orders = valid_cust.merge(orders, on='customer_id', how='left')
orders_per_group = cust_orders.groupby('age_group')['order_id'].nunique()
cust_per_group = valid_cust.groupby('age_group')['customer_id'].nunique()
q6_ans = (orders_per_group / cust_per_group).idxmax()
q6_choices = {'55+': 'A', '25-34': 'B', '35-44': 'C', '45-54': 'D'}
print(f"Q6: Age group with highest avg orders = {q6_ans} -> CHỌN ĐÁP ÁN: {q6_choices.get(q6_ans, 'Không có trong đáp án')}")

# Q7: Region with highest total revenue (GROSS = quantity * unit_price, matches sales.csv definition)
oi_rev = order_items.assign(revenue=order_items['quantity'] * order_items['unit_price'])
oi_ord_geo = (
    oi_rev.merge(orders[['order_id', 'zip']], on='order_id')
          .merge(geography[['zip', 'region']], on='zip')
)
gross_revs = oi_ord_geo.groupby('region')['revenue'].sum().sort_values(ascending=False)

print("\nQ7 Gross Doanh thu các vùng (khớp định nghĩa sales.csv):")
for r, val in gross_revs.items():
    print(f"  - {r}: {format_vnd(val)}")

q7_choices = {'West': 'A', 'Central': 'B', 'East': 'C'}
if gross_revs.max() / gross_revs.min() < 1.05:
    print("Q7: Doanh thu xấp xỉ bằng nhau -> CHỌN ĐÁP ÁN: D")
else:
    q7_ans = gross_revs.idxmax()
    print(f"Q7: Region with highest revenue = {q7_ans} -> CHỌN ĐÁP ÁN: {q7_choices.get(q7_ans, 'Không có trong đáp án')}\n")

# Q8: Payment method for cancelled orders
cancelled = orders[orders['order_status'] == 'cancelled']
q8_ans = cancelled['payment_method'].value_counts().idxmax()
q8_choices = {'credit_card': 'A', 'cod': 'B', 'paypal': 'C', 'bank_transfer': 'D'}
print(f"Q8: Most used payment method for cancelled = {q8_ans} -> CHỌN ĐÁP ÁN: {q8_choices.get(q8_ans, 'Không có trong đáp án')}")

# Q9: Size with highest return rate (đề định nghĩa: số bản ghi returns / số dòng order_items)
item_prod = order_items.merge(products[['product_id', 'size']], on='product_id')
ret_prod2 = returns.merge(products[['product_id', 'size']], on='product_id')
size_items = item_prod['size'].value_counts()
size_returns = ret_prod2['size'].value_counts()
return_rates = (size_returns / size_items * 100).sort_values(ascending=False)
q9_ans = return_rates.idxmax()
q9_choices = {'S': 'A', 'M': 'B', 'L': 'C', 'XL': 'D'}
print(f"Q9: Return rate theo rows: {return_rates.round(3).to_dict()}")
print(f"Q9: Size with highest return rate = {q9_ans} ({return_rates[q9_ans]:.2f}%) -> CHỌN ĐÁP ÁN: {q9_choices.get(q9_ans, 'Không có trong đáp án')}")

# Cross-check Q9 bằng quantity/return_quantity (đề phòng đề diễn giải khác)
size_units = item_prod.groupby('size')['quantity'].sum()
size_ret_units = ret_prod2.groupby('size')['return_quantity'].sum()
rate_by_units = (size_ret_units / size_units * 100).sort_values(ascending=False)
print(f"Q9 cross-check theo units: {rate_by_units.round(3).to_dict()} -> top = {rate_by_units.idxmax()}")

# Q10: Installment plan with highest average payment value (lọc về 4 lựa chọn đề cho)
payment_means = payments.groupby('installments')['payment_value'].mean()
q10_choices = {1: 'A', 3: 'B', 6: 'C', 12: 'D'}
payment_means_valid = payment_means.loc[[k for k in q10_choices if k in payment_means.index]]
print(f"Q10: Mean payment_value theo installments (chỉ 1/3/6/12):")
for k, v in payment_means_valid.sort_values(ascending=False).items():
    print(f"  - {k} kỳ: {format_vnd(v)}")
q10_ans = payment_means_valid.idxmax()
print(f"Q10: Installment plan with highest avg payment = {q10_ans} kỳ -> CHỌN ĐÁP ÁN: {q10_choices.get(q10_ans, 'Không có trong đáp án')}")

# --- FINAL ANSWERS (copy chuỗi bên dưới vào form nộp bài) ---
final_answers = {
    'Q1': q1_choices[closest_q1],
    'Q2': q2_choices.get(q2_ans, '?'),
    'Q3': q3_choices.get(q3_ans, '?'),
    'Q4': q4_choices.get(q4_ans, '?'),
    'Q5': q5_choices[closest_q5],
    'Q6': q6_choices.get(q6_ans, '?'),
    'Q7': q7_choices.get(q7_ans, '?'),
    'Q8': q8_choices.get(q8_ans, '?'),
    'Q9': q9_choices.get(q9_ans, '?'),
    'Q10': q10_choices.get(q10_ans, '?'),
}
print("\n" + "=" * 50)
print("FINAL ANSWERS (copy vào form nộp bài):")
print("=" * 50)
for q, a in final_answers.items():
    print(f"  {q}: {a}")
print(f"\nChuỗi copy nhanh: {','.join(final_answers.values())}")
