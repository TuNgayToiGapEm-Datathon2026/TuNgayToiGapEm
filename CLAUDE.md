# CLAUDE.md — Bộ não dự án Datathon 2026 Round 1

> **Dành cho Claude sessions tương lai**: Đây là context toàn cục. Đọc file này TRƯỚC KHI làm bất kỳ việc gì. Nếu §12 còn câu hỏi chưa trả lời → hỏi user ngay đầu phiên.

---

## §1 — Bối cảnh cuộc thi

- **Tên**: Datathon 2026 Round 1 — "The Gridbreakers"
- **Chủ đề**: *Breaking Business Boundaries*
- **Đơn vị tổ chức**: VinTelligence — VinUniversity Data Science & AI Club
- **Vai trò giả định**: Data Scientist tại một công ty thời trang TMĐT Việt Nam
- **Chung kết**: 2026-05-23 tại VinUniversity, Hà Nội
- **Kaggle competition**: https://www.kaggle.com/competitions/datathon-2026-round-1
- **LaTeX template**: NeurIPS 2025 — https://neurips.cc/Conferences/2025/CallForPapers
- **Cơ cấu điểm**: 100đ = Part 1 MCQ (20đ) + Part 2 EDA (60đ) + Part 3 Forecasting (20đ)
- **Số thành viên**: 2-4 người / đội
- **Dataset**: 14 file CSV (PDF §1.1 ghi "15 file CSV" nhưng Table 1 chỉ liệt kê 14), ~130MB, 10.5 năm lịch sử (2012-07 → 2022-12) của một công ty thời trang TMĐT VN

### Bối cảnh kinh doanh (motivation cho forecasting — từ `Đề thi Vòng 1.pdf` §2.3.1 + Rule_book "Bối cảnh kinh doanh")

Bạn đóng vai Data Scientist tại công ty thời trang TMĐT VN. Doanh nghiệp cần dự báo **nhu cầu** (demand) chính xác ở mức **chi tiết theo ngày** để:
1. **Tối ưu hoá phân bổ tồn kho** — biết bán bao nhiêu để nhập đủ, không thừa.
2. **Lập kế hoạch khuyến mãi** — chọn đúng thời điểm chạy promo theo dự báo demand.
3. **Quản lý logistics trên toàn quốc** — phân bổ hàng giữa các vùng (East/Central/West).

→ Mọi insight EDA & feature model nên kết nối ngược về 1 trong 3 mục tiêu này khi viết phần Prescriptive.

---

## §2 — 3 phần thi chi tiết

### Part 1 — MCQ (20đ)
- 10 câu × 2 điểm = 20 điểm
- **Không trừ điểm câu sai** — luôn đoán kể cả khi không chắc
- Chỉ chọn **1 đáp án** / câu
- Câu hỏi tính trực tiếp từ dataset CSV

**10 câu hỏi nguyên văn** (từ `Đề thi Vòng 1.pdf` tr.7-10):

**Q1.** Trong số các khách hàng có nhiều hơn một đơn hàng, **trung vị số ngày giữa hai lần mua liên tiếp** (inter-order gap) xấp xỉ là bao nhiêu? (Tính từ `orders.csv`)
- A) 30 ngày · B) 90 ngày · C) 180 ngày · D) 365 ngày

**Q2.** Phân khúc sản phẩm (segment) nào trong `products.csv` có **tỷ suất lợi nhuận gộp trung bình** cao nhất, với công thức `(price - cogs) / price`?
- A) Premium · B) Performance · C) Activewear · D) Standard

**Q3.** Trong các bản ghi trả hàng liên kết với sản phẩm thuộc danh mục **Streetwear** (join `returns` với `products` theo `product_id`), **lý do trả hàng** nào xuất hiện nhiều nhất?
- A) `defective` · B) `wrong_size` · C) `changed_mind` · D) `not_as_described`

**Q4.** Trong `web_traffic.csv`, nguồn truy cập (`traffic_source`) nào có **tỷ lệ thoát trung bình** (`bounce_rate`) **thấp nhất** trên tất cả các ngày xuất hiện nguồn đó trong cột `traffic_source`?
- A) `organic_search` · B) `paid_search` · C) `email_campaign` · D) `social_media`

**Q5.** Tỷ lệ phần trăm các dòng trong `order_items.csv` có áp dụng khuyến mãi (tức là `promo_id` không null) xấp xỉ là bao nhiêu?
- A) 12% · B) 25% · C) 39% · D) 54%

**Q6.** Trong `customers.csv`, xét các khách hàng có `age_group` khác null, nhóm tuổi nào có **số đơn hàng trung bình trên mỗi khách hàng** cao nhất? (tổng số đơn / số khách hàng trong nhóm)
- A) 55+ · B) 25-34 · C) 35-44 · D) 45-54

**Q7.** Vùng (region) nào trong `geography.csv` tạo ra **tổng doanh thu cao nhất** trong `sales_train.csv`?
- A) West · B) Central · C) East · D) Cả ba vùng có doanh thu xấp xỉ bằng nhau
- **Ghi chú**: đề gọi là `sales_train.csv` nhưng file thực tế là `sales.csv`. Doanh thu ở đây phải join qua `orders.zip → geography.region` và sum theo region (KHÔNG có region trong sales.csv).

