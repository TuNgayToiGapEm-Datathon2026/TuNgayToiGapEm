## PHAN TICH CHI TIET DE TAI #3: RETURN x SIZE x CATEGORY
### Refund Leakage tu ly do wrong_size va top-risk category-size cells

---

## ANALYSIS COMPLETION CHECKLIST

### TANG 1: DESCRIPTIVE (D) - "What happened?"
- [x] Load returns, order_items, products, reviews cho giai doan 2012-2022
- [x] Tong hop return reason distribution va return rate theo size/category
- [x] Dung heatmap return rate theo category x size

Key Finding:
- Tong return lines: 39,939
- Tong refund amount: $510,598,507
- wrong_size chiem 35.0% return lines (ly do lon nhat)
- GenZ la category co return rate cao nhat: 5.72%

---

### TANG 2: DIAGNOSTIC (Di) - "Why did it happen?"
- [x] Phan tich refund leakage theo return reason
- [x] Tim top-risk category-size cells co return rate cao nhat
- [x] Danh gia wrong_size concentration trong Streetwear

Key Finding:
- Wrong-size refund share: 34.6% tong refund
- Streetwear wrong_size share: 35.0%
- Top risk cell: GenZ - XL voi return rate 6.17%

---

### TANG 3: PREDICTIVE (P) - "What is likely to happen?"
- [x] Tao monthly wrong_size trend theo thang
- [x] Fit linear trend de du bao 3 thang toi

Key Finding:
- Forecast wrong_size rate (3M): 34.68%
- Trend slope: -0.000032 per month (gan nhu di ngang, giam rat nhe)

---

### TANG 4: PRESCRIPTIVE (Pr) - "What should we do?"
- [x] Uoc tinh tiet kiem neu giam wrong_size 30%
- [x] De xuat bo khuyen nghi giam return leakage theo cell-level
- [x] De xuat scorecard KPI van hanh return theo thang

4 Key Recommendations:

1. Fix size guide cho top-risk cells
   - Uu tien top 10 category-size co return rate cao nhat
   - Tap trung GenZ va Streetwear voi size risk cao

2. Size advisor tai PDP/Checkout
   - Goi y size dua tren return profile theo category + size
   - Canh bao fit risk cho SKU bat thuong

3. Post-purchase fit confirmation
   - Trigger CSKH som cho don high-risk
   - Giam return truoc khi phat sinh hoan tien

4. Return scorecard bat buoc
   - KPI: wrong_size_share, refund_leakage, top-risk-cell rate
   - Review theo thang de cap nhat size chart va inventory mix

---

## DELIVERABLES CREATED

### Code & Analysis:
- 03_Return_Reason_Size_Complete_Analysis.ipynb - Notebook phan tich day du D-Di-P-Pr
- IDEA_3_DETAILED_REPORT.md - Bao cao chi tiet
- ANALYSIS_SUMMARY_IDEA_3.md - Tom tat insight

### Visualizations:
- 01_return_reason_distribution.png
- 02_category_size_heatmap.png
- 03_wrong_size_trend.png
- 04_refund_by_reason.png

### Data Summary:
- summary_metrics.csv

---

## METRICS SUMMARY TABLE

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Total Return Lines | 39,939 | Quy mo return lines trong du lieu |
| Total Refund Amount | $510,598,507 | Tong leakage tai chinh do returns |
| Wrong-size Share (%) | 35.0% | Ly do return lon nhat |
| Wrong-size Refund Share (%) | 34.6% | Phan refund do wrong_size gay ra |
| Worst Size by Return Rate | S | Size co return rate cao nhat |
| Worst Size Return Rate (%) | 5.65% | Risk level cua size xau nhat |
| Worst Category by Return Rate | GenZ | Category xau nhat theo return rate |
| Worst Category Return Rate (%) | 5.72% | Muc do risk cua category xau nhat |
| Streetwear Wrong-size Share (%) | 35.0% | Wrong-size concentration trong Streetwear |
| Forecast Wrong-size Rate (3M, %) | 34.68% | Du bao ngan han cho wrong_size |
| Trend Slope Wrong-size (per month) | -0.000032 | Trend gan nhu on dinh, giam nhe |
| Est. Savings if Wrong-size -30% | $53,006,160 | Tiem nang tiet kiem neu can thiep dung |

---

## ONE-LINER TAKEAWAY

"Return khong chi la van hanh, do la bai toan fit giua san pham va ky vong khach hang."

---

## NEXT STEPS

1. Thu nghiem A/B size-guide moi tren top-risk category-size cells.
2. Trien khai size advisor rule-based cho GenZ/Streetwear truoc.
3. Theo doi scorecard wrong_size hang thang de danh gia hieu qua can thiep.
4. Dua return-risk features vao model forecasting va demand planning.

---

Status: ANALYSIS COMPLETE & READY FOR PART 2 EDA