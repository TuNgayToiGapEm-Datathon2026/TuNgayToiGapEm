# Thẻ 1

**DATATHON 2026 — VÒNG 1**

*The Gridbreakers · Breaking Business Boundaries*

**PHÂN TÍCH ĐỀ BÀI & BRAINSTORM CHIẾN LƯỢC — v2 (chi tiết chuyên sâu)**

*Tài liệu kickoff team — sync với PDF bản 2026-04-19*

| Mục | Thông tin |
| :---- | :---- |
| **Đội** | The Gridbreakers — 4 thành viên: Hiển (Đội trưởng) · Đồng (Lead Analyst) · Kiên (Insights Lead) · Phúc (ML Engineer).  |
| **Ngày phát hành brief (v1)** | 2026-04-18 |
| **Ngày cập nhật brief (v2)** | 2026-04-19 (sync theo PDF updated cùng ngày) |
| **Deadline nộp Vòng 1** | 2026-05-01 — cứng, còn 12 ngày tính từ 04-19 |
| **Vòng Chung kết** | 2026-05-23 tại VinUniversity, Hà Nội (bắt buộc ≥1 thành viên dự) |
| **Kaggle competition** | https://www.kaggle.com/competitions/datathon-2026-round-1 |
| **LaTeX template** | NeurIPS 2025 — https://neurips.cc/Conferences/2025/CallForPapers |
| **Vai trò giả định** | Data Scientist tại công ty thời trang TMĐT Việt Nam |
| **Dataset** | 14 file CSV (\~130MB), 10.5 năm dữ liệu (2012-07-04 → 2022-12-31) |
| **File kỷ luật nội bộ** | CLAUDE.md (§1–§13) — brain file tổng, đọc trước mọi phiên làm việc |

# **1\. Tóm tắt nhanh (TL;DR)**

Datathon 2026 Vòng 1 yêu cầu chúng ta đóng vai Data Scientist của 1 công ty thời trang TMĐT VN, khai thác 14 file CSV (10.5 năm dữ liệu) để biến dữ liệu thành giải pháp kinh doanh. Bài thi 3 phần với tổng 100 điểm; trọng số áp đảo nằm ở Phần 2 (EDA \= 60đ). 3 mục tiêu nghiệp vụ xuyên suốt: (1) tối ưu tồn kho, (2) lập kế hoạch promo, (3) quản lý logistics theo vùng.

| Phần | Nội dung | Điểm | Tỷ trọng | Ưu tiên đầu tư |
| :---- | :---- | :---- | :---- | :---- |
| **1** | MCQ — 10 câu × 2đ | 20 | 20% | Trung bình (1 ngày, code 1 notebook) |
| **2** | EDA & Data Visualization | 60 | 60% | ★★★ CAO NHẤT (5–6 ngày) |
| **3** | Sales Forecasting (Kaggle) | 20 | 20% | ★★ Cao (3–4 ngày) |
| **—** | Tổng | 100 | 100% | — |

| Insight chiến lược: Phần 2 EDA đáng giá gấp 3 lần Phần 3 Forecasting. Kaggle ranking chỉ chiếm 12/100 điểm tổng — không cần 'all-in' vào model. Đầu tư mạnh nhất vào EDA storytelling \+ 4 tầng phân tích (đặc biệt Prescriptive). Phần 3 cần beat baseline (≥20% MAE) và viết explainability tốt để lấy đủ 8đ báo cáo kỹ thuật. |
| :---- |

# **2\. Phân tích đề bài**

## **2.1. Bối cảnh kinh doanh**

PDF §2.3.1: 'Doanh nghiệp cần dự báo nhu cầu (demand) chính xác ở mức chi tiết để tối ưu hoá phân bổ tồn kho, lập kế hoạch khuyến mãi và quản lý logistics trên toàn quốc.' Dù target model là daily Revenue/COGS, framing 'demand' mở rộng hơn — nhắc chúng ta rằng báo cáo Prescriptive nên nói về demand, không chỉ tiền.

| Mục tiêu nghiệp vụ | KPI cải thiện | Dataset liên quan |
| :---- | :---- | :---- |
| **1\. Tối ưu phân bổ tồn kho** | Giảm stockout\_days 20–30% cho top SKU; tăng fill\_rate; giảm overstock\_flag | inventory, order\_items, products, sales |
| **2\. Kế hoạch khuyến mãi** | Tăng incremental revenue / campaign; giảm cannibalization với khách cũ | promotions, order\_items, orders, customers, sales |
| **3\. Logistics toàn quốc** | Giảm lead-time (delivery\_date − ship\_date); phân bổ inventory theo region rising | orders, shipments, geography, inventory |

*→ Mọi insight EDA và feature model phải kết nối ngược về 1 trong 3 mục tiêu này khi viết phần Prescriptive. Đây là tiêu chí ban giám khảo đánh giá 'business value' (15đ trong Phần 2).*

## **2.2. Phần 1 — MCQ (20 điểm)**

* 10 câu × 2đ \= 20đ. KHÔNG trừ điểm câu sai → luôn đoán cả khi không chắc.  
* Mỗi câu chỉ chọn 1 đáp án (radio).  
* Tất cả câu hỏi đều tính trực tiếp từ CSV → phải code thật để verify, không đoán bằng trực giác.

**Bảng 10 câu — file nguồn, phương pháp tính, và hint verify:**