**Q8.** Trong các đơn hàng có `order_status = 'cancelled'` trong `orders.csv`, **phương thức thanh toán** nào được sử dụng nhiều nhất?
- A) `credit_card` · B) `cod` · C) `paypal` · D) `bank_transfer`

**Q9.** Trong bốn kích thước sản phẩm (S, M, L, XL), kích thước nào có **tỷ lệ trả hàng cao nhất**, được định nghĩa là số bản ghi trong `returns` chia cho số dòng trong `order_items` (join với `products` theo `product_id`)?
- A) S · B) M · C) L · D) XL

**Q10.** Trong `payments.csv`, **kế hoạch trả góp** nào có **giá trị thanh toán trung bình trên mỗi đơn hàng** cao nhất?
- A) 1 kỳ (trả một lần) · B) 3 kỳ · C) 6 kỳ · D) 12 kỳ

### Part 2 — EDA & Data Visualization (60đ) — **trọng số lớn nhất, ưu tiên cao nhất**

Rubric (nguồn: `Đề thi Vòng 1.pdf` tr.13-14, Bảng tiêu chí EDA):
| Tiêu chí | Điểm tối đa |
|---|---|
| Chất lượng trực quan hoá (chart có title/axis/legend, chọn loại chart phù hợp, thẩm mỹ) | 15 |
| Chiều sâu phân tích (phủ đủ 4 tầng Descriptive→Diagnostic→Predictive→Prescriptive) | 25 |
| Insight kinh doanh (actionable, định lượng, gắn data → decision) | 15 |
| Tính sáng tạo & kể chuyện (góc nhìn độc đáo, narrative xuyên suốt, tích hợp nhiều bảng) | 5 |

**Bảng band điểm chi tiết từng tiêu chí** (dùng để tự chấm — nguồn: `Đề thi Vòng 1.pdf` tr.14):

| Tiêu chí | Band cao | Band trung | Band thấp |
|---|---|---|---|
| Trực quan hoá (15đ) | **13–15**: tất cả chart đạt chuẩn, chọn loại tối ưu | **8–12**: phần lớn đạt, một số thiếu nhãn | **0–7**: thiếu thông tin, khó đọc |
| Chiều sâu (25đ) | **21–25**: đạt cả 4 tầng nhất quán | **14–20**: đạt 3 tầng, Prescriptive còn hời hợt | **7–13** chỉ Descriptive+Diagnostic · **0–6** chỉ mô tả bề mặt |
| Insight (15đ) | **13–15**: đề xuất cụ thể, định lượng, áp dụng ngay | **8–12**: có đề xuất chung chung | **0–7**: thiếu kết nối business |
| Sáng tạo (5đ) | **4–5**: góc độc đáo, kết hợp đa nguồn, narrative thuyết phục | **2–3**: có điểm sáng tạo nhưng chưa nhất quán | **0–1**: dự đoán được, không nổi bật |

**4 tầng phân tích bắt buộc phủ đủ** (mỗi tầng = 1 câu hỏi ban giám khảo trả lời):
1. **Descriptive** — *What happened?* — thống kê tổng hợp chính xác, biểu đồ có nhãn rõ.
2. **Diagnostic** — *Why did it happen?* — giả thuyết nhân quả, so sánh phân khúc, xác định bất thường.
3. **Predictive** — *What is likely to happen?* — ngoại suy xu hướng, phân tích mùa vụ, chỉ số dẫn xuất.
4. **Prescriptive** — *What should we do?* — đề xuất hành động kinh doanh, đánh đổi định lượng. **← ăn điểm nhất.**

> Top team đạt **Prescriptive nhất quán** trên nhiều phân tích sẽ đạt điểm cao nhất.

### Part 3 — Sales Forecasting (20đ)

**Cấu trúc điểm** (nguồn: `Đề thi Vòng 1.pdf` tr.15-16):

| Thành phần | Mô tả | Điểm tối đa |
|---|---|---|
| Hiệu suất mô hình | MAE/RMSE/R² trên Kaggle leaderboard, xếp hạng tương đối | 12 |
| Báo cáo kỹ thuật | Pipeline (FE, temporal CV, leakage), SHAP/feature importance, tuân thủ ràng buộc | 8 |
| **Tổng** | | **20** |

**Bảng band điểm chi tiết**:

| Thành phần | Band | Tiêu chí |
|---|---|---|
| Hiệu suất (12đ) | **10–12** | Top leaderboard; MAE/RMSE thấp, R² cao |
| | **5–9** | Trung bình; mô hình hoạt động nhưng chưa tối ưu |
| | **3–4** | Hợp lệ nhưng performance thấp (mức điểm sàn) |
| Báo cáo kỹ thuật (8đ) | **7–8** | Pipeline rõ, temporal CV đúng, SHAP cụ thể, tuân thủ đầy đủ ràng buộc |
| | **4–6** | Pipeline đủ dùng, giải thích định tính, vài ràng buộc chưa xử lý tường minh |
| | **0–3** | Thiếu giải thích, không kiểm soát leakage, hoặc không tái lập được |

