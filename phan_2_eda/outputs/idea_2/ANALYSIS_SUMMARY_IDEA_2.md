## 📊 PHÂN TÍCH CHI TIẾT ĐỀ TÀI #2: PROMO ROI DEEP-DIVE
### Incremental Revenue vs Cannibalization

---

## ✅ ANALYSIS COMPLETION CHECKLIST

### ✓ Tầng 1: DESCRIPTIVE (D) - "What happened?"
- [x] Load promotions, orders, order_items, sales cho giai đoạn 2012-2022
- [x] Dựng promo-window calendar theo start_date/end_date
- [x] Tính promo-window lift so với non-promo days
- [x] Tính uplift cho từng campaign (so với window ngay trước campaign)

**Key Finding**:
- 50 campaign được đo lường đầy đủ
- Promo day share: 44.5%
- Promo-window lift tổng thể: **-11.8%**
- Campaign median uplift: **-16.48%**

---

### ✓ Tầng 2: DIAGNOSTIC (Di) - "Why did it happen?"
- [x] So sánh uplift theo promo_type
- [x] Tách top 5 và bottom 5 campaign theo uplift
- [x] Đo cannibalization proxy từ returning customers (<=30d)

**Key Finding**:
- promo_type `percentage` có mean uplift tốt hơn (`+3.26%`) so với `fixed` (`-26.33%`)
- Chỉ 40.0% campaign có uplift dương
- Returning share in promo revenue: 14.4%

---

### ✓ Tầng 3: PREDICTIVE (P) - "What is likely to happen?"
- [x] Fit linear trend giữa `duration_days` và `uplift_pct`
- [x] Dự báo uplift theo độ dài campaign

**Key Finding**:
- Predicted uplift 3-day: 66.85%
- Predicted uplift 7-day: 58.41%
- Predicted uplift 14-day: 43.64%
- Slope: -2.110 pp/day (duration tăng thì uplift giảm)

---

### ✓ Tầng 4: PRESCRIPTIVE (Pr) - "What should we do?"
- [x] Đề xuất khung promo scheduling theo ROI thực tế
- [x] Đề xuất target để giảm cannibalization
- [x] Xây baseline promo scorecard để quyết định scale campaign

**4 Key Recommendations**:

1. **Rút ngắn campaign window**
   - Ưu tiên campaign <=3 ngày
   - Hạn chế campaign >=7 ngày nếu không có bằng chứng uplift dương

2. **Ưu tiên promo_type hiệu quả**
   - Dồn ngân sách theo ROI lịch sử
   - Mặc định `percentage` là nhóm ưu tiên thử nghiệm tiếp

3. **Giảm cannibalization khách cũ**
   - Giới hạn ưu đãi mạnh cho khách vừa mua <=30 ngày
   - Ưu tiên target nhóm dormant >90 ngày

4. **Thiết lập promo scorecard bắt buộc**
   - KPI: uplift%, incremental revenue, returning share
   - Chỉ scale campaign khi đạt ngưỡng KPI tối thiểu

---

## 📁 DELIVERABLES CREATED

### Code & Analysis:
- ✅ `02_Promo_ROI_Complete_Analysis.ipynb` - Notebook phân tích đầy đủ D-Di-P-Pr
- ✅ `IDEA_2_DETAILED_REPORT.md` - Báo cáo chi tiết
- ✅ `ANALYSIS_SUMMARY_IDEA_2.md` - Tóm tắt insight

### Visualizations:
- ✅ `01_revenue_promo_timeline.png`
- ✅ `02_top_bottom_uplift.png`
- ✅ `03_uplift_by_type.png`
- ✅ `04_duration_vs_uplift.png`

### Data Summary:
- ✅ `summary_metrics.csv`

---

## 📊 METRICS SUMMARY TABLE

| Metric | Value | Interpretation |
|--------|-------|-----------------|
| Promo Campaign Count | 50 | Full campaign universe |
| Promo Day Share | 44.5% | Promo xuất hiện gần nửa timeline |
| Promo Window Lift | -11.8% | Promo window tổng thể đang underperform |
| Campaign Mean Uplift | +0.30% | Trung bình gần như neutral |
| Campaign Median Uplift | -16.48% | Đa số campaign kém hiệu quả |
| Positive Campaign Rate | 40.0% | 6/10 campaign không tạo uplift dương |
| Best Campaign Uplift | +78.65% | Có outlier hiệu quả rất cao |
| Worst Campaign Uplift | -36.03% | Có campaign gây suy giảm mạnh |
| Best Promo Type | percentage | Mean uplift tốt nhất |
| Returning Share (Promo Rev) | 14.4% | Cần theo dõi cannibalization |
| Predicted Uplift 3-day | 66.85% | Gợi ý short-window strategy |
| Duration-Uplift Slope | -2.110 pp/day | Duration dài làm giảm uplift |

---

## 🎯 ONE-LINER TAKEAWAY

**"Promo chỉ có giá trị khi tạo demand mới, không phải kéo doanh thu tương lai về hiện tại."**

---

## 🚀 NEXT STEPS

1. A/B test 3-day vs 7-day campaign trên cùng category.
2. Định nghĩa ngưỡng `returning_share` cảnh báo cannibalization.
3. Chuẩn hóa dashboard promo scorecard theo tuần/tháng.
4. Đồng bộ signal promo ROI vào feature engineering Part 3.

---

**Status**: ✅ ANALYSIS COMPLETE & READY FOR PART 2 EDA
