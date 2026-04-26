# Tóm Tắt Phân Tích — IDEA #6: Web Traffic Funnel

**Notebook:** `06_Web_Traffic_Funnel_Complete_Analysis.ipynb`

---

## Danh Sách Kiểm Tra Hoàn Thành

- [x] Đã tải dữ liệu từ `web_traffic`, `orders`, `order_items`
- [x] Đã xây dựng bảng funnel theo ngày và source
- [x] Hoàn thành phân tích 4 tầng D-Di-P-Pr
- [x] Đã tạo 4 biểu đồ theo đúng cấu trúc
- [x] Đã xuất bảng chỉ số tổng hợp `summary_metrics.csv`
- [x] Đã hoàn thiện khuyến nghị hành động theo kênh

---

## Phát Hiện Chính

| Chỉ số | Giá trị |
|:--|:--|
| Tổng Sessions | 91,452,537 |
| Tổng Orders | 121,586 |
| Tổng Revenue | $2,947,636,902 |
| Conversion Proxy Toàn Kênh | 0.1329% |
| AOV Toàn Kênh | $24,243.23 |
| Revenue per Session Toàn Kênh | $32.23 |
| Số Nguồn Traffic | 6 |
| Nguồn Dẫn Đầu Theo Revenue | organic_search |
| Revenue Nguồn Dẫn Đầu | $1,214,210,252 |
| Conversion Nguồn Dẫn Đầu | 0.1858% |
| Bounce Rate Nguồn Dẫn Đầu | 0.45% |
| Nguồn RPS Cao Nhất | organic_search ($44.65/session) |
| Nguồn Kém Hiệu Quả Nhất | direct |
| Dự Báo Revenue +1 Tháng (Nguồn Dẫn Đầu) | $6,885,156 |
| Độ Dốc Xu Hướng | -$53,442/tháng |
| Doanh Thu Gia Tăng Ước Tính (Dịch Chuyển Ngân Sách) | $8,655,831 |

---

## Điểm Nhấn Một Câu

> **Bounce cao không đồng nghĩa hiệu quả thấp; cần tối ưu theo conversion × AOV và revenue/session thay vì chỉ nhìn traffic volume.**

---

## Kết Luận Theo 4 Tầng

### 1) Descriptive — Điều gì đã xảy ra?
- organic_search dẫn đầu cả doanh thu, conversion và revenue/session.
- paid_search và social_media theo sau, nhưng hiệu suất vẫn thấp hơn organic_search.
- direct là kênh có hiệu suất thấp nhất trong bộ dữ liệu hiện tại.

### 2) Diagnostic — Vì sao xảy ra?
- Chênh lệch hiệu suất đến từ chất lượng traffic (ý định mua), không chỉ từ số phiên.
- So sánh điển hình: paid_search cao hơn social_media khoảng 8.1% theo revenue/session.
- Kênh có bounce không nhất thiết kém nếu vẫn chuyển đổi và tạo giá trị đơn hàng tốt.

### 3) Predictive — Điều gì có khả năng xảy ra tiếp theo?
- Nguồn top (`organic_search`) được dự báo tháng tới khoảng $6.89M.
- Xu hướng ngắn hạn giảm nhẹ: -$53,442/tháng.
- Hàm ý: cần can thiệp tối ưu thông điệp/khuyến mãi để giữ đà doanh thu.

### 4) Prescriptive — Nên làm gì?
1. Dịch chuyển 20% ngân sách từ kênh yếu sang kênh hiệu quả cao.
2. Đổi KPI chính từ sessions sang bộ chỉ số `conversion proxy`, `AOV`, `revenue/session`.
3. Tách chiến dịch theo ý định mua: nhóm high intent tập trung chốt đơn, nhóm low intent tập trung nurture.
4. Duy trì scorecard theo tháng cho từng source để tái phân bổ ngân sách liên tục.

---

## Tệp Đầu Ra

- `01_source_revenue_ranking.png`
- `02_bounce_vs_conversion_scatter.png`
- `03_top3_conversion_trend.png`
- `04_top_source_revenue_forecast.png`
- `summary_metrics.csv`

**Thư mục:** `phan_2_eda/outputs/idea_6/outputs/`