**Mục tiêu dự báo**:
- `Revenue` và `COGS` daily cho 2023-01-01 → 2024-07-01 (**548 ngày**) — submission format có cả 2 cột.
- Đề chính thức nhấn mạnh **Revenue** là target chính (PDF §2.3.2: *"Dự báo cột Revenue trong khoảng thời gian của sales_test.csv"*), nhưng `sample_submission.csv` yêu cầu cả `Revenue, COGS` → mô hình phải predict cả hai.
- Train trên `sales.csv`: 2012-07-04 → 2022-12-31 (**3,833 ngày**). Test file thực tế tên `sales_test.csv` (không công bố public).

**Công thức metric**:
```
MAE  = (1/n) × Σ|F_i - A_i|
RMSE = √[(1/n) × Σ(F_i - A_i)²]
R²   = 1 - Σ(A_i - F_i)² / Σ(A_i - Ā)²
```

**Điều kiện loại bài** (`Đề thi Vòng 1.pdf` tr.16): vi phạm 1 trong 3 → mất toàn bộ 20đ Part 3:
1. Dùng `Revenue`/`COGS` của test set làm feature.
2. Dùng dữ liệu ngoài 15 CSV.
3. Không nộp code hoặc kết quả không tái lập được.

**Lưu ý format báo cáo**: Phần 2 EDA + Phần 3 model report **gộp chung 1 PDF ≤4 trang** (NeurIPS template).

---

## §3 — Ràng buộc cứng (vi phạm = LOẠI)

1. **Không dùng dữ liệu ngoài** — tất cả feature phải derive từ 15 CSV gốc.
2. **Reproducibility** — code phải trên GitHub (public hoặc invite organizers), random seed set.
3. **Explainability** — báo cáo PHẢI giải thích main revenue drivers qua feature importance / SHAP / PDP bằng **ngôn ngữ business** (không chỉ "feature X has SHAP value 0.3").
4. **Không leakage** — không dùng Revenue/COGS của test set làm feature.
5. **Temporal CV** — KHÔNG được random split, phải rolling-origin / expanding window.
6. **Submission đúng thứ tự** — `submission.csv` có 3 cột `Date, Revenue, COGS` và thứ tự dòng khớp 100% với `sample_submission.csv`. Không reorder, không shuffle.
7. **Báo cáo PDF ≤4 trang** — template NeurIPS (lấy từ neurips.cc), chứa link GitHub trong báo cáo.
8. **README.md** trên GitHub phải có hướng dẫn reproduce đầy đủ.
9. **Ảnh thẻ sinh viên** — tất cả thành viên, bắt buộc khi nộp form.
10. **Confirm chung kết** — checkbox ≥1 thành viên tham dự 2026-05-23 tại VinUni HN, bắt buộc tick.

---

## §4 — Deadline & tài liệu gốc

- **Hôm nay (session đầu)**: 2026-04-18
- **Phiên re-audit PDF**: 2026-04-19 — còn **12 ngày** tới deadline (PDF được tổ chức cập nhật 2026-04-19)
- **🔴 DEADLINE NỘP VÒNG 1: 2026-05-01** — **cứng, không slack**
- **Chung kết**: 2026-05-23 tại VinUniversity, Hà Nội
- **File gốc cần tham khảo** (nằm trong thư mục dự án):
  - `Đề thi Vòng 1.pdf` — đề thi vòng 1 (tiếng Việt, bản cập nhật 2026-04-19)
  - `Rule_book.docx` — quy chế cuộc thi (tiếng Việt)
  - `dataset-datathon-2026-round-1/dataset_description.docx` — data dictionary

### Checklist nộp bài (PDF page 16)

Mỗi đội phải hoàn thành đủ 4 hạng mục sau — thiếu 1 → không hợp lệ:
1. **Submission Kaggle** — file `submission.csv` đúng format, đúng thứ tự dòng như `sample_submission.csv`; submit tại https://www.kaggle.com/competitions/datathon-2026-round-1
2. **Báo cáo PDF** — template NeurIPS 2025, ≤4 trang (không tính references/appendix), chứa link GitHub repo, gộp cả EDA (Part 2) + model report (Part 3)
3. **GitHub repository** — public hoặc cấp quyền cho BTC trước deadline; có `README.md` mô tả cấu trúc + hướng dẫn reproduce; chứa toàn bộ code + notebook + file submission
4. **Form nộp bài chính thức** — gồm: đáp án MCQ (10 câu) + upload PDF báo cáo + link GitHub + link Kaggle submission + **ảnh thẻ sinh viên của tất cả thành viên** + **tickbox cam kết ít nhất 1 thành viên dự chung kết 23/05/2026 tại VinUni HN**

---

## §5 — Dataset: 14 file CSV

Tất cả nằm trong `dataset-datathon-2026-round-1/`. **Không sửa data gốc**.

