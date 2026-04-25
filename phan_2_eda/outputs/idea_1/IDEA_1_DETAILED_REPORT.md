# PHÂN TÍCH CHI TIẾT ĐỀ TÀI #1: CUSTOMER LIFECYCLE & COHORT RETENTION
## Acquisition Channel Quality và bài toán giữ chân khách hàng

---

## 1. EXECUTIVE SUMMARY (ONE-LINER INSIGHT)

**"Acquisition tốt không chỉ mua lần 1, mà phải mua lần 2."**

### Kết quả nổi bật:
- 90,246 / 121,930 khách đã mua hàng (74.0%)
- Repeat buyers đạt 75.2%, nhưng retention ngắn hạn còn thấp (30D: 8.2%)
- 90D retention toàn cục: 17.6%, 180D retention: 27.4%
- social_media đang nhỉnh hơn paid_search về retention 90D (18.0% vs 17.4%)
- Pool re-engagement rất lớn: 22,175 dormant one-time buyers (>90 ngày)

---

## 2. TẦNG 1: DESCRIPTIVE ("What happened?")

### 2.1 Dataset Coverage

- Customers: 121,930 dòng
- Orders: 646,945 dòng
- Khoảng thời gian orders: 2012-07-04 đến 2022-12-31

### 2.2 Lifecycle Funnel

| Metric | Value |
|-------|-------|
| Total Customers | 121,930 |
| Buyers | 90,246 |
| Buyer Conversion | 74.0% |
| Repeat Buyers | 67,888 |
| Repeat Rate (on buyers) | 75.2% |

### 2.3 Retention Windows

| Retention Window | Rate |
|------------------|------|
| 30D | 8.2% |
| 90D | 17.6% |
| 180D | 27.4% |

**Nhận xét**:
- Sau mua lần đầu, tỷ lệ quay lại trong 30 ngày tương đối thấp.
- Retention tích lũy tăng theo thời gian, cho thấy vẫn có cơ hội nuôi dưỡng vòng đời nếu chăm sóc đúng thời điểm.

---

## 3. TẦNG 2: DIAGNOSTIC ("Why did it happen?")

### 3.1 Channel Quality Comparison

| Channel | 90D Retention | Repeat Signal |
|---------|---------------|---------------|
| organic_search | 17.8% | tốt |
| social_media | 18.0% | tốt |
| paid_search | 17.4% | trung bình |
| email_campaign | 17.6% | trung bình |
| referral | 16.8% | thấp hơn |
| direct | 17.4% | thấp hơn |

### 3.2 Hypothesis Check

Giả thuyết ban đầu: **paid_search retention > social_media**.

Kết quả thực tế:
- paid_search 90D retention: 17.4%
- social_media 90D retention: 18.0%
- Ratio paid/social: **0.96x**

**Kết luận**: trong data hiện tại, giả thuyết không được ủng hộ.

### 3.3 Behavioral Diagnostic

Từ scatter recency vs total orders:
- Nhóm khách có recency lớn và total_orders=1 chiếm tỷ lệ đáng kể.
- Đây là nhóm có khả năng "churn mềm" và phù hợp cho chiến dịch re-engagement theo trigger thời gian.

---

## 4. TẦNG 3: PREDICTIVE ("What is likely to happen?")

### 4.1 Cohort Pattern

- Cohort retention giảm rất nhanh sau tháng đầu.
- Sau đó retention đi vào vùng thấp nhưng ổn định.

### 4.2 Short-term Retention Forecast

Dùng linear trend trên cohort retention tại cohort_index=3 gần nhất:
- Forecast retention index-3: **0.9%**

**Diễn giải**:
- Nếu không có can thiệp, xác suất cải thiện tự nhiên trong ngắn hạn là thấp.
- Do đó cần giải pháp chủ động ở mốc 30/60/90 ngày.

---

## 5. TẦNG 4: PRESCRIPTIVE ("What should we do?")

### 5.1 Action 1 — Budget theo Channel Quality

**Vấn đề**: tối ưu marketing theo traffic/CPA dễ bỏ qua chất lượng giữ chân.

**Hành động**:
- Dùng thêm retention 90D như KPI bắt buộc khi scale budget.
- Giảm phụ thuộc vào chỉ số bề mặt (sessions, CTR, CPA).

### 5.2 Action 2 — 90-Day Re-engagement Flow

**Đối tượng**: 22,175 dormant one-time buyers (>90 ngày).

**Giả định**:
- Reactivation rate: 12%
- Khách quay lại ước tính: 2,661
- Value proxy ước tính: **$67,581,476**

**Ý nghĩa**: đây là "low-hanging fruit" lớn nhất của idea 1.

### 5.3 Action 3 — Welcome Journey theo từng Channel

- Paid/search: đẩy bundle và loyalty ngay sau đơn thứ 2.
- Social: incentive sớm 7 ngày + giảm friction (size guide, gợi ý sản phẩm).

### 5.4 Action 4 — Thêm Retention vào Marketing Scorecard

- Theo dõi KPI: 30D/90D retention theo channel.
- Dừng scale channel có first-to-second-order conversion thấp.

---

## 6. VISUAL OUTPUTS

1. `01_cohort_heatmap.png`: ma trận retention theo cohort tháng.
2. `02_channel_retention.png`: retention 90D và repeat rate theo channel.
3. `03_retention_curve.png`: retention decay curve cho top channels.
4. `04_recency_repeat_scatter.png`: phân bố recency và số đơn.
5. `summary_metrics.csv`: bảng chỉ số tổng hợp.

---

## 7. KẾT LUẬN KINH DOANH

- Trọng tâm của idea 1 không phải mua thêm khách mới, mà là tối ưu chuyển đổi từ mua lần 1 sang mua lần 2.
- Retention ngắn hạn thấp cho thấy cần chiến lược lifecycle-based marketing thay vì campaign-based marketing.
- Tập dormant one-time buyers đủ lớn để tạo uplift đáng kể nếu triển khai re-engagement đúng cách.

---

## 8. NEXT EXPERIMENTS

1. A/B test re-engagement 90 ngày trên social_media cohort.
2. So sánh hiệu quả incentive 7 ngày vs 14 ngày cho first-time buyers.
3. Bổ sung feature retention vào mô hình Part 3 để đo tác động gián tiếp tới doanh thu.

---

**Generated**: 2026-04-24
**Status**: ✅ Ready for Part 2 EDA integration
