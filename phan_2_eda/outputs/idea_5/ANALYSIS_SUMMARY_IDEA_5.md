# Tóm Tắt Phân Tích — IDEA #5: Hiệu Suất Theo Danh Mục Sản Phẩm

**Notebook:** `05_Product_Category_Performance_Complete_Analysis.ipynb`

---

## ✅ Danh Sách Kiểm Tra Phân Tích

- [x] Đã tải dữ liệu: products, order_items, orders, returns
- [x] Đã xây dựng bảng doanh thu danh mục kèm margin và return metrics
- [x] Phân tích Descriptive: xếp hạng danh mục và phân bố margin
- [x] Phân tích Diagnostic: ma trận lợi nhuận và efficiency score
- [x] Phân tích Predictive: dự báo doanh thu danh mục dẫn đầu (3 tháng)
- [x] Đã tạo 4 biểu đồ (ranking, scatter, so sánh, trend + forecast)
- [x] Đã xuất bảng chỉ số tổng hợp ra CSV
- [x] Đã hoàn thiện khuyến nghị Prescriptive

---

## 🎯 Phát Hiện Chính

| Metric | Value |
|:-------|:------|
| **Total Revenue** | $15.68B |
| **Total Gross Profit** | $1.52B |
| **Overall Margin** | 9.68% |
| **Total Orders** | 650,651 |
| **Average Order Value** | $24,100 |
| **Overall Return Rate** | 1.24% |
| **Số Danh Mục Phân Tích** | 4 (Streetwear, Outdoor, Casual, GenZ) |
| **Top Category** | Streetwear: $12.56B (80.1% share) |
| **Highest Margin Category** | GenZ: 15.47% |
| **Lowest Margin Category** | Casual: 7.66% |
| **Biên Cơ Hội Margin** | 7.80 điểm phần trăm |
| **Top Category Forecast (M+1)** | $71.7M |
| **Xu Hướng Danh Mục Dẫn Đầu** | -$440,085/tháng |
| **Best Efficiency** | Streetwear (score: 6.20) |
| **Worst Efficiency** | Casual (score: -0.99) |
| **Tổng Refund** | $510.6M |

---

## 💡 Điểm Nhấn Một Câu

> **"Hiệu suất danh mục = quy mô doanh thu + tối ưu margin, là con đường đến tối ưu lợi nhuận."**

Mức tập trung doanh thu ở Streetwear (80.1%) đi cùng chênh lệch margin lớn (7.80 điểm %) tạo ra cơ hội tối ưu kép: vừa mở rộng nhóm danh mục có biên tốt, vừa nâng hiệu suất nhóm đang yếu bằng pricing và product mix.

---

## 📊 Ma Trận Xếp Hạng Danh Mục

### **Các Tầng Hiệu Suất**

**🏆 Nhóm Star (Doanh thu cao + Margin cao)**
- _GenZ_: 2.1% doanh thu, **15.47% margin** (cao nhất) — định vị premium đang hiệu quả

**💰 Nhóm Cash Cow (Doanh thu cao, Margin trung bình)**
- _Streetwear_: 80.1% doanh thu, 9.28% margin — động cơ sản lượng; cần tối ưu biên
- _Outdoor_: 15.0% doanh thu, **11.35% margin** (cao thứ hai) — nhóm cân bằng tốt

**⚠️ Nhóm Cần Xử Lý (Doanh thu thấp, Margin thấp)**
- _Casual_: 2.8% doanh thu, **7.66% margin** (thấp nhất) — efficiency score -0.99; cần đổi chiến lược

---

## 🔍 Phân Tích Chẩn Đoán Chuyên Sâu

**Phân tích lợi nhuận:**
- Dẫn đầu gross profit: **Streetwear** ($1.17B), nhưng chủ yếu nhờ quy mô hơn là biên
- Dẫn đầu margin: **GenZ** (15.47%), hiệu quả cao hơn tỷ trọng doanh thu
- Tụt hậu margin: **Casual** (7.66%), có thể tăng thêm $34.4M nếu đạt biên ngang GenZ

