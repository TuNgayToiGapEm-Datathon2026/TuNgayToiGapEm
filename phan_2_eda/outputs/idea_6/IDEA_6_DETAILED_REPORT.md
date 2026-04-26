# Báo Cáo Chi Tiết — IDEA #6: Phân Tích Web Traffic Funnel

**Notebook:** `06_Web_Traffic_Funnel_Complete_Analysis.ipynb`  
**Phạm vi dữ liệu:** web_traffic + orders + order_items (giai đoạn dữ liệu lịch sử)

---

## 1. Tóm Tắt Điều Hành

Phân tích funnel theo nguồn traffic cho thấy khác biệt hiệu suất giữa các kênh là đáng kể, dù cùng đóng góp vào tổng traffic. Nguồn `organic_search` dẫn đầu toàn diện về doanh thu, conversion proxy và revenue/session. Trong khi đó, `direct` là điểm nghẽn hiệu suất. Kết quả khẳng định cần dịch chuyển cách đo lường marketing từ “volume sessions” sang “giá trị mỗi phiên”.

**Thông điệp cốt lõi:** Bounce rate chỉ là tín hiệu hành vi, không phải KPI quyết định ngân sách khi đứng một mình.

---

## 2. Tầng 1 — Descriptive (Điều gì đã xảy ra?)

### 2.1 Tổng quan funnel toàn hệ thống
- Tổng sessions: 91,452,537
- Tổng orders: 121,586
- Tổng revenue: $2,947,636,902
- Conversion proxy toàn kênh: 0.1329%
- AOV toàn kênh: $24,243.23
- Revenue/session toàn kênh: $32.23

### 2.2 Cấu trúc theo nguồn traffic
- Tổng số nguồn: 6
- Nguồn dẫn đầu theo doanh thu: `organic_search` ($1.214B)
- Các nguồn tiếp theo: `paid_search`, `social_media`, `email_campaign`, `referral`, `direct`

Nhận định: hệ thống có mức tập trung giá trị cao ở nhóm nguồn có ý định tìm kiếm rõ (search-driven).

---

## 3. Tầng 2 — Diagnostic (Vì sao xảy ra?)

### 3.1 Khác biệt hiệu suất giữa các nguồn
- Nguồn có revenue/session cao nhất: `organic_search` ($44.65/session)
- Nguồn có conversion cao nhất: `organic_search` (0.1858%)
- Nguồn kém hiệu quả nhất theo score: `direct`

### 3.2 Kiểm tra giả thuyết paid_search vs social_media
- `paid_search` cao hơn `social_media` khoảng 8.1% theo revenue/session
- Điều này gợi ý chất lượng traffic từ paid_search có khả năng chốt đơn tốt hơn trong dữ liệu hiện tại

### 3.3 Kết luận chẩn đoán
- Sự khác biệt không chỉ do lượng truy cập, mà chủ yếu do **chất lượng phiên** và **ý định mua**.
- Bounce rate không đủ đại diện cho hiệu quả kinh doanh nếu tách khỏi conversion và AOV.

---

## 4. Tầng 3 — Predictive (Điều gì có khả năng xảy ra?)

Dựa trên chuỗi theo tháng của nguồn dẫn đầu (`organic_search`):
- Dự báo doanh thu +1 tháng: $6,885,156
- Độ dốc xu hướng: -$53,442/tháng

Diễn giải:
- Nguồn dẫn đầu vẫn là trụ cột doanh thu, nhưng xu hướng ngắn hạn có dấu hiệu giảm nhẹ.
- Nếu không có hành động tối ưu thông điệp, trải nghiệm landing, và phân bổ ngân sách, hiệu quả có thể suy giảm theo thời gian.

---

## 5. Tầng 4 — Prescriptive (Nên làm gì?)

### 5.1 Tối ưu phân bổ ngân sách kênh
- Đề xuất dịch chuyển 20% ngân sách từ nguồn kém hiệu quả sang nguồn hiệu quả cao.
- Tác động doanh thu ước tính: **+$8,655,831** mỗi chu kỳ tối ưu.

### 5.2 Chuẩn hóa KPI marketing mới
Bộ KPI trọng tâm nên gồm:
1. Conversion proxy
2. AOV
3. Revenue per session
4. Bounce rate (chỉ dùng như chỉ báo phụ)

### 5.3 Tách chiến lược theo ý định mua
- Nhóm high-intent: thông điệp chốt đơn nhanh, CTA rõ.
- Nhóm low-intent: content nuôi dưỡng, retargeting theo hành vi.

### 5.4 Scorecard vận hành theo tháng
Mỗi source cần theo dõi cố định:
- sessions
- conversion proxy
- AOV
- revenue/session
- bounce_rate

---

## 6. Hệ Thống Biểu Đồ Đầu Ra

1. `01_source_revenue_ranking.png`: Xếp hạng doanh thu theo source.
2. `02_bounce_vs_conversion_scatter.png`: Quan hệ bounce và conversion theo nguồn.
3. `03_top3_conversion_trend.png`: Xu hướng conversion theo tháng của top 3 nguồn.
4. `04_top_source_revenue_forecast.png`: Dự báo 3 tháng cho nguồn dẫn đầu.
5. `summary_metrics.csv`: Bảng chỉ số tổng hợp phục vụ dashboard.

---

## 7. Kết Luận Kinh Doanh

Idea 6 chứng minh rằng hiệu suất marketing không thể đo bằng traffic volume đơn thuần. Nguồn tạo ra giá trị cao (revenue/session tốt, conversion tốt) mới là nơi nên ưu tiên ngân sách. Trong bối cảnh xu hướng nguồn dẫn đầu đang giảm nhẹ, việc tái phân bổ ngân sách theo hiệu quả thực và áp dụng scorecard theo tháng là bước hành động cần triển khai ngay.

**Mục tiêu sau triển khai:** tăng doanh thu biên từ tối ưu channel mix, đồng thời giảm lãng phí ngân sách ở nguồn traffic hiệu suất thấp.