| Q | Nội dung | File & join | Phương pháp tính (pseudocode) |
| :---- | :---- | :---- | :---- |
| **1** | Trung vị số ngày giữa 2 lần mua liên tiếp (inter-order gap) ở khách hàng có \>1 đơn | orders.csv | df.sort(\[customer\_id, order\_date\]); gap \= order\_date.diff() groupby customer\_id; filter \>=1 order gap; median(gap).days |
| **2** | Segment có gross margin trung bình cao nhất | products.csv | margin \= (price−cogs)/price; groupby segment; mean(margin).idxmax() |
| **3** | Lý do trả hàng phổ biến nhất trong category Streetwear | returns ⨝ products trên product\_id | filter products.category=='Streetwear'; value\_counts(return\_reason).idxmax() |
| **4** | traffic\_source có bounce\_rate trung bình thấp nhất | web\_traffic.csv | groupby traffic\_source; mean(bounce\_rate).idxmin() |
| **5** | % dòng order\_items có promo\_id không null | order\_items.csv | (promo\_id.notna().sum() / len(df)) \* 100 |
| **6** | age\_group có trung bình số đơn / khách cao nhất | orders \+ customers trên customer\_id | orders.groupby(customer\_id).size → map age\_group → groupby age\_group mean(); dropna age\_group trước |
| **7** | Region tạo tổng doanh thu cao nhất trong sales\_train | order\_items ⨝ orders ⨝ geography (orders.zip → geography.zip) | revenue\_per\_line \= quantity × unit\_price; groupby region sum(); idxmax(). ⚠ sales.csv không có region — phải dùng order\_items. |
| **8** | Payment method phổ biến nhất ở đơn cancelled | orders.csv | filter order\_status=='cancelled'; value\_counts(payment\_method).idxmax() |
| **9** | Size có return rate cao nhất (\#returns / \#order\_items lines) | returns ⨝ products; order\_items ⨝ products | num \= returns.merge(products).groupby(size).size; den \= order\_items.merge(products).groupby(size).size; (num/den).idxmax() |
| **10** | Installment plan có giá trị thanh toán trung bình cao nhất | payments.csv | groupby installments; mean(payment\_value).idxmax() |

| Chiến thuật MCQ: 1 người (đề xuất Hiển) viết 02\_mcq.ipynb chạy cả 10 câu trong vài giờ. Save kết quả ra outputs/mcq\_answers.json \+ print full breakdown (mean/count per group) để team verify chéo. KHÔNG submit trước khi có 2 người đọc lại. |
| :---- |

## **2.3. Phần 2 — EDA & Data Visualization (60 điểm)**

Đây là phần ĂN ĐIỂM NHẤT. Không có đáp án đúng duy nhất — BGK chấm khả năng kể chuyện bằng dữ liệu và chiều sâu phân tích. Bài nộp gồm 2 phần: (1) Visualizations có title/axis/legend rõ; (2) Analysis đi kèm mỗi chart: key findings \+ business implications \+ actionable recommendations.

**Rubric 4 tiêu chí (PDF page 15):**

| Tiêu chí | Mô tả | Điểm tối đa |
| :---- | :---- | :---- |
| **Chất lượng trực quan hoá** | Chart có title/axis/legend đủ, chọn loại phù hợp, thẩm mỹ | 15 |
| **Chiều sâu phân tích** | Phủ đủ 4 tầng Descriptive → Diagnostic → Predictive → Prescriptive | 25 |
| **Insight kinh doanh** | Đề xuất cụ thể, định lượng, áp dụng được ngay | 15 |
| **Tính sáng tạo & kể chuyện** | Góc nhìn độc đáo, narrative xuyên suốt, kết nối đa bảng | 5 |
| **—** | Tổng | 60 |

**Chi tiết band điểm (để tự chấm):**

| Tiêu chí | Band cao | Band trung | Band thấp |
| :---- | :---- | :---- | :---- |
| **Trực quan (15đ)** | 13–15: tất cả chart đạt chuẩn, chọn loại tối ưu | 8–12: phần lớn đạt, thiếu nhãn | 0–7: thiếu thông tin, khó đọc |
| **Chiều sâu (25đ)** | 21–25: đạt cả 4 tầng nhất quán | 14–20: 3 tầng, Prescriptive hời hợt | 0–13: chỉ mô tả bề mặt |
| **Insight (15đ)** | 13–15: đề xuất cụ thể, định lượng, áp dụng ngay | 8–12: đề xuất chung chung | 0–7: thiếu kết nối business |
| **Sáng tạo (5đ)** | 4–5: góc độc đáo, narrative thuyết phục | 2–3: có sáng tạo chưa nhất quán | 0–1: dự đoán được |

**4 tầng phân tích — câu hỏi BGK & chiều sâu kỳ vọng:**

| Tầng | Câu hỏi BGK | Ví dụ phân tích chiều sâu |
| :---- | :---- | :---- |
| **Descriptive** | What happened? | YoY revenue 2013-2022 \+ monthly seasonality; top 10 SKU; region split; customer pyramid theo age\_group. |
| **Diagnostic** | Why did it happen? | COVID 2020-2021: revenue dip vs same-month 2019 (∆%), channel mix shift (mobile spike?); test hypothesis với z-test. |
| **Predictive** | What is likely? | STL decompose sales → trend+season+residual; extrapolate; tính dự báo demand SKU-level cho Q1-2023 dựa rolling 365 \+ cohort retention. |
| **Prescriptive** | What should we do? | Shift 20% social → paid\_search (ΔROAS định lượng); raise price Premium \+5% (margin cao, elasticity \< 0.5); pre-stock Tết \+14 ngày. |

| Quy tắc vàng: Top team đạt PRESCRIPTIVE NHẤT QUÁN trên nhiều phân tích sẽ được điểm cao nhất. Mỗi visualization phải có ít nhất 1 dòng 'So what?' \+ 1 dòng 'Action gì?' \+ 1 con số định lượng impact (VD: tiết kiệm X triệu/năm, tăng Y% conversion). |
| :---- |

## **2.4. Phần 3 — Sales Forecasting (20 điểm)**

* Target — Predict Revenue (và COGS) hàng ngày cho 548 ngày 2023-01-01 → 2024-07-01.  
* Train — sales.csv (PDF gọi sales\_train.csv) 2012-07-04 → 2022-12-31, 3,833 ngày.  
* Submission — submission.csv 3 cột (Date, Revenue, COGS), thứ tự dòng KHỚP 100% sample\_submission.csv. Không reorder.  
* Metrics — MAE, RMSE (càng thấp càng tốt), R² (càng cao càng tốt, lý tưởng \~1).

**Quy đổi điểm Phần 3:**

| Thành phần | Band | Mô tả |
| :---- | :---- | :---- |
| **Hiệu suất mô hình (12đ)** | 10–12 | Top leaderboard; MAE/RMSE thấp, R² cao |
|  | 5–9 | Trung bình; model chạy nhưng chưa tối ưu |
|  | 3–4 | Hợp lệ, performance thấp (mức sàn) |
| **Báo cáo kỹ thuật (8đ)** | 7–8 | Pipeline rõ, temporal CV đúng, SHAP cụ thể, tuân thủ ràng buộc |
|  | 4–6 | Pipeline đủ dùng, giải thích định tính, ràng buộc chưa tường minh |
|  | 0–3 | Thiếu giải thích, leakage, không tái lập |

| Điều kiện LOẠI Phần 3 (mất nguyên 20đ): (1) Dùng Revenue/COGS test làm feature; (2) Dùng dữ liệu ngoài 14 CSV; (3) Không nộp code hoặc kết quả không tái lập. Mitigate ngay từ đầu: anti-leakage checklist \+ seed=42 \+ submission chạy end-to-end trên máy thứ 2 trước khi nộp. |
| :---- |

# **3\. Dataset tour — 14 CSV chia 4 lớp**

PDF §1.1 tổ chức 14 file thành 4 lớp logic. PDF intro ghi '15 file CSV' nhưng Table 1 chỉ liệt kê 14 — trên disk thực tế là 14 (không có inventory\_enhanced.csv; inventory.csv hiện tại đã có đủ cột enhanced).

| Lớp | Vai trò | File | Đặc điểm khi dùng |
| :---- | :---- | :---- | :---- |
| **Master** | Tham chiếu, ít thay đổi | products, customers, promotions, geography | Slowly-changing dimensions; dùng để dim, filter, groupby. |
| **Transaction** | Sự kiện thô event-level | orders, order\_items, payments, shipments, returns, reviews | Khối lượng lớn (\~647K orders, 715K items). Gốc của mọi metric daily. |
| **Analytical** | Aggregate pre-compute | sales (train), sample\_submission (test format) | Daily Revenue \+ COGS — chính là TARGET của Phần 3\. |
| **Operational** | Vận hành nội bộ | inventory (monthly snapshot), web\_traffic (daily) | Inventory end-of-month; web\_traffic không có cho test period. |

**Quan hệ giữa các bảng (cardinality):**

| Quan hệ | Cardinality |
| :---- | :---- |
| **orders ↔ payments** | 1 : 1 |
| **orders ↔ shipments** | 1 : 0 hoặc 1 (chỉ status shipped/delivered/returned) |
| **orders ↔ returns** | 1 : 0 hoặc nhiều |
| **orders ↔ reviews** | 1 : 0 hoặc nhiều (\~20% delivered orders có review) |
| **order\_items ↔ promotions** | nhiều : 0 hoặc 1 (qua promo\_id, promo\_id\_2) |
| **products ↔ inventory** | 1 : nhiều (1 dòng/sản phẩm/tháng) |

## **3.1. Quick-reference — cột đắt giá mỗi CSV**

Bảng dưới để join 2+ bảng mà không phải mở dataset\_description.docx. PK \= primary key, FK \= foreign key. Cột in đậm ở notebook \= thường dùng làm feature hoặc groupby.

| File | PK / FK | Cột đắt giá cho phân tích |
| :---- | :---- | :---- |
| **products** | PK product\_id | category (4), segment (8), size (S/M/L/XL), color, price, cogs |
| **customers** | PK customer\_id, FK zip | signup\_date, age\_group (nullable), gender (nullable), acquisition\_channel (nullable) |
| **geography** | PK zip | region (East/Central/West), city (42), district |
| **promotions** | PK promo\_id | promo\_type (percentage/fixed), discount\_value, start\_date, end\_date, applicable\_category, stackable\_flag, min\_order\_value |
| **orders** | PK order\_id, FK customer\_id, zip | order\_date, order\_status (6), payment\_method (5), device\_type (3), order\_source (6) |
| **order\_items** | PK (order\_id, product\_id); FK promo\_id, promo\_id\_2 | quantity, unit\_price (ĐÃ giảm giá\!), discount\_amount |
| **payments** | FK order\_id (1:1) | payment\_method, payment\_value, installments (1/3/6/12) |
| **shipments** | FK order\_id (1:0/1) | ship\_date, delivery\_date, shipping\_fee (0 \= free) |
| **returns** | PK return\_id; FK order\_id, product\_id | return\_date, return\_reason (5), return\_quantity, refund\_amount |
| **reviews** | PK review\_id; FK order\_id, product\_id, customer\_id | review\_date, rating (1-5), review\_title |
| **inventory** | PK (snapshot\_date, product\_id) | stock\_on\_hand, stockout\_days, days\_of\_supply, fill\_rate, stockout\_flag, overstock\_flag, reorder\_flag, sell\_through\_rate (+category, segment denorm) |
| **web\_traffic** | PK date (từ 2013-01-01) | sessions, unique\_visitors, page\_views, bounce\_rate, avg\_session\_duration\_sec, traffic\_source (6). KHÔNG có conversion\_rate → tự tính orders/sessions. |
| **sales** | PK Date (2012-07-04 → 2022-12-31, 3833 dòng) | Revenue, COGS — ★ TARGET train. PDF dùng cả tên sales.csv (Table 1\) lẫn sales\_train.csv (Split). File thật trên disk: sales.csv. |
| **sample\_submission** | PK Date (2023-01-01 → 2024-07-01, 548 dòng) | Revenue, COGS dummy — ★ format test. File test thật (sales\_test.csv) không public. |

## **3.2. 7 cái bẫy dữ liệu PHẢI biết**

*Đã gặp hoặc dự kiến gặp khi code — ghi ra để không ai lặp lại:*

| Cạm bẫy | Chi tiết & cách xử |
| :---- | :---- |
| **\#1. order\_items.unit\_price là GIÁ SAU GIẢM** | Không phải giá list. Muốn ra giá gốc: (qty × unit\_price \+ discount\_amount) / qty. Nếu quên, tất cả phân tích pricing / gross margin sẽ sai. |
| **\#2. PDF dùng 2 tên cho cùng file train** | Table 1 gọi sales.csv; Split table và Q7 gọi sales\_train.csv. File thật trên disk: sales.csv. Trích dẫn trong báo cáo nên thống nhất 1 tên (nên dùng 'sales.csv (Train split)'). |
| **\#3. inventory\_enhanced.csv KHÔNG tồn tại** | PDF cũ liệt kê file \#14, PDF 2026-04-19 đã xoá. inventory.csv hiện tại đã có enhanced columns (stockout\_flag, overstock\_flag, reorder\_flag, sell\_through\_rate). Không đi tìm file riêng. |
| **\#4. web\_traffic.csv chỉ có đến 2022-12-31** | Test period 2023-01-01 → 2024-07-01 KHÔNG có traffic. 3 option xử lý: (a) forecast traffic riêng, (b) rolling mean 2022 proxy, (c) bỏ traffic feature. Decide trước khi build FE pipeline. |
| **\#5. shipments chỉ tồn tại cho 3 status** | Chỉ shipped/delivered/returned. Orders status cancelled/paid/created không có dòng shipment → left join sẽ có NaN, đừng coi là data quality issue. |
| **\#6. web\_traffic.csv bắt đầu 2013-01-01, sales.csv bắt đầu 2012-07-04** | 6 tháng đầu của sales KHÔNG có dữ liệu traffic. Dùng inner join sẽ mất 180 ngày, hoặc chấp nhận NaN và cho model học. |
| **\#7. inventory.csv snapshot end-of-month, không có daily** | Phải forward-fill sang daily khi join với sales. Không có inventory cho 2023+ (giống web\_traffic) → cần forward-fill 2022-12-31 snapshot hoặc drop feature. |

# **4\. Brainstorm — ý tưởng tổng hợp & chiến lược**

| Bản đồ §4 (đọc theo luồng):  §4.1 Narrative (khung story) ─▶ quyết định chart nào vào báo cáo.  §4.2 12 ý tưởng EDA ─▶ cung cấp insight cho §4.4 (Prescriptive) \+ feature cho §4.3 (Model).  §4.3 Feature blocks ─▶ input cho notebook 05/06/07 (Kiên). Mỗi block link về ý EDA nguồn.  §4.4 Prescriptive KPI ─▶ ending của story §4.1; phục vụ 3 business goal §2.1; con số 'Dự kiến impact' do §4.3 forecast cung cấp.  §4.5 Coverage matrix ─▶ audit: mỗi ý §4.2 có phủ đủ 14 CSV không. |
| :---- |

## **4.1. Narrative xuyên suốt (đề xuất)**

*→ Phụ trách: Kiên (Insights Lead). Tham chiếu: §4.2 (chart), §4.4 (ending \= action).*

| Tagline báo cáo: "Từ DATA đến DECISION — Hành trình tăng trưởng 10 năm của một thương hiệu thời trang Việt Nam." Cấu trúc story 5 nút:  (1) Quá khứ 2013-2019 — tăng trưởng  → chart từ §4.2 ý \#4 (regional growth) \+ \#11 (segment mix).  (2) Cú sốc COVID 2020-2021  → chart từ §4.2 ý \#10 (seasonality \+ event overlay).  (3) Phục hồi 2022  → chart từ §4.2 ý \#2 (promo ROI) \+ \#5 (inventory-sales mismatch).  (4) Dự báo 2023-2024  → chart từ §4.3 (pred vs actual \+ SHAP summary).  (5) Khuyến nghị hành động cho 3 business goals  → toàn bộ §4.4. |
| :---- |

Vì báo cáo ≤4 trang, chỉ nên giữ tối đa 5-6 chart 'đắt giá nhất' cho EDA \+ 2 chart cho Forecasting (pred vs actual trên val, SHAP summary). Appendix có thể chứa chart phụ. Kỷ luật chọn chart: mỗi chart phải gắn với 1 nút trong story arc trên \+ 1 hàng trong §4.4 (nếu không có action → cắt).

| 4 story arc dự phòng (thematic lens — dùng khi viết notebook 04 cần chia section theo chủ đề, hoặc khi narrative 5-nút không fit slot chart):  • Story A — 'Doanh thu không chỉ nằm ở traffic': consume ý \#6 (web funnel) \+ §4.4 'Channel-mix budget'.  • Story B — 'Khuyến mãi là con dao hai lưỡi': consume ý \#2 (Promo ROI) \+ \#9 (cannibalization) \+ §4.4 'Promo scheduling'.  • Story C — 'Tồn kho & size ảnh hưởng trải nghiệm': consume ý \#3 (return × size) \+ \#5 (inventory mismatch) \+ §4.4 'Size-guide fix' \+ 'Inventory reorder'.  • Story D — 'Nhóm khách hàng mục tiêu': consume ý \#1 (cohort retention) \+ \#11 (segment mix) \+ §4.4 'Customer retention' \+ 'Pricing & discount'.Narrative 5-nút (Quá khứ → COVID → Phục hồi → Dự báo → Khuyến nghị) vẫn là PRIMARY story cho PDF ≤4 trang. 4 story arc trên là lens bổ trợ cho notebook section, không thay thế narrative chính. |
| :---- |

## **4.2. 12 ý tưởng EDA — Framework TTM (Pain → Truth → Tension → Motivation → Insight → Action)**

*→ Phụ trách: Đồng (ý D/Di) \+ Kiên (ý P/Pr). Mỗi ý chỉ rõ section nào của §4 sẽ 'tiêu thụ' kết quả.*

| Framework TTM — chuẩn 'lọt top' cho mỗi ý EDA (bắt buộc đủ 6 layer):  • Pain — business pain point cụ thể (ai đau, đau ở đâu, đau bao nhiêu tiền).  • Truth — fact từ data sau phân tích (con số \+ chart reference, observable, verifiable).  • Tension — mâu thuẫn ngầm customer không nói ra, là chỗ business đang hiểu sai.  • Motivation — động lực sâu behind customer behavior (lý do thật họ hành xử thế).  • Insight (the one line) — câu chốt ≤20 từ; BGK đọc 1 lần là nhớ. Insight phải 'đắt hơn truth'.  • Action — hành động business team làm ngay → liên kết §4.4 \+ 1 business goal §2.1.Nối tiếp plan cũ: mỗi ý có 2 link explicit → §4.1 nút (N) \+ §4.4 hàng 'X'. Block 'Execution note' giữ H/T/A cũ cho người phân tích chạy code.Icon 🔄 \= counter-intuitive takeaway (nhắm điểm 'Tính sáng tạo & kể chuyện' §2.3 rubric). |
| :---- |

*Lưu ý về template: chart-level annotation trong notebook 03/04 dùng O-E-I-A (Observation → Evidence → Interpretation → Action) cho gọn. Insight-level callout trong PDF báo cáo PHẢI dùng TTM — TTM supersedes O-E-I-A cho báo cáo ≤4 trang.*

**★ 1\. Customer lifecycle & cohort retention**

  *· Datasets: customers ⨝ orders (customer\_id)  ·  Tầng: Di \+ Pr  ·*  

  **Pain:** CAC cao nhưng churn 90-day ở social\_media lớn → marketing đốt tiền không hoàn vốn.

  **Truth:** Cohort 90-day retention paid\_search ≈ X% vs social\_media ≈ Y% (cohort heatmap count distinct customer\_id quay lại theo tháng).

  **Tension:** Marketing nghĩ social là 'brand awareness' nên churn OK; data cho thấy social user không bao giờ quay lại mua lần 2\.

  **Motivation:** Paid\_search đến với nhu cầu cụ thể ('tôi cần áo mùa thu') → loyal vì problem-solution fit. Social đến vì giải trí, không cần sản phẩm.

  **Insight: Social\_media mua 1 lượt — paid\_search mới mua lần 2\.*

  **Action:** Email re-engage cohort social sau 90 ngày; re-allocate budget sang paid\_search nếu retention gap \>2×.

  *→ §4.1 nút (1) Quá khứ tăng trưởng  ·  → §4.4 hàng 'Customer retention'  ·  → §4.3 block 'Customer/Return signals (lag\_365)'*

  ***Execution note:** H: paid\_search retention 90-day \> social\_media. T: cohort heatmap \= count distinct customer\_id quay lại tháng M+k / tại M, split theo acquisition\_channel. A: tăng CPA bid paid\_search nếu H đúng; nếu sai → social cần retention campaign.*

**★ 🔄 2\. Promo ROI deep-dive (50 campaign / 10.5 năm — sparse)**

  *· Datasets: promotions ⨝ order\_items ⨝ orders ⨝ sales  ·  Tầng: Di \+ Pr  ·*  

  **Pain:** 50 campaign tốn discount cost 10.5 năm — không rõ campaign nào thật sự incremental vs pull-forward demand.

  **Truth:** Top 5 campaign Δrevenue vs same-week-prior-year ≈ \+X%; bottom 5 ≈ −Y% (cannibalize baseline).

  **Tension:** Marketing nghĩ mỗi discount đều 'kích cầu'; số liệu cho thấy campaign dài chỉ pull-forward, không tạo demand mới.

  **Motivation:** Khách mua khi promo không vì 'giá rẻ' mà vì deadline (FOMO). Campaign \>7 ngày không có urgency → cannibalize baseline.

  **Insight: Promo không tạo demand — promo chỉ dịch chuyển thời điểm mua. Chỉ scarcity mới incremental.**

  **Action:** Rút promo window ≤3 ngày; target segment chưa mua 90 ngày thay vì blast-all.

  *→ §4.1 nút (3) Phục hồi  ·  → §4.4 hàng 'Promo scheduling'  ·  → §4.3 block 'Promo indicators'  ·  Liên quan MCQ Q5*

  ***Execution note:** H: promo percentage có incremental revenue \> fixed amount. T: cho mỗi campaign tính Δrevenue trong promo window vs same-week prior year, split promo\_type. A: Top 5 case study; Bottom 5 rút kinh nghiệm; quantify $X incremental/năm nếu scale top pattern.*

**★ 3\. Return reason × size × category heatmap**

  *· Datasets: returns ⨝ order\_items ⨝ products  ·  Tầng: Di \+ Pr  ·*  

  **Pain:** Mỗi return \= phí ship 2 chiều \+ refund \+ hàng second-hand khó bán lại → margin ăn mòn.

  **Truth:** wrong\_size chiếm ≥40% returns ở Streetwear; tập trung size S/XL (extremes) — pivot heatmap (category, size, reason).

  **Tension:** Ops nghĩ khách 'đổi ý'; thực chất size chart lệch so với body thật của Gen-Z VN.

  **Motivation:** Khách Gen-Z mua online theo size số (không thử); lệch 1 size \= buộc phải trả, không phải 'whim'.

  **Insight: Return không phải 'đổi ý' — đó là size chart đang nói dối khách.**

  **Action:** Fix size guide top 3 SKU wrong\_size cao nhất; thêm tag 'chạy đúng/to/nhỏ' từ review users.

  *→ §4.1 nút (3) Phục hồi  ·  → §4.4 hàng 'Size-guide fix'  ·  → §4.3 block 'Customer/Return signals (lag\_365)'  ·  Liên quan MCQ Q3*

  ***Execution note:** H: wrong\_size chiếm ≥40% returns ở Streetwear, tập trung S/XL. T: pivot count(return\_id) trên (category, size, reason) \+ chi-square. A: fix size guide top 3 SKU; refund\_saved \= N\_wrong\_size × avg\_refund × 30% giảm.*

**★ 4\. Regional growth map (East/Central/West)**

  *· Datasets: order\_items ⨝ orders ⨝ geography  ·  Tầng: D \+ P  ·* 

  **Pain:** Warehouse đặt cố định (giả định HN/miền Bắc) trong khi demand East (HCM) tăng nhanh → lead-time East dài, chi phí reverse logistics cao.

  **Truth:** East YoY revenue growth 2020-2022 ≈ \+X%/năm, West ≈ \+Y%/năm (choropleth region × year, linear fit YoY, CI 95%).

  **Tension:** Supply chain nghĩ 'các vùng mua như nhau'; gravity demand đã dịch về East từ 2020\.

  **Motivation:** HCM đô thị hoá nhanh, Gen-Z online-first; miền Bắc-Trung còn offline-first.

  **Insight: Demand đã chuyển về East, nhưng warehouse vẫn ở đâu đó giữa BC 2018\.**

  **Action:** Mở warehouse vệ tinh East → giảm lead-time 5 → 3 ngày.

  *→ §4.1 nút (1) Quá khứ tăng trưởng  ·  → §4.4 hàng 'Regional logistics'  ·  → §4.3 block 'Rolling features' (region-level optional)  ·  Liên quan MCQ Q7*

  ***Execution note:** H: East tăng trưởng YoY nhanh nhất 2020-2022. T: choropleth region × year; linear fit. A: pre-stock inventory East; cross-check với shipments.lead\_time per region.*

**★ 5\. Inventory–sales mismatch (lost revenue)**

  *· Datasets: inventory ⨝ order\_items ⨝ orders ⨝ sales  ·  Tầng: Di \+ Pr  ·*  

  **Pain:** Stockout \= lost revenue; overstock \= vốn chết \+ rủi ro giảm giá cuối mùa.

  **Truth:** \~15% peak-demand SKU-day có stockout\_flag=1 trong Q4 (mùa lễ); lost\_revenue \= avg\_daily\_qty × stockout\_days × unit\_price.

  **Tension:** Supply chain báo 'đủ hàng' theo tổng; SKU-level cho thấy bestseller hết trong khi slow-mover dư.

  **Motivation:** Buyer tính theo tổng doanh thu, không theo SKU profile → không phân bổ đủ cho bestseller.

  **Insight: Out-of-stock không phải vấn đề supply — là vấn đề phân bổ. Bestseller thiếu trong khi slow-movers dư.**

  **Action:** Reorder threshold \= days\_of\_supply × 1.3 cho top 50 SKU (80% revenue); reclaim $X revenue/năm. Xây dựng quy tắc "Markdown tự động" (giảm giá xả hàng) cho các mã SKU có `overstock_flag=1` và `sell_through_rate` \< 20% sau 60 ngày ra mắt để thu hồi dòng tiền, thay vì chịu phí lưu kho.

  *→ §4.1 nút (3) Phục hồi  ·  → §4.4 hàng 'Inventory reorder'  ·  → §4.3 block 'Inventory signals'*

  ***Execution note:** H: ≥15% peak-demand SKU-day rơi vào stockout\_flag=1 Q4. T: forward-fill inventory daily × order\_items; lost\_revenue. A: reorder threshold top 50 SKU.*

**★ 🔄 6\. Web-traffic funnel (orders-per-session proxy)**

  *· Datasets: web\_traffic \+ orders (attribute theo source)  ·  Tầng: D \+ P  ·*  

  **Pain:** Marketing budget phân đều 6 channel không biết channel nào thật sự convert → ROAS ảo.

  **Truth:** paid\_search bounce cao nhưng (n\_orders/sessions) × AOV ≈ cao nhất; email bounce thấp nhưng AOV thấp.

  **Tension:** Marketing coi 'bounce thấp \= tốt'; bounce cao có thể là user biết mình cần gì, click-and-buy.

  **Motivation:** User paid\_search đến với intent rõ (có search query); user email đến vì tò mò newsletter.

  **Insight: Bounce cao không phải user hỏng — có thể là user biết mình cần gì và mua thẳng.**

  **Action:** Shift 20% budget social → paid\_search; track conv × AOV thay vì bounce.

  *→ §4.1 nút (4) Dự báo  ·  → §4.4 hàng 'Channel-mix budget'  ·  → §4.3 block 'Traffic features' (cần decide option a/b/c — §9)  ·  Liên quan MCQ Q4*

  ***Execution note:** H: paid\_search bounce cao nhưng conv cao nhất vì intent; email bounce thấp nhưng AOV thấp. T: (conv\_proxy \= n\_orders\_attributed / sessions) × AOV, plot 2D. A: optimize bid → channel có conv × AOV cao. ⚠ Traffic chỉ 2013-2022, không có test period.*

**★ 🔄 7\. Payment & device behaviour**

  *· Datasets: orders ⨝ payments  ·  Tầng: D \+ Di  ·* 

  **Pain:** COD cancel \~30% → mất ship đi \+ warehouse picking cost ăn vào margin.

  **Truth:** COD cancel rate ≈ 30%, credit\_card ≈ 5% (groupby(payment\_method) % status=='cancelled').

  **Tension:** Shop nghĩ COD là service 'build trust với khách mới'; khách COD đã không trust ngay từ đầu.

  **Motivation:** Chọn COD vì không tin shop → chờ 3-5 ngày ship khuếch đại nghi ngờ → cancel.

  **Insight: COD không phải payment method — đó là niềm tin còn thiếu.**

  **Action:** Voucher 2% prepaid cho COD khách cũ; ship express COD \<24h để rút window nghi ngờ.

  *→ §4.1 nút (3) Phục hồi  ·  → §4.4 hàng 'COD optimization'  ·  → §4.3 block 'Order aggregates (pct\_cod\_d, pct\_cancelled\_d)'  ·  Liên quan MCQ Q8/Q10*

  ***Execution note:** H: COD có cancel rate cao nhất \~30%. T: groupby(payment\_method) % cancelled \+ chi-square. A: voucher 2% cho COD; giảm cancel 5% → tiết kiệm $X.*

**★ 8\. Review → return correlation**

  *· Datasets: reviews ⨝ orders ⨝ returns ⨝ products  ·  Tầng: Di \+ P  ·*  

  **Pain:** Review xấu damage lên cả product listing, không chỉ 1 đơn — ảnh hưởng lâu dài.

  **Truth:** Orders có rating ≤2 có return rate cao gấp \~3× orders rating ≥4 (2×2 contingency \+ fisher exact).

  **Tension:** CSKH chỉ phản hồi sau khi review public — đã muộn, reputation damage đã xảy ra.

  **Motivation:** Khách để review thấp không vì ghét — vì muốn được nghe. Phản hồi kịp thời → đa số xoá review.

  **Insight: Review thấp là SOS, không phải feedback. Nghe kịp thì cứu được cả đơn lẫn danh tiếng.**

  **Action:** Trigger CSKH reach-out ≤48h sau review ≤2; giảm return 20% nếu H đúng.

  *→ §4.1 nút (3) Phục hồi  ·  → §4.4 hàng 'Size-guide fix' (bổ sung CSKH post-review trigger)*

  ***Execution note:** H: orders rating ≤2 có return rate 3× orders rating ≥4. T: 2×2 contingency (rating ≤2 vs ≥3) × (returned vs not) \+ fisher exact. A: CSKH trigger post-review ≤48h.*

**★ 🔄 9\. Discount cannibalization**

  *· Datasets: promotions ⨝ order\_items ⨝ orders ⨝ customers  ·  Tầng: Di \+ Pr  ·*  

  **Pain:** Discount cost $X/năm không biết bao nhiêu % là 'giảm giá cho khách vốn đã sẵn sàng mua full price'.

  **Truth:** \>60% revenue promo đến từ returning customers (đã mua ≤30 ngày trước) — split pre-promo vs during-promo × flag first-time/returning.

  **Tension:** CMO nghĩ promo là 'acquisition tool'; thực chất là 'retention discount' không ai gọi tên.

  **Motivation:** Returning customer sẽ mua full price nếu không có promo; khi có promo, họ đợi rồi mua. Promo đang train khách đợi sale.

  **Insight: Promo đại trà không acquire khách mới — mà dạy khách cũ đợi sale.**

  **Action:** Target segment chưa mua 90 ngày (behavioural trigger); không blast-all.

  *→ §4.1 nút (3) Phục hồi  ·  → §4.4 hàng 'Promo scheduling' (bổ sung targeting)  ·  → §4.3 block 'Promo indicators'  ·  Liên quan MCQ Q5*

  ***Execution note:** H: \>60% revenue promo đến từ returning customers → cannibalize. T: split pre vs during promo, flag first-time vs returning, % new customer acquired trong promo. A: target segment dormant 90 ngày.*

**★ 🔄 10\. Seasonality: Tết / 11.11 / 12.12 / Black Friday**

  *· Datasets: sales \+ promotions \+ self-built VN calendar  ·  Tầng: P \+ Pr  ·*  

  **Pain:** Promo budget lãng phí khi trùng peak mùa vụ (demand tự peak không cần boost); pre-stock cũng lệch.

  **Truth:** Revenue tuần Tết \+0→+7 thấp hơn baseline ≈ 30%; 11.11 peak ≈ \+200% baseline tự phát (STL decompose \+ event overlay).

  **Tension:** Merch team chạy promo Tết và 11.11 vì 'đó là mùa sale'; Tết promo mất cost, 11.11 promo cannibalize margin.

  **Motivation:** Khách VN mua theo pattern văn hoá (Tết ở với gia đình; 11.11 là shopping festival của họ) — không cần shop kích.

  **Insight: Mùa vụ không cần promo — promo cần đánh ngoài mùa.**

  **Action:** KHÔNG promo tuần Tết \+7; pre-stock \+14 ngày trước Tết; 'pre-11.11' 1 tuần bắt early shopper thay vì 'all-in 11.11'.

  *→ §4.1 nút (2) COVID \+ (4) Dự báo  ·  → §4.4 hàng 'Promo scheduling' \+ 'Inventory reorder'  ·  → §4.3 block 'Calendar features (self-built)'*

  ***Execution note:** H: revenue tuần Tết \+0→+7 thấp hơn baseline 30% (bận lễ, logistics đóng). T: STL decompose \+ event overlay; boxplot trong vs ngoài window. A: tránh launch promo Tết; pre-stock 14 ngày trước Tết; feed holiday\_flag vào model Phần 3\.*

**★ 🔄 11\. Gross-margin × segment mix**

  *· Datasets: products ⨝ order\_items ⨝ orders  ·  Tầng: D \+ Pr  ·*  

  **Pain:** Segment Premium margin 60% nhưng revenue share giảm 2021-2022 → mất vũ khí lợi nhuận.

  **Truth:** Premium volume 2021 ≈ X đơn, 2022 ≈ Y đơn (−Z%); Activewear volume \+W% (Pareto 80/20 \+ trend YoY per segment).

  **Tension:** Merch nghĩ 'khách trẻ chỉ muốn Activewear giá rẻ'; thực chất Premium bị bỏ quên, không phải không còn khách.

  **Motivation:** Khách ngân sách Premium vẫn tồn tại, nhưng không được target ads, không thấy collection mới → chuyển brand khác.

  **Insight: Premium không chết — Premium bị bỏ đói marketing.**

  **Action:** Bundle Premium \+ Activewear cross-category; raise price Premium \+5% khi elasticity ước tính \<0.5.

  *→ §4.1 nút (1) Quá khứ tăng trưởng  ·  → §4.4 hàng 'Pricing & discount'  ·  Liên quan MCQ Q2*

  ***Execution note:** H: segment Premium margin \~60% nhưng volume giảm 2021-2022. T: margin % theo segment \+ revenue trend YoY; Pareto 80/20. A: bundle Premium \+ Activewear; raise price \+5% khi elasticity \<0.5.*

**★ 🔄 12\. Shipping fee vs return rate**

  *· Datasets: shipments ⨝ orders ⨝ returns  ·  Tầng: Di \+ Pr  ·* 

  **Pain:** Free-shipping tốn ship cost, tưởng boost doanh thu nhưng return rate ăn hết margin.

  **Truth:** Free-ship orders có return rate cao hơn paid-ship ≈ 15% (odds ratio \>1.2; 2×2 shipping\_fee==0 vs \>0 × returned vs not).

  **Tension:** Growth team đẩy free-ship vì 'conversion lift'; return rate ăn hết margin gain.

  **Motivation:** Free-ship khiến khách 'thử miễn phí, rủi ro \= 0' → mua nhiều size/color rồi trả phần thừa (try-before-buy abuse).

  **Insight: Free-ship không kéo khách — free-ship tạo fitting room miễn phí.**

  **Action:** min\_order\_value cho free-ship; cap số SKU free-ship return / customer / tháng.

  *→ §4.1 nút (3) Phục hồi  ·  → §4.4 hàng 'Regional logistics' (bổ sung min\_order\_value rule)*

  ***Execution note:** H: free-ship orders return rate cao hơn 15%. T: 2×2 table (shipping\_fee==0 vs \>0) × (returned vs not); odds ratio \+ CI. A: min\_order\_value cho free-ship.*

| ★ Counter-intuitive takeaway (icon 🔄): 6 ý \#2, \#6, \#7, \#10, \#11, \#12 có insight đảo ngược trực giác — dùng để 'đánh' điểm Tính sáng tạo & Kể chuyện (5đ, §2.3 rubric). Mỗi ý tag Pr phải kết nối 1 trong 3 business goals (inventory / promo / logistics — §2.1 / CLAUDE.md §1) khi viết insight báo cáo. Chart nào không dẫn đến action cụ thể nên cắt. Luật nhất quán: nếu §4.2 tạo ra insight X mà §4.3 không có feature tương ứng \+ §4.4 không có hàng action → một trong hai bên đang miss; báo ngay cho cả team. |
| :---- |

## **4.3. Model Phần 3 — feature block chi tiết**

*→ Phụ trách: Phúc (ML Engineer). Cột '→ EDA §4.2' chỉ rõ ý tưởng EDA nào validate/cung cấp cho block này.*

Target: predict Revenue \+ COGS hàng ngày 548 ngày 2023-01-01 → 2024-07-01. Bảng dưới liệt kê từng khối feature, nguồn CSV, giá trị lag/window cụ thể, ràng buộc anti-leakage, và liên kết ngược về §4.2.

| Feature block | Cột / Biến tạo | CSV nguồn & ràng buộc | → EDA §4.2 nguồn |
| :---- | :---- | :---- | :---- |
| **Baseline seasonal × growth** | base\_level × growth^years\_ahead × seasonal(month, day) | sales.csv duy nhất. Benchmark tối thiểu; model nâng cao phải beat ≥20% MAE. | (nền) ý \#10 Seasonality \+ §4.1 story arc |
| **Lag features (Revenue, COGS)** | lag\_7, lag\_14, lag\_28, lag\_365; diff\_7, diff\_365 | sales.csv. Test xa 548 ngày → phải recursive forecast (predict step-by-step) hoặc chỉ dùng lag ≥548 (lag\_548, lag\_730). | ý \#10 Seasonality (lý do chọn lag\_365) |
| **Rolling features** | rolling\_mean\_7/30/90, rolling\_std\_7/30, rolling\_min\_max\_30 | sales.csv. Rolling KHÔNG bao gồm day t (shift 1). Test 2023+ → phải recursive hoặc dùng rolling dựa trên lag ≥548. | ý \#4 Regional growth \+ ý \#11 Segment mix (trend mượt) |
| **Calendar features (SELF-BUILT)** | day\_of\_week, month, quarter, is\_month\_end, is\_tet (lunar), is\_quoc\_khanh, is\_black\_friday, is\_1111, is\_1212 | ⚠ KHÔNG import Prophet holidays (external data → LOẠI). Tự build DataFrame VN holiday 2012-2024 từ list tĩnh. | ý \#10 Seasonality (VN event list) |
| **Order aggregates (historical)** | n\_orders\_d, n\_unique\_customers\_d, pct\_cancelled\_d, pct\_cod\_d, pct\_mobile\_d, avg\_AOV\_d | orders group by order\_date. Các agg này KHÔNG có cho test 2023+ → dùng LAG (ví dụ lag\_365) hoặc forecast riêng. | ý \#7 Payment/device behaviour |
| **Order-item aggregates** | n\_lines\_d, n\_units\_sold\_d, pct\_promo\_d, avg\_discount\_pct\_d, n\_unique\_SKU\_d | order\_items group by order\_date. Tương tự: chỉ dùng lag cho test period. | ý \#2 Promo ROI \+ ý \#9 Cannibalization |
| **Traffic features** | sessions\_d, bounce\_rate\_d, page\_views\_d, pct\_paid\_search\_d, pct\_social\_d, avg\_duration\_d, engagement\_index (= avg\_session\_duration × (1 − bounce\_rate)), traffic\_momentum (= sessions / sessions.rolling(7).mean()) | web\_traffic daily. Chỉ có 2013-2022, không có test → Option (a) forecast riêng / (b) rolling 2022 proxy / (c) drop. Decide Phase 6\. | ý \#6 Web funnel (cần output conv\_proxy) |
| **Promo indicators** | active\_promo\_today, n\_active\_promos, days\_since\_last\_promo, days\_until\_next\_promotion, days\_since\_promotion, promo\_type\_one\_hot | promotions expand daily. 50 campaign đã biết lịch 2013-2022. Test 2023+ → dùng historic seasonality như proxy hoặc gán all-zero (conservative). | ý \#2 Promo ROI \+ ý \#9 Cannibalization |
| **Inventory signals** | total\_stock\_on\_hand\_d, pct\_SKU\_stockout\_d, avg\_days\_of\_supply\_d, n\_overstock\_d | inventory end-of-month → reindex daily forward-fill. Test 2023+ → forward-fill 2022-12-31 snapshot hoặc drop. Decide cùng web\_traffic. | ý \#5 Inventory-sales mismatch |
| **Cash-flow features** | money\_in \= Σ credit\_card \+ apple\_pay \+ bank\_transfer trên order\_date \+ Σ cod trên delivery\_date (khi tiền thực nhận)  ·  money\_out \= Σ refund\_amount từ returns  ·  net\_cash\_d \= money\_in − money\_out | payments \+ shipments (delivery\_date cho COD) \+ returns. Note: COD revenue được 'ghi' khi giao thành công, không phải khi đặt → proxy doanh thu thực nhận khác với Revenue đăng ký. | Bổ trợ target Revenue/COGS \+ ý \#7 Payment behaviour |
| **Customer / Return signals (lag)** | lag\_365\_return\_rate, lag\_365\_new\_customer\_share, new\_customers\_count (mỗi ngày số customer có first order \= day t, chỉ dùng làm lag 365), average\_ratings\_d (rolling 30 ngày) | returns \+ customers \+ reviews, chỉ dùng làm LAG 365 để tránh future leak. new\_customers\_count / average\_ratings phải shift ≥548 ngày hoặc chỉ dùng historic pattern cho test period. | ý \#1 Lifecycle \+ ý \#3 Return reason \+ ý \#8 Review→return |
| **Calendar features (SELF-BUILT)** | day\_of\_week, day\_of\_month, month, quarter, is\_weekend, is\_month\_end, is\_tet (lunar), is\_quoc\_khanh, is\_black\_friday, is\_1111, is\_1212 | ⚠ KHÔNG import Prophet holidays (external data → LOẠI). Tự build DataFrame VN holiday 2012-2024 từ list tĩnh. day\_of\_month/is\_weekend giúp bắt pattern pay-day \+ cuối tuần. | ý \#10 Seasonality (VN event list) |
| **Model chính** | LightGBM 2 head (Revenue \+ COGS) — direct multi-output; Python 3.10, lightgbm ≥4.0, random\_state=42 | Cân nhắc 2 model độc lập vs 1 MultiOutput. Early stopping theo temporal val. n\_estimators cap 2000\. MAE là metric chính (Kaggle), KHÔNG dùng MSE nội bộ. | — (mô hình trung tâm) |
| **Model candidates (taxonomy)** | Statistical: SARIMAX (Prophet ⚠ §7 rủi ro external holiday → skip hoặc tắt holidays)  ·  ML: LightGBM, XGBoost, CatBoost (direct multi-output)  ·  DL: DLinear, N-HITS, TimeXer, TimeMixer, TiDE, Temporal Fusion Transformer (note thời gian train \+ GPU cost)  ·  Zero-shot / Foundation: TimesFM, Moirai, Chronos | Foundation weights KHÔNG phải 'external data' — chỉ dùng train-free inference trên sales.csv nội bộ, hợp lệ ràng buộc §3. DL options phải cân nhắc train time vs pred\_len=548 (TFT/N-HITS thường \>1h GPU). | — (shortlist cho Phase 6c) |
| **Ensemble strategies** | (a) Top 3-5 best models → weighted average với learnable weights (lr-grid trên val 2022\)  ·  (b) Temporal hierarchical: train tại Daily / Weekly / Monthly / Quarterly / Yearly → chọn best per level → Reconciliation (Top-down / Bottom-up / MinT — tối thiểu implement Bottom-up vì đơn giản nhất) | Robust hơn khi COVID-like shock. Weight chọn trên val set 2022\. Hierarchical reconciliation giúp aggregate consistency giữa Daily và Monthly forecast. | ý \#10 Seasonality (SARIMAX bắt mùa vụ) \+ §4.1 nút (4) |
| **Temporal CV — 5-fold rolling window** | k=365 step, pred\_len=548  ·  weights \= \[0.1, 0.15, 0.2, 0.25, 0.3\] (fold mới nhất weight cao hơn)  ·  Fold 1: Train \[t\_0 → t\_n\], Val \[t\_n+1 → t\_n+pred\_len\]  ·  Fold 2: Train \[t\_0 → t\_n+k\], Val \[t\_n+k+1 → t\_n+k+pred\_len\]  ·  … | Tổng train 3,833 ngày → có thể chỉ đủ 2-3 fold thực tế với pred\_len=548. Nếu thiếu, degrade xuống 3-fold và note trong báo cáo. KHÔNG random split. Code: src/cv.py (Phase 6). | — (audit §3.2 bẫy \#2 \+ §7 risk leakage) |
| **Metric selection** | Primary \= MAE (Kaggle leaderboard)  ·  Sanity-check \= RMSE, R²  ·  Submit Kaggle bằng model có MAE thấp nhất trên val trung bình (weighted theo fold recency) | KHÔNG dùng MSE nội bộ — MAE là metric Kaggle chính. Weighted MAE ưu tiên fold mới nhất để phản ánh pattern gần test period. | — (căn cứ §2.3 Part 3 rubric hiệu suất) |
| **Explainability** | SHAP TreeExplainer: summary plot \+ top-10 feature bar \+ 2 force plot (ngày bất thường) | Diễn giải business: 'Tết → lag\_365 dominate vì pattern năm trước'. Permutation importance bổ sung để cross-check SHAP. | Narrative §4.1 nút (4) Dự báo \+ §4.4 (justify action bằng feature importance) |

*→ Output của §4.3 quay ngược phục vụ §4.4: con số 'Dự kiến impact định lượng' trong §4.4 nên dùng forecast từ model này (vd: tính Δrevenue khi \+5% price Premium \= model predict với feature price tăng). Nếu thiếu hụt thời gian, dùng công thức heuristic trong §4.4 cột 'CSV & công thức'.*

## **4.4. Tầng Prescriptive — KPI & số định lượng mẫu**

*→ Phụ trách: Kiên (Insights Lead). Số 'Dự kiến impact' nên dùng output từ §4.3 (model). Mỗi hàng là ending của 1 ý §4.2.*

Top team được đánh giá ở đây (Insight 15đ). Cột 'CSV & công thức' liệt kê nguồn \+ metric cụ thể để phản biện khi BGK hỏi 'dựa vào đâu?'. Cột 'Dự kiến impact' cho con số ước lượng (phải định lượng được). Cột '← §4.2' chỉ rõ ý EDA nào sinh ra hàng này; cột 'Business goal' chỉ rõ 1 trong 3 mục tiêu §2.1 mà khuyến nghị này phục vụ.

| Domain | Khuyến nghị cụ thể | CSV & công thức | Dự kiến impact định lượng | ← §4.2 ý | Business goal (§2.1) |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Pricing & discount** | Tăng giá segment Premium \+5%; segment có demand elasticity \< 0.5 trong analysis promo | products (price, cogs, segment) \+ order\_items \+ promotions → margin % \+ price-elasticity \= %Δqty/%Δprice | Nếu elasticity 0.3, \+5% price → −1.5% qty → net \+3.4% revenue Premium | \#11 Gross-margin × segment | (2) Promo planning |
| **Inventory reorder** | Reorder threshold \= days\_of\_supply × 1.3 cho top 50 SKU (80% revenue) | inventory \+ demand forecast từ sales → expected\_daily\_demand × 1.3 | Giảm stockout 30% → reclaim \~$X revenue/năm (tính từ lost\_revenue analysis ý \#5) | \#5 Inventory-sales mismatch \+ \#10 Seasonality | (1) Inventory optimization |
| **Channel-mix budget** | Shift 20% budget social\_media → paid\_search (conv proxy cao hơn 2.3×) | web\_traffic \+ orders (order\_source) → (n\_orders/sessions) × AOV | Ở cùng budget, \+18% total orders từ paid\_search (nếu ROAS scale tuyến tính) | \#6 Web-traffic funnel | (2) Promo planning |
| **Customer retention** | Email re-engagement sau \~90 ngày (median inter-order gap từ Q1 MCQ) | customers \+ orders → cohort retention \+ inter-order gap distribution | Re-engage 20% dormant cohort → $Y incremental nếu AOV \= $Z | \#1 Lifecycle \+ \#8 Review→return | (2) Promo planning |
| **Regional logistics** | Ưu tiên warehouse/3PL ở rising region (East); min\_order\_value cho free-ship để filter casual | orders \+ geography \+ shipments → revenue per region YoY \+ avg lead\_time (delivery\_date − ship\_date) per region | Giảm lead-time East từ 5 ngày → 3 ngày → tăng conversion trang checkout \~+4% | \#4 Regional growth \+ \#12 Shipping-fee × return | (3) Logistics |
| **Size-guide fix** | Update size chart cho top 3 SKU có wrong\_size return cao nhất; CSKH reach-out trong 48h với review ≤2 | returns (reason='wrong\_size', refund\_amount) \+ products (size, category) \+ reviews (rating) | Giảm 30% wrong\_size → refund\_saved \= N\_wrong × avg\_refund × 0.3 | \#3 Return reason × size \+ \#8 Review→return | (1) Inventory optimization |
| **Promo scheduling** | KHÔNG chạy promo trong tuần Tết \+7 ngày (demand đã peak); target promo vào segment chưa mua 90 ngày | promotions \+ sales \+ VN calendar self-built → uplift % promo vs non-promo trong/ngoài mùa | Tiết kiệm discount cost 100% tuần Tết khi revenue vẫn peak tự nhiên | \#2 Promo ROI \+ \#9 Cannibalization \+ \#10 Seasonality | (2) Promo planning |
| **COD optimization** | Yêu cầu voucher trả trước 5% cho đơn COD trên $M value | orders (payment\_method, order\_status) \+ payments (payment\_value) | Giảm cancel\_rate COD từ 30% → 25% → reclaim $W revenue/năm | \#7 Payment/device behaviour | (2) Promo planning |

*→ Phản chiếu: mỗi hàng ở đây PHẢI có 1 chart EDA tương ứng trong §4.2 \+ 1 feature tương ứng trong §4.3 (nếu relevant). Nếu hàng nào thiếu chart EDA → rơi điểm 'Insight kinh doanh' (thiếu chứng cứ); nếu thiếu feature model → rơi điểm 'Explainability' trong Phần 3\. Dùng audit §4.5 để kiểm tra cross-coverage.*

## **4.5. Dataset coverage matrix**

*→ Audit cuối cùng: cột 'Ý §4.2' chỉ rõ ý nào sẽ 'chạm' đến CSV đó → đảm bảo không CSV nào bị bỏ quên.*

Ma trận 14 CSV × 4 tầng phân tích — giúp team chắc chắn đã 'đụng' đủ dataset trong bài nộp. Ký hiệu: ✓ \= bắt buộc phủ; — \= không cần (file chỉ dùng cho Analytical target).

| CSV | D (What) | Di (Why) | P (Likely) | Pr (Action) | Ý §4.2 phủ |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **products** | ✓ | ✓ | — | ✓ | \#3, \#11 |
| **customers** | ✓ | ✓ | ✓ | ✓ | \#1, \#9 |
| **geography** | ✓ | ✓ | — | ✓ | \#4 |
| **promotions** | — | ✓ | ✓ | ✓ | \#2, \#9, \#10 |
| **orders** | ✓ | ✓ | ✓ | ✓ | \#1, \#4, \#6, \#7, \#9, \#12 |
| **order\_items** | ✓ | ✓ | ✓ | ✓ | \#2, \#3, \#4, \#5, \#9, \#11 |
| **payments** | ✓ | ✓ | — | ✓ | \#7 |
| **shipments** | ✓ | ✓ | — | ✓ | \#4, \#12 |
| **returns** | ✓ | ✓ | — | ✓ | \#3, \#8, \#12 |
| **reviews** | ✓ | ✓ | — | — | \#8 |
| **inventory** | ✓ | ✓ | ✓ | ✓ | \#5 |
| **web\_traffic** | ✓ | ✓ | ✓ | ✓ | \#6 |
| **sales** | ✓ | — | ✓ | ✓ | \#10 \+ nền §4.3 |
| **sample\_submission** | — | — | ✓ | — | — (target format Phần 3\) |

*→ Nếu cột 'Ý §4.2 phủ' của CSV nào rỗng khi đọc bảng này → quay lại §4.2 thêm ý mới hoặc mở rộng ý hiện có. Hiện tại 14/14 CSV có ít nhất 1 ý EDA — ổn để nộp.*

# **5\. Kế hoạch 12 ngày → deadline 2026-05-01**

| Giai đoạn | Ngày | Output | Lead |
| :---- | :---- | :---- | :---- |
| **Re-audit \+ Data audit** | 04-19 → 04-20 | Re-audit PDF ✅; 01\_data\_audit.ipynb (schema, missing, outliers, integrity) | All (Đồng dẫn) |
| **MCQ** | 04-21 | 02\_mcq.ipynb \+ outputs/mcq\_answers.json (verify chéo) | Hiển |
| **EDA Descriptive \+ Diagnostic** | 04-21 → 04-23 | 03\_eda\_descriptive.ipynb — tầng 1-2, 6-8 chart đắt giá (§4.2 ý \#1/\#3/\#4/\#5/\#6/\#7/\#11) | Đồng (Lead Analyst) |
| **EDA Predictive \+ Prescriptive** | 04-24 → 04-26 | 04\_eda\_predictive.ipynb — tầng 3-4, story-led (§4.1) \+ action định lượng (§4.4) | Kiên (Insights Lead) |
| **Feature engineering \+ Model** | 04-27 → 04-29 | 05\_FE.ipynb, 06\_baseline.ipynb, 07\_advanced.ipynb (§4.3 feature blocks) \+ Kaggle submission đầu tiên | Phúc (ML Engineer) |
| **Kaggle iteration \+ Report** | 04-30 | 2-3 Kaggle submission refinement \+ main.tex viết song song (Hiển lay-out, Kiên viết EDA section, Phúc viết Model section) | Phúc \+ Hiển (lead), Kiên hỗ trợ |
| **Finalize \+ GitHub \+ form** | 05-01 | main.pdf ≤4 trang (NeurIPS), README.md, submit form chính thức (§8) | Hiển \+ All |

| Dự phòng: Buffer 1 ngày (05-01 sáng) cho việc submit cuối \+ fix lỗi format PDF/Kaggle. Không lùi deadline nội bộ sang 04-30 trừ khi có rủi ro lớn. Submission Kaggle phải đúng 548 dòng, thứ tự khớp 100% sample\_submission.csv (Kaggle sẽ reject nếu sai format). |
| :---- |
| Rebuild baseline: baseline.ipynb hiện dùng DATA\_DIR='dataset/' — sai path so với folder dataset-datathon-2026-round-1/. Trong giai đoạn 04-27 → 04-29 (ML Engineer), bước đầu tiên là fork baseline sang 06\_model\_baseline.ipynb, sửa DATA\_DIR, re-run end-to-end để xác nhận reproducibility trước khi build LightGBM. |

# **6\. Phân công vai trò (đã chốt 2026-04-19)**

Team đã chốt 4 role. Các section khác trong file này tham chiếu bằng tên role (Lead Analyst / Insights Lead / ML Engineer / Đội trưởng) — xem cột '→ Liên quan' để biết section nào của file phục vụ cho role nào.

| Role | Người | Trách nhiệm chính | Notebook | → Liên quan trong file |
| :---- | :---- | :---- | :---- | :---- |
| **Đội trưởng** | Hiển | Coordinator, MCQ, LaTeX báo cáo, GitHub, submission form, theo deadline. | 02, report/, README | §2.2 (MCQ), §5 (04-21 \+ 04-30 \+ 05-01), §8 (checklist nộp bài) |
| **Lead Analyst** | Đồng | EDA tầng 1-2 (Descriptive \+ Diagnostic), data audit, storytelling nền tảng. | 01\_data\_audit, 03\_eda\_descriptive | §2.3 (tầng D+Di), §3.1–§3.2 (cột đắt \+ bẫy dữ liệu), §4.2 ý \#1/\#3/\#4/\#5/\#6/\#7/\#11 (tag D/Di), §4.5 coverage, §5 (04-19→04-23) |
| **Insights Lead** | Kiên | EDA tầng 3-4 (Predictive \+ Prescriptive), viết insight \+ storytelling cho báo cáo. | 04\_eda\_predictive | §2.3 (tầng P+Pr), §4.1 narrative, §4.2 ý \#2/\#8/\#9/\#10/\#12 (tag P/Pr), §4.4 toàn bộ (KPI \+ impact), §5 (04-24→04-26) |
| **ML Engineer** | Phúc | Feature engineering, baseline, LightGBM, SHAP, Kaggle submissions. | 05\_feature\_engineering, 06\_model\_baseline, 07\_model\_advanced | §2.4 (ràng buộc Phần 3), §3.2 bẫy \#2/\#3/\#5/\#7 (leakage), §4.3 toàn bộ feature blocks, §4.4 cột 'Dự kiến impact' (input cho forecasting), §5 (04-27→04-30), §7 rủi ro leakage/Prophet/RAM |

| Luật review chéo (bắt buộc): (a) Mỗi notebook có cell đầu tiên set SEED=42 \+ in phiên bản pandas/numpy/lightgbm để debug cross-machine. (b) Hiển review MCQ+Report; Đồng review EDA Predictive của Kiên; Kiên review Prescriptive-narrative trong model report của Phúc; Phúc review feature Engineering pipeline của mình \+ audit leakage trên notebook 03/04 trước khi đưa vào model. (c) Trước mỗi deadline nội bộ (§5), 1 thành viên chạy end-to-end trên máy thứ 2 để xác nhận reproducibility. |
| :---- |

# **7\. Rủi ro & mitigation**

| Rủi ro | Tác động | Mitigation |
| :---- | :---- | :---- |
| **RAM laptop không đủ cho orders.csv (44MB) \+ order\_items.csv (23MB)** | Notebook crash khi load full | Khai báo dtype (int32 thay int64, category cho text), dùng chunksize, hoặc move sang Kaggle/Colab. |
| **Prophet auto-load VN holiday → bị coi 'external data'** | Loại Phần 3 (mất 20đ) | KHÔNG dùng Prophet với holidays=... Tự xây VN calendar tĩnh 2012-2024. |
| **Dùng Revenue/COGS 2023+ làm feature (leakage)** | Loại Phần 3 | Anti-leakage checklist CLAUDE.md §9. Code review cross check. Unit test: X\_train.max(Date) \< '2023-01-01'. |
| **web\_traffic / inventory không có cho 2023+** | Mất feature mạnh | 3 option: forecast riêng / rolling proxy / drop. Decide Phase 6 đồng thời cho cả 2 file. |
| **PDF báo cáo ≤4 trang RẤT chặt cho cả EDA \+ Model** | Cắt insight | Plan layout từ tuần 1; ưu tiên 5-6 chart đắt giá nhất \+ bảng tóm tắt; appendix cho phụ. |
| **Repository public → ảnh thẻ SV bị leak nếu commit nhầm** | Vi phạm bảo mật cá nhân | Thêm photos/, .env vào .gitignore. KHÔNG push ảnh thẻ. Upload ảnh riêng qua form. |
| **Screen recording .mov 5GB** | Push fail, repo bloat | Thêm \*.mov vào .gitignore. |
| **Kaggle team chưa merge trước deadline** | Submission không tính cho team | Hiển check ngay 04-19: join competition → team → merge 4 thành viên. |
| **Submission sai format (thiếu cột, sai order)** | Kaggle reject, mất 0 điểm | Assert 548 dòng; assert columns \== \['Date','Revenue','COGS'\]; assert Date order match sample\_submission. |

# **8\. Checklist nộp bài**

Tick từng mục trước khi bấm Submit form (theo PDF page 16):

* Kaggle submission đúng 548 dòng, thứ tự khớp 100% sample\_submission.csv, 3 cột Date/Revenue/COGS.  
* GitHub repo public hoặc invite organizers; README.md có hướng dẫn reproduce đầy đủ \+ requirements.txt \+ SEED=42.  
* Báo cáo PDF ≤4 trang (không tính refs/appendix), template NeurIPS 2025, có link GitHub trong nội dung PDF.  
* Báo cáo có mục Explainability (SHAP / feature importance / PDP) bằng ngôn ngữ business.  
* Báo cáo có section riêng cho EDA (Phần 2\) và Model (Phần 3).  
* Form: đáp án 10 MCQ \+ upload PDF \+ GitHub link \+ Kaggle submission link.  
* Form: ảnh thẻ sinh viên của TẤT CẢ 4 thành viên.  
* Form: tickbox cam kết ≥1 thành viên tham dự Vòng Chung kết 2026-05-23 tại VinUni HN.  
* Random seed \= 42 set consistent ở mọi notebook (np, random, lightgbm random\_state).  
* KHÔNG có Revenue/COGS test set xuất hiện trong feature pipeline (verify bằng assert).  
* KHÔNG dùng dữ liệu/library auto-load external data (Prophet holiday, Yahoo Finance, etc.).  
* Test reproduce end-to-end trên máy thứ 2 ít nhất 1 lần trước deadline.

# **9\. Câu hỏi mở cho cuộc họp đầu tiên**

| ✅ Đã chốt (2026-04-19) \+ re-assign role Phúc↔Kiên (2026-04-21) — chi tiết §6. Hiện tại: Hiển (Đội trưởng) · Đồng (Lead Analyst) · Kiên (Insights Lead — EDA P+Pr) · Phúc (ML Engineer — Model). |
| :---- |

Còn lại — cần thống nhất trong cuộc họp team đầu tiên (04-19 / 04-20):

* **GitHub repo —** Tên repo? Owner account? Public từ đầu hay private rồi public sát deadline?  
* **Kaggle team setup —** Tất cả 4 thành viên đã join competition chưa? Merge team trên Kaggle hay 1 account submit?  
* **Môi trường compute —** Ai dùng laptop? RAM bao nhiêu? Có cần Colab/Kaggle Notebook làm fallback không?  
* **Web traffic test period —** Chọn option (a) self-forecast / (b) rolling mean proxy / (c) bỏ feature?  
* **Inventory test period —** Snapshot dừng 2022-12-31, test 18 tháng không có. Forward-fill 2022-12 hay drop? (Nên quyết cùng lúc với web\_traffic.)  
* **Prophet vs LightGBM —** Có dùng Prophet không (rủi ro external data)? Hay LightGBM-only ngay từ đầu?  
* **Lịch họp —** Họp chốt mỗi mấy ngày (đề xuất: 04-20, 04-23, 04-27, 04-30)?  
* **Template chart —** Chọn matplotlib \+ seaborn hay plotly? Phải đồng nhất style (color palette, title size) — đề xuất seaborn whitegrid \+ colorblind palette.  
* **Evaluation budget Kaggle —** Submission limit/ngày? Lên lịch submit ưu tiên model mạnh nhất, tránh burn limit vào sanity check.

# **Phụ lục — File tham chiếu nội bộ**

| File | Vai trò |
| :---- | :---- |
| **README.md** | Brain file tổng cho Claude sessions — đọc §1–§13 trước khi làm việc. Luôn là source of truth cho dự án. |
| **Đề thi Vòng 1.pdf (2026-04-19)** | Đề chính thức — luôn là nguồn cuối cùng nếu có tranh cãi. Bản cập nhật mới nhất. |
| **Rule\_book.docx** | Quy chế chi tiết, ít chi tiết hơn PDF nhưng có business context. |
| **dataset-datathon-2026-round-1/baseline.ipynb** | Baseline seasonal × growth — dùng làm benchmark tối thiểu. |
| **dataset-datathon-2026-round-1/dataset\_description.docx** | Data dictionary chi tiết — cross-check với PDF §1. |
| **scripts/build\_team\_brief\_v2.py** | Script sinh lại file docx này (reproducible). |

*Tài liệu này là snapshot v2 tại 2026-04-19. Sau cuộc họp đầu, update lại §6 (phân công), §9 (resolved questions), và lưu thành phiên bản v3 nếu cần. Lịch sử thay đổi lớn giữa v1 và v2:*

* Sync sang 14 file CSV (PDF Table 1\) thay vì 15; xoá mention inventory\_enhanced.csv obsolete.  
* Thêm chi tiết methodology cho từng MCQ (phương pháp tính pseudocode).  
* Mở rộng mỗi ý tưởng EDA thành (H) Hypothesis / (T) Test / (A) Action với con số định lượng.  
* Chi tiết hoá feature block model: lag values cụ thể, expanding-window CV folds, SHAP plan.  
* Thêm cột 'Dự kiến impact định lượng' cho toàn bộ Prescriptive recommendations.  
* Thêm bẫy dữ liệu \#7 (inventory monthly snapshot) và nhắc PDF dùng 2 tên cho file train.  
* Timeline đổi sang 12 ngày (từ 04-19) với buffer submit cuối.

# Phần 1 \- 0h 26/04/2026

# Phần 2 \- 0h 26/04/2026

# Phần 3

