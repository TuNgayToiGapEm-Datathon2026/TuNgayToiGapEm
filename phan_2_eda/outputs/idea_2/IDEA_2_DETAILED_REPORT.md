# PHÂN TÍCH CHI TIẾT ĐỀ TÀI #2: PROMO ROI DEEP-DIVE
## Incremental Revenue vs Cannibalization trong 50 chiến dịch khuyến mãi

---

## 1. EXECUTIVE SUMMARY (ONE-LINER INSIGHT)

**"Promo chỉ có giá trị khi tạo demand mới, không phải kéo doanh thu tương lai về hiện tại."**

### Kết quả trọng tâm:
- Promo xuất hiện 44.5% số ngày trong lịch sử dữ liệu.
- Doanh thu trung bình trong promo-window thấp hơn non-promo (**-11.8%**).
- Mean uplift campaign gần như bằng 0 (**+0.30%**), median âm mạnh (**-16.48%**).
- Chỉ 40% campaign có uplift dương.
- Campaign duration dài có xu hướng làm giảm uplift (slope **-2.110 pp/day**).

---

## 2. TẦNG 1: DESCRIPTIVE ("What happened?")

### 2.1 Data Scope

- Promotions: 50 campaigns
- Orders: 646,945
- Order items: 714,669
- Sales daily: 3,833 ngày

### 2.2 Promo Exposure

| Metric | Value |
|-------|-------|
| Promo Day Share | 44.5% |
| Promo Window Lift | -11.8% |

**Diễn giải**:
- Tần suất promo cao nhưng hiệu quả tổng thể không tương xứng.
- Cần đánh giá campaign-level thay vì nhìn tổng volume khuyến mãi.

### 2.3 Campaign Uplift Distribution

| Metric | Value |
|-------|-------|
| Mean Uplift | +0.30% |
| Median Uplift | -16.48% |
| Positive Campaign Rate | 40.0% |
| Best Campaign | +78.65% |
| Worst Campaign | -36.03% |

**Diễn giải**:
- Có một số campaign rất tốt, nhưng phần lớn campaign dưới baseline.
- Hệ thống hiện tại thiếu cơ chế “chỉ scale thứ đã chứng minh hiệu quả”.

---

## 3. TẦNG 2: DIAGNOSTIC ("Why did it happen?")

### 3.1 Promo Type Performance

| Promo Type | Mean Uplift | Median Uplift |
|-----------|-------------|----------------|
| percentage | +3.26% | -14.95% |
| fixed | -26.33% | -25.17% |

**Diễn giải**:
- `percentage` có kỳ vọng tốt hơn `fixed` trong bộ dữ liệu này.
- `fixed` có dấu hiệu underperform nhất quán.

### 3.2 Cannibalization Proxy

- Returning share in promo revenue (khách quay lại <=30 ngày): **14.4%**.

**Diễn giải**:
- Tỷ trọng này chưa cực cao nhưng đủ để cảnh báo risk “discount cho khách vốn đã có khả năng mua lại”.
- Cần thêm rule segmentation để tránh bào mòn biên lợi nhuận không cần thiết.

---

## 4. TẦNG 3: PREDICTIVE ("What is likely to happen?")

Mô hình tuyến tính đơn giản giữa `duration_days` và `uplift_pct` cho kết quả:

- Predicted uplift (3-day): **66.85%**
- Predicted uplift (7-day): **58.41%**
- Predicted uplift (14-day): **43.64%**
- Duration-Uplift slope: **-2.110 pp/day**

**Kết luận predictive**:
- Campaign càng kéo dài càng làm giảm độ sắc của uplift.
- Short-window promo có xác suất tạo kết quả tốt hơn (đặc biệt khi gắn urgency).

---

## 5. TẦNG 4: PRESCRIPTIVE ("What should we do?")

### 5.1 Action 1 — Short-window First

- Mặc định khung 3 ngày cho campaign mới.
- Campaign 7+ ngày chỉ chạy khi có hypothesis rõ và guardrail KPI.

### 5.2 Action 2 — Type-level Budget Allocation

- Ưu tiên promo_type có hiệu suất lịch sử tốt (`percentage`).
- Giảm tỷ trọng `fixed` cho đến khi chứng minh ROI dương ổn định.

### 5.3 Action 3 — Cannibalization Control

- Giới hạn ưu đãi mạnh cho khách vừa mua gần đây (<=30 ngày).
- Dịch chuyển ưu đãi sang nhóm dormant / near-churn để tạo incremental demand.

### 5.4 Action 4 — Promo Scorecard Governance

Thiết lập KPI bắt buộc trước khi scale:
1. `uplift_pct`
2. `incremental_revenue` (so baseline window)
3. `returning_share_in_promo_revenue`

Campaign không đạt ngưỡng KPI => không scale.

---

## 6. VISUAL OUTPUTS

1. `01_revenue_promo_timeline.png` — Doanh thu theo ngày + overlay promo-window.
2. `02_top_bottom_uplift.png` — So sánh top 5 vs bottom 5 campaign.
3. `03_uplift_by_type.png` — Boxplot uplift theo promo_type.
4. `04_duration_vs_uplift.png` — Tương quan duration và uplift.
5. `summary_metrics.csv` — Bảng KPI tổng hợp.

---

## 7. KẾT LUẬN KINH DOANH

- Chạy promo thường xuyên không đồng nghĩa tạo tăng trưởng.
- Chất lượng thiết kế campaign (duration, type, target) quan trọng hơn số lượng campaign.
- Đòn bẩy lớn nhất hiện tại: chuyển từ “promo theo lịch” sang “promo theo incremental logic”.

---

## 8. NEXT EXPERIMENTS

1. A/B test `percentage` vs `fixed` cùng tệp khách và cùng thời gian.
2. A/B test 3 ngày vs 7 ngày để đo uplift thực tế và margin impact.
3. Xây “campaign pre-check” tự động trước khi launch (dựa trên scorecard).
4. Kết nối output promo ROI vào feature block của forecasting model.

---

**Generated**: 2026-04-24
**Status**: ✅ Ready for Part 2 EDA integration
