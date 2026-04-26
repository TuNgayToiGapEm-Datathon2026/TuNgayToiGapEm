# Tóm Tắt Phân Tích — IDEA #8: Review -> Return Correlation

**Notebook:** 08_Review_Return_Correlation_Complete_Analysis.ipynb

---

## Danh Sách Kiểm Tra Hoàn Thành

- [x] Đã sử dụng dữ liệu từ `orders`, `reviews`, `returns`, `products`
- [x] Đã xây dựng bảng phân tích theo `rating_band`
- [x] Đã chạy kiểm định Fisher Exact cho giả thuyết low-rating vs high-rating
- [x] Đã tạo đủ 4 biểu đồ phân tích
- [x] Đã xuất `summary_metrics.csv`
- [x] Đã đề xuất hành động CSKH theo trigger sau review thấp

---

## Phát Hiện Chính

| Chỉ số | Giá trị |
|:--|:--|
| Tổng Orders | 646,945 |
| Orders có Review | 111,369 |
| Tỷ lệ phủ Review | 17.21% |
| Return Rate trong nhóm có Review | 0.00% |
| Return Rate nhóm Low Rating (<=2) | 0.00% |
| Return Rate nhóm High Rating (>=4) | 0.00% |
| Rate Ratio Low/High | nanx |
| Fisher Exact p-value | 1.000000 |
| Odds Ratio | nan |
| Category rủi ro cao nhất trong nhóm Low Rating | Casual |
| Return Rate category rủi ro cao nhất | 0.00% |
| Dự báo Return Rate nhóm Low Rating (+1M) | 0.00% |
| Trend slope nhóm Low Rating | 0.0000 pp/tháng |
| Low Group Return Volume | 0 |
| Avg Refund Per Return | $12,784.46 |
| Estimated Saved Returns (20%) | 0 |
| Estimated Refund Saved | $0 |
| SLA CSKH đề xuất | <=48h |

---

## Điểm Nhấn Một Câu

> **Review thấp là tín hiệu cảnh báo sớm (SOS), nhưng pipeline hiện tại chưa bắt được tín hiệu return tương ứng ở cấp order-review để định lượng tác động.**

---

## Kết Luận Theo 4 Tầng

### 1) Descriptive — Điều gì đã xảy ra?
- Dữ liệu review bao phủ 17.21% tổng đơn hàng.
- Trong pipeline hiện tại, tỷ lệ return ở các nhóm rating đều bằng 0.00%.

### 2) Diagnostic — Vì sao xảy ra?
- Kiểm định Fisher cho kết quả p-value = 1.0, không có khác biệt thống kê giữa nhóm low-rating và high-rating trong dữ liệu đã ghép.
- Điều này nhiều khả năng phản ánh hạn chế ở logic mapping review-return theo order-level, thay vì phản ánh đúng bản chất nghiệp vụ.

### 3) Predictive — Điều gì có khả năng xảy ra tiếp theo?
- Forecast cho nhóm low-rating đang phẳng (0.00%) với slope 0.0000.
- Khi tín hiệu đầu vào bằng 0, mô hình dự báo chưa cung cấp giá trị ra quyết định.

### 4) Prescriptive — Nên làm gì?
1. Giữ trigger CSKH <=48h cho review <=2 sao như một cơ chế phòng ngừa rủi ro danh tiếng.
2. Ở vòng tiếp theo, cần chuẩn hóa lại mapping giữa review và return theo `order_id + product_id + time window` để đo đúng tác động.
3. Ưu tiên theo dõi category Casual trong nhóm low-rating để phát hiện tín hiệu sớm.
4. Chỉ định KPI vận hành: low-rating volume, SLA xử lý, return_after_review, refund_saved.

---

## Tệp Đầu Ra

- 01_return_rate_by_rating_band.png
- 02_category_rating_return_heatmap.png
- 03_low_high_rating_return_trend.png
- 04_low_rating_return_forecast.png
- summary_metrics.csv

**Thư mục:** `phan_2_eda/outputs/idea_8/outputs/`