### Phân tầng 4 lớp dữ liệu (theo `Đề thi Vòng 1.pdf` §1.1)

Đề chính thức (PDF Table 1) tổ chức 14 file CSV thành 4 lớp logic — dùng làm khung tham chiếu khi viết EDA:

| Lớp | Mô tả | File |
|---|---|---|
| **Master** (4 file) | Dữ liệu tham chiếu, ít thay đổi | `products`, `customers`, `promotions`, `geography` |
| **Transaction** (6 file) | Giao dịch raw event-level | `orders`, `order_items`, `payments`, `shipments`, `returns`, `reviews` |
| **Analytical** (2 file) | Aggregate đã pre-compute (target) | `sales` (train), `sample_submission` (test format) |
| **Operational** (2 file) | Vận hành nội bộ | `inventory` (monthly snapshot), `web_traffic` (daily) |

> **Ghi chú**: `inventory.csv` đã có sẵn các cột enhanced (stockout_flag, overstock_flag, reorder_flag, days_of_supply, fill_rate, sell_through_rate) — không tồn tại file `inventory_enhanced.csv` riêng.

### Bảng tổng

| # | File | Rows | Size | Primary Key | Foreign Keys |
|---|---|---|---|---|---|
| 1 | `products.csv` | 2,413 | 191KB | product_id | — |
| 2 | `customers.csv` | 121,931 | 6.8MB | customer_id | zip → geography |
| 3 | `geography.csv` | 39,948 | 1.3MB | zip | — |
| 4 | `promotions.csv` | 50 | 4.3KB | promo_id | — |
| 5 | `orders.csv` | 646,946 | 44MB | order_id | customer_id, zip |
| 6 | `order_items.csv` | 714,670 | 23MB | (order_id, product_id) | order_id, product_id, promo_id, promo_id_2 |
| 7 | `payments.csv` | 646,946 | 18MB | order_id | order_id (1:1) |
| 8 | `shipments.csv` | 566,068 | 19MB | order_id | order_id (1:0 hoặc 1) |
| 9 | `returns.csv` | 39,939 | 2.2MB | return_id | order_id, product_id |
| 10 | `reviews.csv` | 113,551 | 6.5MB | review_id | order_id, product_id, customer_id |
| 11 | `sales.csv` | 3,833 | 127KB | Date | **← TARGET (train)** |
| 12 | `sample_submission.csv` | 548 | 18KB | Date | **← TARGET format (test)** |
| 13 | `inventory.csv` | 60,247 | 5.4MB | (snapshot_date, product_id) | product_id |
| 14 | `web_traffic.csv` | 3,653 | 204KB | date | — |

### Chi tiết schema từng bảng

#### products.csv
| col | type | ghi chú |
|---|---|---|
| product_id | int | PK |
| product_name | str | vd "SaigonFlex UC-01" |
| category | str | {Streetwear, Casual, Outdoor, GenZ} (4) |
| segment | str | {Everyday, Performance, Balanced, Standard, All-weather, Premium, Trendy, Activewear} (8) |
| size | str | {S, M, L, XL} |
| color | str | 10 màu |
| price | float | giá list |
| cogs | float | giá vốn (luôn < price) |

**Business rule**: Gross Margin % = (price - cogs) / price

#### customers.csv
| col | type | ghi chú |
|---|---|---|
| customer_id | int | PK |
| zip | int | FK → geography |
| city | str | |
| signup_date | date | |
| gender | str | {Female, Male, Non-binary} — **nullable** |
| age_group | str | {18-24, 25-34, 35-44, 45-54, 55+} — **nullable** |
| acquisition_channel | str | {social_media, email_campaign, organic_search, referral, direct, paid_search} — **nullable** |

#### geography.csv
| col | type | ghi chú |
|---|---|---|
| zip | int | PK |
| city | str | 42 thành phố |
| region | str | {East, Central, West} (3) |
| district | str | vd "District #13" |

#### promotions.csv (chỉ 50 campaign trong 10.5 năm — PROMO RẤT THƯA)
| col | type | ghi chú |
|---|---|---|
| promo_id | str | PK, vd "PROMO-0001" |
| promo_name | str | vd "Spring Sale 2013" |
| promo_type | str | {percentage, fixed} |
| discount_value | float | % hoặc số tiền cố định |
| start_date | date | |
| end_date | date | |
| applicable_category | str | NULL = áp dụng tất cả |
| promo_channel | str | {email, online, all_channels, in_store, social_media} |
| stackable_flag | int | 0/1 — cho phép cộng dồn |
| min_order_value | float | nullable |

**Công thức discount**:
- percentage: `discount_amount = quantity × unit_price × (discount_value / 100)`
- fixed: `discount_amount = quantity × discount_value`

#### orders.csv
| col | type | ghi chú |
|---|---|---|
| order_id | int | PK |
| order_date | date | |
| customer_id | int | FK |
| zip | int | FK (ZIP giao hàng) |
| order_status | str | {delivered, returned, shipped, cancelled, paid, created} (6) |
| payment_method | str | {credit_card, cod, paypal, apple_pay, bank_transfer} (5) |
| device_type | str | {desktop, mobile, tablet} |
| order_source | str | {paid_search, direct, referral, email_campaign, organic_search, social_media} |

