# Giải pháp Phần 1 - Trắc nghiệm MCQ (Datathon 2026 Round 1)

Dựa trên tài liệu `CLAUDE.md` và phân tích đề bài, dưới đây là chi tiết logic xử lý và mã nguồn Pandas để giải quyết 10 câu hỏi trắc nghiệm (MCQ). Hãy copy đoạn mã này vào notebook `02_mcq.ipynb` để trích xuất đáp án cuối cùng.

## Cài đặt thư viện và Load dữ liệu
```python
import pandas as pd
import numpy as np

# Đường dẫn đến thư mục chứa dữ liệu
DATA_DIR = '../dataset-datathon-2026-round-1/'

orders = pd.read_csv(f'{DATA_DIR}orders.csv', parse_dates=['order_date'])
products = pd.read_csv(f'{DATA_DIR}products.csv')
returns = pd.read_csv(f'{DATA_DIR}returns.csv')
web_traffic = pd.read_csv(f'{DATA_DIR}web_traffic.csv')
order_items = pd.read_csv(f'{DATA_DIR}order_items.csv')
customers = pd.read_csv(f'{DATA_DIR}customers.csv')
geography = pd.read_csv(f'{DATA_DIR}geography.csv')
payments = pd.read_csv(f'{DATA_DIR}payments.csv')
```

---

## Q1. Trung vị số ngày giữa hai lần mua liên tiếp
**Logic**: Lọc khách hàng có `> 1` đơn hàng. Sắp xếp đơn hàng theo `customer_id` và `order_date`. Dùng `shift(1)` để tính độ lệch số ngày (gap), sau đó tính trung vị.
```python
customer_order_counts = orders['customer_id'].value_counts()
multi_order_customers = customer_order_counts[customer_order_counts > 1].index

multi_orders = orders[orders['customer_id'].isin(multi_order_customers)].copy()
multi_orders = multi_orders.sort_values(by=['customer_id', 'order_date'])

multi_orders['prev_order_date'] = multi_orders.groupby('customer_id')['order_date'].shift(1)
multi_orders['gap_days'] = (multi_orders['order_date'] - multi_orders['prev_order_date']).dt.days

ans_q1 = multi_orders['gap_days'].median()
print(f"Q1 Answer: {ans_q1} ngày")
```

## Q2. Phân khúc có tỷ suất lợi nhuận gộp (Gross Margin) trung bình cao nhất
**Logic**: Tính margin = `(price - cogs) / price` cho từng sản phẩm. Groupby `segment` và lấy trung bình cao nhất.
```python
products['margin'] = (products['price'] - products['cogs']) / products['price']
ans_q2 = products.groupby('segment')['margin'].mean().idxmax()
print(f"Q2 Answer: {ans_q2}")
```

## Q3. Lý do trả hàng phổ biến nhất cho danh mục "Streetwear"
**Logic**: Join `returns` với `products` qua `product_id`. Lọc `category == 'Streetwear'`. Đếm số lần xuất hiện của `return_reason`.
```python
ret_prod = returns.merge(products, on='product_id')
streetwear_rets = ret_prod[ret_prod['category'] == 'Streetwear']
ans_q3 = streetwear_rets['return_reason'].value_counts().idxmax()
print(f"Q3 Answer: {ans_q3}")
```

## Q4. Nguồn traffic có tỷ lệ thoát (bounce_rate) trung bình thấp nhất
**Logic**: Groupby `traffic_source` trong bảng `web_traffic` tính mean của `bounce_rate`. Lấy giá trị nhỏ nhất.
```python
ans_q4 = web_traffic.groupby('traffic_source')['bounce_rate'].mean().idxmin()
print(f"Q4 Answer: {ans_q4}")
```

## Q5. Tỷ lệ dòng trong order_items có áp dụng khuyến mãi
**Logic**: Đếm số dòng có `promo_id` không null chia cho tổng số dòng của `order_items`.
```python
promo_applied = order_items['promo_id'].notnull().sum()
ans_q5 = (promo_applied / len(order_items)) * 100
print(f"Q5 Answer: {ans_q5:.2f}%")
```

## Q6. Nhóm tuổi có số đơn hàng trung bình cao nhất
**Logic**: Bỏ null trong `age_group`. Join `customers` với `orders` (Left join để đếm khách chưa mua nếu có). Đếm tổng số lượng đơn hàng / số lượng khách hàng độc nhất của nhóm tuổi đó.
```python
valid_customers = customers[customers['age_group'].notnull()]
cust_orders = valid_customers.merge(orders, on='customer_id', how='left')

orders_per_group = cust_orders.groupby('age_group')['order_id'].nunique()
users_per_group = valid_customers.groupby('age_group')['customer_id'].nunique()

avg_orders_per_group = orders_per_group / users_per_group
ans_q6 = avg_orders_per_group.idxmax()
print(f"Q6 Answer: {ans_q6}")
```

## Q7. Region tạo ra tổng doanh thu cao nhất
**Logic**: Dựa theo rule tính revenue của BTC: `doanh thu = quantity * unit_price` (chú ý `unit_price` đã bao gồm giảm giá). Join `order_items` -> `orders` -> `geography` để sum revenue theo vùng.
```python
order_items['revenue'] = order_items['quantity'] * order_items['unit_price']
oi_ord = order_items.merge(orders[['order_id', 'zip']], on='order_id')
oi_ord_geo = oi_ord.merge(geography[['zip', 'region']], on='zip')

ans_q7 = oi_ord_geo.groupby('region')['revenue'].sum().idxmax()
print(f"Q7 Answer: {ans_q7}")
```

## Q8. Phương thức thanh toán được dùng nhiều nhất ở các đơn bị "cancelled"
**Logic**: Lọc `order_status == 'cancelled'` trong bảng `orders`. Đếm tần suất của `payment_method`.
```python
cancelled_orders = orders[orders['order_status'] == 'cancelled']
ans_q8 = cancelled_orders['payment_method'].value_counts().idxmax()
print(f"Q8 Answer: {ans_q8}")
```

## Q9. Kích thước (size) có tỷ lệ trả hàng cao nhất
**Logic**: Tính tỷ lệ trả hàng (return_rate) cho từng size: `số dòng trong returns theo size / số dòng trong order_items theo size`.
```python
items_with_size = order_items.merge(products[['product_id', 'size']], on='product_id')
returns_with_size = returns.merge(products[['product_id', 'size']], on='product_id')

size_counts_items = items_with_size['size'].value_counts()
size_counts_returns = returns_with_size['size'].value_counts()

return_rate_by_size = (size_counts_returns / size_counts_items) * 100
ans_q9 = return_rate_by_size.idxmax()
print(f"Q9 Answer: {ans_q9}")
```

## Q10. Kế hoạch trả góp có thanh toán trung bình cao nhất
**Logic**: Groupby `installments` trong bảng `payments`, tính mean của `payment_value`.
```python
ans_q10 = payments.groupby('installments')['payment_value'].mean().idxmax()
print(f"Q10 Answer: {ans_q10}")
```