**Efficiency Scorecard** (margin % × revenue share - return rate):
1. **Streetwear**: +6.20 (dominant scale + acceptable margin)
2. **Outdoor**: +0.72 (balanced; good margin but smaller share)
3. **GenZ**: +0.24 (high margin but small revenue share)
4. **Casual**: -0.99 (weak efficiency; low margin eats revenue contribution)

---

## 📈 Triển Vọng Dự Báo

**Dự báo doanh thu danh mục dẫn đầu (Streetwear):**
- Bình quân tháng hiện tại: $31.1M
- Tháng +1: $71.7M (đỉnh dự báo, khả năng do mùa vụ/promo)
- Tháng +2: $71.3M
- Tháng +3: $70.8M
- **Độ dốc xu hướng**: -$440,085/tháng (giảm nhẹ sau đỉnh)

**Hàm ý:** Streetwear có đỉnh theo mùa vụ hoặc chiến dịch; run-rate bền vững nhiều khả năng quanh vùng $70-71M/tháng.

---

## 🚀 Khuyến Nghị Hành Động

**1. ƯU TIÊN DANH MỤC**
   - **Bảo vệ và mở rộng Streetwear**: duy trì vận hành tốt, tập trung phục hồi margin (9.28% so với 15.47% của GenZ)
   - **Đẩy mạnh GenZ**: định vị premium biên cao đã được chứng minh; mở rộng danh mục và đầu tư marketing
   - **Tái cấu trúc Casual**: phân tích nguyên nhân margin thấp 7.66% so với 15.47% của GenZ

**2. TỐI ƯU MARGIN**
   - **Mục tiêu nâng Casual**: nếu Casual đạt 15.47%, phần tăng gross profit ước tính = $34.4M
   - **Chiến lược giá**: rà soát định vị cạnh tranh; cân nhắc tái định vị premium/value line
   - **Hiệu quả chi phí**: tìm cơ hội giảm COGS ở nhóm margin thấp

**3. TỐI ƯU CƠ CẤU TỒN KHO**
   - **Nhóm bán nhanh, biên cao (GenZ)**: tăng độ sâu SKU và phân bổ vốn lưu động
   - **Nhóm quy mô lớn (Streetwear)**: tối ưu tốc độ quay vòng tồn kho, không chỉ nhìn mỗi margin
   - **Nhóm yếu (Casual)**: điều chỉnh phân bổ tồn kho theo kết quả tái cấu trúc

**4. SCORECARD QUẢN TRỊ DANH MỤC**
   - **KPI hàng tháng**: Revenue trend, margin %, return rate, efficiency score
   - **Rà soát hàng quý**: điều chỉnh chiến lược, lịch khuyến mãi, mục tiêu margin
   - **Đánh giá hàng năm**: sức khỏe danh mục và quyết định hợp nhất/thoái nhóm kém hiệu quả

---

## 📂 Tệp Đầu Ra

**Các tệp đã tạo:**
- ✓ `01_category_revenue_ranking.png` — Top 15 danh mục theo doanh thu  
- ✓ `02_margin_vs_revenue_scatter.png` — Bubble chart margin theo doanh thu (kích thước = return rate)  
- ✓ `03_top_bottom_categories_comparison.png` — So sánh side-by-side doanh thu và margin  
- ✓ `04_top_category_trend_forecast.png` — Xu hướng Streetwear theo tháng + dự báo 3 tháng  
- ✓ `summary_metrics.csv` — File 20 chỉ số cho dashboard  

**Location:** `phan_2_eda/outputs/idea_5/outputs/`

---

## ✨ Bước Tiếp Theo

1. **Chốt định hướng với ban điều hành**: trình bày category matrix cho đội product và finance
2. **Đào sâu Casual**: phân tích nguyên nhân gốc của khoảng cách margin
3. **Rà soát pricing**: benchmark giá premium của GenZ so với Casual/Outdoor
4. **Xác thực dự báo**: kiểm tra yếu tố mùa vụ và xu hướng với đội demand/supply
5. **Dựng dashboard vận hành**: scorecard danh mục theo tháng

---

_Phân tích hoàn thành theo khung D-Di-P-Pr: Descriptive (tổng quan danh mục) → Diagnostic (động lực lợi nhuận) → Predictive (dự báo) → Prescriptive (chiến lược hành động)._