#### order_items.csv
| col | type | ghi chú |
|---|---|---|
| order_id | int | FK |
| product_id | int | FK |
| quantity | int | |
| unit_price | float | **ĐÃ giảm giá**, không phải giá list |
| discount_amount | float | tổng discount cho line item |
| promo_id | str | nullable |
| promo_id_2 | str | nullable (stackable promo) |

**⚠️ QUAN TRỌNG**: `unit_price` trong `order_items` là **giá sau giảm**, không phải giá list. Muốn ra giá gốc: `(quantity × unit_price + discount_amount) / quantity`.

#### payments.csv
| col | type | ghi chú |
|---|---|---|
| order_id | int | FK (1:1 với orders) |
| payment_method | str | |
| payment_value | float | tổng thanh toán |
| installments | int | số kỳ trả góp |

#### shipments.csv (chỉ tồn tại cho orders có status shipped/delivered/returned)
| col | type | ghi chú |
|---|---|---|
| order_id | int | FK (1:0 hoặc 1) |
| ship_date | date | |
| delivery_date | date | |
| shipping_fee | float | 0 = free shipping |

**⚠️ Không có shipments cho orders status `cancelled`, `paid`, `created`.**

#### returns.csv
| col | type | ghi chú |
|---|---|---|
| return_id | str | PK, vd "RET-000001" |
| order_id | int | FK |
| product_id | int | FK |
| return_date | date | |
| return_reason | str | {late_delivery, wrong_size, defective, changed_mind, not_as_described} (5) |
| return_quantity | int | |
| refund_amount | float | |

#### reviews.csv (chỉ ~20% delivered orders có review)
| col | type | ghi chú |
|---|---|---|
| review_id | str | PK, vd "REV-0000001" |
| order_id | int | FK |
| product_id | int | FK |
| customer_id | int | FK |
| review_date | date | |
| rating | int | 1-5 sao |
| review_title | str | |

**Phân bố rating**: {1: 5772, 2: 9095, 3: 17016, 4: 36412, 5: 45256} — lệch phải (satisfaction bias).

#### inventory.csv (snapshot end-of-month)
| col | type | ghi chú |
|---|---|---|
| snapshot_date | date | cuối tháng |
| product_id | int | FK |
| stock_on_hand | int | tồn cuối tháng |
| units_received | int | nhập trong tháng |
| units_sold | int | bán trong tháng |
| stockout_days | int | số ngày hết hàng |
| days_of_supply | float | tồn còn đủ bao nhiêu ngày bán |
| fill_rate | float | tỷ lệ fulfillment |
| stockout_flag | int | 0/1 |
| overstock_flag | int | 0/1 |
| reorder_flag | int | 0/1 |
| sell_through_rate | float | |
| product_name, category, segment | | denormalized từ products |
| year, month | int | derived |

**Time range**: 2012-07-31 → 2022-12-31 (monthly snapshot)

#### web_traffic.csv (2013-01-01 → 2022-12-31, 3,653 rows)
| col | type | ghi chú |
|---|---|---|
| date | date | PK |
| sessions | int | |
| unique_visitors | int | |
| page_views | int | |
| bounce_rate | float | 0-1 |
| avg_session_duration_sec | float | |
| traffic_source | str | 6 channels |

**⚠️ KHÔNG có cột `conversion_rate`** — phải tự tính = `orders_per_date / sessions` nếu cần.
**⚠️ Bắt đầu 2013-01-01** (trễ 6 tháng so với `sales.csv` 2012-07-04) → 6 tháng đầu sales không có traffic; inner join hoặc chấp nhận NaN.
**⚠️ Không có data traffic cho test period 2023-01 → 2024-07.** Cần decide cách handle (xem §12 câu 9).

#### sales.csv — TARGET TRAIN
| col | type | ghi chú |
|---|---|---|
| Date | date | 2012-07-04 → 2022-12-31 |
| Revenue | float | net daily revenue |
| COGS | float | daily cost of goods sold |

**Stats**: Revenue min=279,814 / mean=4,286,584 / max=20,905,271. COGS min=236,576 / mean=3,695,134 / max=16,535,858. Zero missing values.

#### sample_submission.csv — TARGET TEST FORMAT
| col | type | ghi chú |
|---|---|---|
| Date | str YYYY-MM-DD | 2023-01-01 → 2024-07-01 (548 dòng) |
| Revenue | float | dummy, cần predict |
| COGS | float | dummy, cần predict |

### Quan hệ giữa các bảng

```
customers ←(zip)← geography
    ↓ (customer_id)
  orders ←(order_id)→ payments (1:1)
    ↓       ←(order_id)→ shipments (1:0/1, chỉ shipped/delivered/returned)
    ↓       ←(order_id)→ returns (1:0/many)
    ↓       ←(order_id)→ reviews (1:0/many)
    ↓ (order_id)
  order_items ←(product_id)→ products
                ←(promo_id, promo_id_2)→ promotions

products ←(product_id)→ inventory (1:many theo snapshot_date)
sales (standalone — aggregate daily)
web_traffic (standalone — daily)
```

---

## §6 — Công thức quan trọng

- **Daily Revenue** = Σ (qty × unit_price của order_items trong ngày) net của return
- **Daily COGS** = Σ (product.cogs × qty của order_items trong ngày)
- **Gross Margin %** = (price - cogs) / price
- **Order net value** = payment_value (tổng đã trả)
- **Original price (trước giảm)** = (quantity × unit_price + discount_amount) / quantity
- **Return rate** = returned_orders / total_orders × 100%
- **Conversion rate** (web) = orders / sessions
- **MAPE** = (1/n) × Σ |F-A| / A × 100% — dùng nội bộ để sanity check (không phải metric leaderboard)

---

## §7 — Baseline notebook đã có

File: `dataset-datathon-2026-round-1/baseline.ipynb`

**Chiến lược (seasonal × growth)**:
1. Tính geometric mean YoY growth rate từ annual totals 2013-2022.
2. Build seasonal profile: mean normalized Revenue/COGS theo `(month, day)` xuyên suốt các năm.
3. `prediction = base_level × growth^years_ahead × seasonal_factor` với `base_level = 2022_annual_mean / 365`.
4. Validate bằng MAPE trên 2021-2022 (tail training).

**Đánh giá**:
- Đơn giản, interpretable, dùng làm **benchmark tối thiểu**.
- Không capture: promo, web traffic, customer behavior, inventory, events.
- Model nâng cao phải **beat baseline MAE ≥ 20%**.

---

## §8 — Cấu trúc thư mục dự án

```
/Users/dominhhien/Documents/AI/Datathon/
├── CLAUDE.md                      # ← file này (brain)
├── README.md                      # hướng dẫn reproduce cho GitHub (sẽ tạo Phase 7)
├── Đề thi Vòng 1.pdf              # gốc — không sửa
├── Rule_book.docx                 # gốc — không sửa
├── dataset-datathon-2026-round-1/ # gốc — không sửa/không ghi đè
│   ├── products.csv, customers.csv, ...
│   ├── baseline.ipynb             # baseline đã có sẵn
│   └── dataset_description.docx
├── notebooks/                     # 7 notebook theo plan (file 03_* có thể tách thành nhiều phần khi thêm ý 1-10)
│   ├── 01_data_audit.ipynb
│   ├── 02_mcq.ipynb
│   ├── 03_eda_idea11_12_margin_shipping.ipynb   # ý 11 (margin × segment) + ý 12 (shipping × return)
│   ├── 04_eda_predictive.ipynb
│   ├── 05_feature_engineering.ipynb
│   ├── 06_model_baseline.ipynb
│   └── 07_model_advanced.ipynb
├── src/                           # module tái dùng
│   ├── loaders.py                 # load_all() → dict DataFrames
│   ├── features.py                # temporal/lag/rolling feature builders
│   ├── metrics.py                 # mae, rmse, r2, evaluate()
│   └── cv.py                      # TemporalSplit generator
├── outputs/
│   ├── figures/                   # PNG/PDF cho báo cáo
│   ├── models/                    # .pkl model artifacts
│   ├── data_quality_report.md
│   └── submission.csv             # FILE NỘP KAGGLE
├── report/
│   ├── main.tex                   # NeurIPS LaTeX
│   └── main.pdf                   # ≤4 trang
├── requirements.txt
└── .gitignore                     # .mov, models/*.pkl, __pycache__, .ipynb_checkpoints, .DS_Store
```

**Lưu ý**: screen recording `.mov` 5GB KHÔNG push lên Git. Thêm vào `.gitignore`.

---

## §9 — Conventions bắt buộc cho mọi Claude session

### Code
- **Python version**: 3.10+ (đồng bộ với Kaggle).
- **Random seed**: `SEED = 42`, dùng cho `np.random.seed(SEED)`, `random.seed(SEED)`, mọi model `random_state=SEED`.
- **Date parsing**: `pd.read_csv(..., parse_dates=['Date'])` cho sales/sample_submission; `parse_dates=['order_date']` cho orders; tương tự cho các cột date khác.
- **Đọc CSV**: dùng đường dẫn tuyệt đối `/Users/dominhhien/Documents/AI/Datathon/dataset-datathon-2026-round-1/` hoặc relative `../dataset-datathon-2026-round-1/` từ notebook.
- **KHÔNG ghi đè** file trong `dataset-datathon-2026-round-1/` — đó là data gốc read-only.
- **Memory**: orders.csv 44MB + order_items.csv 23MB là lớn; nếu RAM hạn chế, cân nhắc `dtype` khai báo hoặc `chunksize`.

### Ngôn ngữ
- **Variable names, function names, comments trong code**: tiếng Anh.
- **Markdown cells trong notebook, báo cáo, docstring dài**: tiếng Việt (vì team Việt).
- **CLAUDE.md**: tiếng Việt (trừ tên cột/bảng/thuật ngữ kỹ thuật).

### Joins chuẩn
- `orders × order_items × payments`: qua `order_id`.
- `order_items × products`: qua `product_id`.
- `orders × customers × geography`: qua `customer_id`, `zip`.
- `order_items × promotions`: qua `promo_id` hoặc `promo_id_2` (stackable).

### Anti-leakage checklist
- [ ] Feature không dùng thông tin từ test period (2023-01-01+).
- [ ] Lag features: `t-7`, `t-14`, `t-28`, `t-365` — với test xa, phải đảm bảo lag ≥ 548 hoặc dùng predicted lag (recursive forecast).
- [ ] Temporal CV chỉ train past, validate future.
- [ ] KHÔNG dùng `Revenue` hoặc `COGS` của 2023+ làm input (test set).
- [ ] Rolling features (mean, std) chỉ tính trên historical window không bao gồm target day.

---

## §10 — Trạng thái tiến độ (update mỗi phiên)

| Phase | Mô tả | Trạng thái | Ngày hoàn thành |
|---|---|---|---|
| 1 | Tạo CLAUDE.md | ✅ DONE | 2026-04-18 |
| 2 | Audit `Đề thi Vòng 1.pdf` (bản đầu) — extract 10 MCQ + constraint + Kaggle link + template NeurIPS | ✅ DONE | 2026-04-18 |
| 2b | Re-audit PDF bản cập nhật + sync CLAUDE.md (14 file CSV, thứ tự bảng tổng, checklist nộp bài) | ✅ DONE | 2026-04-19 |
| 3 | Data audit notebook (`01_data_audit.ipynb`) | ⏳ TODO | — |
| 4 | MCQ notebook (`02_mcq.ipynb`) | ✅ DONE | 2026-04-23 |
| 5a | EDA descriptive + diagnostic — ý 11+12 (`03_eda_idea11_12_margin_shipping.ipynb`) | 🟡 IN PROGRESS (2/12 ý) | — |
| 5b | EDA predictive + prescriptive (`04_eda_predictive.ipynb`) | ⏳ TODO | — |
| 6a | Feature engineering (`05_feature_engineering.ipynb`) | ⏳ TODO | — |
| 6b | Model baseline reproduce (`06_model_baseline.ipynb`) | ⏳ TODO | — |
| 6c | Model advanced LightGBM + SHAP (`07_model_advanced.ipynb`) | ⏳ TODO | — |
| 7a | Báo cáo NeurIPS PDF (≤4 trang) | ⏳ TODO | — |
| 7b | GitHub repo + README + seed | ⏳ TODO | — |
| 7c | Nộp submission form + Kaggle + ảnh thẻ SV | ⏳ TODO | — |

**Quy tắc bắt đầu phiên mới**:
1. Đọc §10 → biết đã xong Phase nào.
2. Đọc §12 → kiểm tra có câu hỏi chưa resolved.
3. Hỏi user: "Hôm nay mình làm Phase nào?"
4. Làm đúng phạm vi, update §10 sau khi xong.

---

## §11 — Team (4 người) — chốt 2026-04-19, re-assign Phúc↔Kiên 2026-04-21

| Thành viên | Role | Trách nhiệm chính | Notebook |
|---|---|---|---|
| **Hiển** | 🧑‍✈️ Đội trưởng | Coordinator: điều phối + MCQ + LaTeX báo cáo + GitHub + submission form | 02_mcq, report/, README |
| **Đồng** | Lead Analyst | EDA tầng 1-2 (Descriptive + Diagnostic), data audit, storytelling nền tảng | 01_data_audit, 03_eda_idea11_12_margin_shipping (+ các 03_* phần tiếp theo) |
| **Kiên** | 📊 Insights Lead | EDA tầng 3-4 (Predictive + Prescriptive), viết insight + narrative báo cáo | 04_eda_predictive |
| **Phúc** | 🛠 ML Engineer | Feature engineering, baseline, LightGBM, SHAP, Kaggle submissions | 05_feature_engineering, 06_model_baseline, 07_model_advanced |

**Luật review chéo** (bắt buộc):
- Mỗi notebook có cell đầu tiên set `SEED=42` + in phiên bản pandas/numpy/lightgbm để debug cross-machine.
- Hiển review MCQ + Report; Đồng review EDA Predictive của **Kiên**; **Kiên** review Prescriptive-narrative trong model report của **Phúc**; **Phúc** audit leakage trên notebook 03/04 trước khi đưa feature vào model.
- Trước mỗi deadline nội bộ (§ team brief), 1 thành viên chạy end-to-end trên máy thứ 2 để xác nhận reproducibility.

→ Chi tiết cross-reference role ↔ section xem file `Vòng 1 — Phân tích đề & Brainstorm (team brief).docx` §6.

---

## §12 — Nhắc nhở & câu hỏi còn mở

> **Quy tắc**: Mỗi phiên Claude mới, đọc §12 trước. Câu nào còn `[CHƯA CÓ]` hoặc `[CHƯA KHẲNG ĐỊNH]` → hỏi user ngay đầu phiên. Khi có answer → edit §12 xoá entry đó + cập nhật phần tương ứng của CLAUDE.md.

### ✅ Đã resolve (lưu lại để tham khảo)

- ~~10 câu MCQ nguyên văn~~ → đã lưu đầy đủ ở §2 Part 1.
- ~~Team roster + phân công role~~ → Hiển (Đội trưởng), Đồng (Lead Analyst), **Kiên (Insights Lead — EDA P+Pr)**, **Phúc (ML Engineer — Model)** — chi tiết §11. Chốt 2026-04-19, swap Phúc↔Kiên ngày **2026-04-21**. (MSSV/email/ảnh thẻ SV — user yêu cầu **bỏ qua**, không nhắc nữa.)
- ~~Kaggle slug~~ → `datathon-2026-round-1`. URL: https://www.kaggle.com/competitions/datathon-2026-round-1
- ~~LaTeX template~~ → NeurIPS 2025: https://neurips.cc/Conferences/2025/CallForPapers

### Còn mở — cấu hình hạ tầng

1. **[CHƯA CÓ] GitHub repo**
   - Tên repo dự kiến? Ai làm owner? Public từ đầu hay tạm private?
   - Dùng để: chứa code + README + submission. Cần link trong báo cáo PDF.

2. **[CHƯA CÓ] Kaggle team setup**
   - Team đã register chưa? Dùng 1 account nộp hay merge team trên Kaggle?
   - Hiển check: `https://www.kaggle.com/competitions/datathon-2026-round-1` → Join + Team.

3. **[CHƯA CÓ] Môi trường compute**
   - Laptop cá nhân (RAM đủ cho 714K rows không)? Hay Kaggle/Colab?
   - Dùng để: decide cách load data (full vs chunksize) trong notebook.

### Còn mở — quyết định kỹ thuật (resolve khi bắt đầu Phase 6)

4. **[CHƯA KHẲNG ĐỊNH] Xử lý `web_traffic` trong test period**
   - `web_traffic.csv` chỉ có đến 2022-12-31, test 2023-01 → 2024-07 không có.
   - Options:
     - (a) Tự forecast traffic riêng (mô hình phụ).
     - (b) Dùng rolling mean 2022 làm proxy.
     - (c) Bỏ traffic feature, dùng feature khác.

5. **[CHƯA KHẲNG ĐỊNH] Prophet có được coi là "external data" không?**
   - Prophet tự load Vietnam holiday calendar → có thể bị coi là external.
   - Options:
     - (a) Tắt holiday của Prophet, chỉ dùng seasonality.
     - (b) Không dùng Prophet, thay bằng LightGBM + self-built calendar VN.

### Lưu ý phát hiện khi đọc đề (không phải câu hỏi — chỉ để nhớ)

- **PDF dùng 2 tên song song cho cùng 1 file train**: Table 1 (page 3) gọi `sales.csv` (khớp disk), còn các Split table (§1.1 page 3, §2.3.3 page 11) và Q7 (page 9) gọi `sales_train.csv`. **File thật trên disk: `sales.csv`** — không cần rename.
- **PDF §1.1 ghi "15 file CSV" ở phần intro** nhưng **Table 1 chỉ liệt kê 14 file**. Disk thực tế: 14 file. Coi đây là nhất quán nội dung (14 file) và chấp nhận số "15" trong intro là lỗi đánh máy của PDF.
- **Baseline notebook** dùng `DATA_DIR = 'dataset/'` — đường dẫn này không khớp folder `dataset-datathon-2026-round-1/`. Khi chạy lại phải sửa hoặc symlink.
- **Điều kiện loại Phần 3**: (1) dùng Revenue/COGS test làm feature, (2) dùng data ngoài, (3) không nộp code hoặc không reproduce được → **mất toàn bộ 20đ Part 3**.

---

## §13 — Cheatsheet lệnh thường dùng

### Khám phá nhanh CSV
```python
import pandas as pd
df = pd.read_csv('dataset-datathon-2026-round-1/sales.csv', parse_dates=['Date'])
df.info(); df.describe(); df.head()
```

### Load toàn bộ (khi có `src/loaders.py`)
```python
from src.loaders import load_all
data = load_all()   # dict: {'products': df, 'customers': df, ...}
```

### Temporal CV
```python
from sklearn.model_selection import TimeSeriesSplit
tscv = TimeSeriesSplit(n_splits=5)
for train_idx, val_idx in tscv.split(X):
    ...
```

### SHAP cho LightGBM
```python
import shap
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_sample)
shap.summary_plot(shap_values, X_sample, feature_names=feature_names)
```

### Export submission đúng thứ tự
```python
sample = pd.read_csv('dataset-datathon-2026-round-1/sample_submission.csv', parse_dates=['Date'])
submission = sample[['Date']].copy()
submission['Revenue'] = model_rev.predict(X_test)
submission['COGS']    = model_cogs.predict(X_test)
submission['Date']    = submission['Date'].dt.strftime('%Y-%m-%d')
submission.to_csv('outputs/submission.csv', index=False)
assert len(submission) == 548
```
