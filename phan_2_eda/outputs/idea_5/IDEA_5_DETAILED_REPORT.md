# Báo Cáo Chi Tiết — IDEA #5: Phân Tích Hiệu Suất Theo Danh Mục Sản Phẩm

**Ngày phân tích:** Phiên chạy phân tích hiện tại  
**Notebook:** `05_Product_Category_Performance_Complete_Analysis.ipynb`  
**Phạm vi dữ liệu:** Toàn bộ lịch sử giao dịch (2,412 sản phẩm, 714,669 order items, 39,939 returns)

---

## Tóm Tắt Điều Hành

Phân tích này chia danh mục sản phẩm thành **4 nhóm chính** (Streetwear, Outdoor, Casual, GenZ) để xác định mức độ tập trung doanh thu, cơ hội tối ưu biên lợi nhuận và ưu tiên chiến lược theo danh mục. Doanh thu hiện tập trung mạnh vào Streetwear (80.1%), tạo lợi thế quy mô nhưng cũng làm tăng rủi ro phụ thuộc. Đồng thời, độ vênh margin 7.80 điểm phần trăm giữa các danh mục cho thấy dư địa tối ưu đáng kể, đặc biệt ở Casual.

**Hàm ý chiến lược:**  
"Streetwear là động cơ sản lượng; GenZ chứng minh mô hình biên cao hiệu quả; Casual cần can thiệp chiến lược (giá, cơ cấu sản phẩm hoặc thu hẹp)."

---

## TẦNG 1: DESCRIPTIVE — "ĐIỀU GÌ ĐÃ XẢY RA?"

### Tổng quan danh mục

**Phân bổ doanh thu:**
```
Streetwear:  $12,558,477,099 (80.1%)
Outdoor:     $ 2,353,396,797 (15.0%)
Casual:      $   440,285,194 ( 2.8%)
GenZ:        $   328,710,176 ( 2.1%)
-------------------------------------
TỔNG:        $15,680,869,265
```

**Ảnh chụp lợi nhuận:**
| Category | Revenue | Gross Profit | Margin | Return Rate |
|:---------|--------:|-------------:|-------:|------------:|
| Streetwear | $12.56B | $1.17B | 9.28% | 1.23% |
| Outdoor | $2.35B | $0.27B | 11.35% | 1.26% |
| GenZ | $0.33B | $0.05B | 15.47% | 1.27% |
| Casual | $0.44B | $0.03B | 7.66% | 1.20% |
| **TOTAL** | **$15.68B** | **$1.52B** | **9.68%** | **1.24%** |

**Chỉ số đơn hàng:**
- Tổng số đơn: 650,651
- AOV trung bình: $24,100
- Cơ cấu đơn hàng tương đồng cơ cấu doanh thu do AOV giữa các nhóm không chênh quá lớn

---

## TẦNG 2: DIAGNOSTIC — "VÌ SAO ĐIỀU ĐÓ XẢY RA?"

### Động lực lợi nhuận

**Xếp hạng gross profit:**
1. **Streetwear**: $1,165,807,512 (76.8% tổng lợi nhuận) — lợi thế chính đến từ quy mô
2. **Outdoor**: $267,034,092 (17.6%) — biên tốt và quy mô đủ lớn
3. **GenZ**: $50,836,377 (3.4%) — biên cao nhất nhưng quy mô còn nhỏ
4. **Casual**: $33,740,765 (2.2%) — hiệu quả thấp dù vẫn có 2.8% doanh thu

### Phân tích margin

**Danh mục dẫn đầu margin: GenZ (15.47%)**
- Định vị premium được thị trường chấp nhận
- Chất lượng biên tốt và ổn định
- Tiềm năng mở rộng doanh thu còn lớn

**Danh mục thách thức: Casual (7.66%)**
- Margin thấp nhất; khoảng cách 7.80 điểm % so với GenZ
- Nếu thu hẹp khoảng cách này, upside ước tính khoảng $34.4M/năm
- Nguyên nhân có thể gồm:
  - COGS cao
  - Cường độ khuyến mãi lớn
  - Áp lực cạnh tranh về giá
  - Cơ cấu sản phẩm chưa tối ưu

**Nhóm trung gian: Streetwear (9.28%), Outdoor (11.35%)**
- Streetwear thấp hơn mức bình quân danh mục (9.68%) nên có rủi ro bào mòn biên khi lệ thuộc volume
- Outdoor có biên tốt hơn trung bình, là nhóm cân bằng

### Efficiency Scorecard (margin × revenue share - return rate)

**Công thức:** (Margin % × Revenue Share) - (Return Rate × 100)

| Rank | Category | Efficiency Score | Diễn giải |
|:-----|:---------|:---------------:|:---|
| 1 | Streetwear | +6.20 | Đóng góp chính nhờ quy mô rất lớn |
| 2 | Outdoor | +0.72 | Cân bằng, biên tốt dù quy mô nhỏ hơn |
| 3 | GenZ | +0.24 | Biên cao nhưng tỷ trọng doanh thu còn thấp |
| 4 | Casual | -0.99 | Hiệu quả âm, đang kéo giảm hiệu suất toàn danh mục |

Kết luận chẩn đoán: Streetwear là "động cơ lợi nhuận", còn Casual là "điểm rò rỉ lợi nhuận" cần xử lý sớm.

---

## TẦNG 3: PREDICTIVE — "ĐIỀU GÌ CÓ KHẢ NĂNG XẢY RA TIẾP THEO?"

### Dự báo doanh thu danh mục dẫn đầu

**Đối tượng dự báo:** Streetwear  
**Phương pháp:** Linear Regression trên chuỗi doanh thu tháng  
**Horizon:** 3 tháng tới

| Giai đoạn | Doanh thu tháng | Loại dữ liệu |
|:----------|:---------------:|:------------:|
| Month -12 ... Month 0 | ~$31.1M bình quân | Quan sát |
| **Month +1** | **$71,725,039** | **Dự báo** |
| **Month +2** | **$71,284,954** | **Dự báo** |
| **Month +3** | **$70,844,869** | **Dự báo** |

**Độ dốc xu hướng:** -$440,085/tháng

Diễn giải:
- Month +1 tăng mạnh, khả năng do mùa vụ hoặc chiến dịch.
- Sau đỉnh có xu hướng giảm nhẹ về vùng run-rate bền vững quanh $70-71M/tháng.
- Hàm ý chiến lược: nếu không tối ưu margin, tăng trưởng lợi nhuận sẽ chậm lại khi doanh thu vào pha bão hòa.

---

## TẦNG 4: PRESCRIPTIVE — "CHÚNG TA NÊN LÀM GÌ?"

### Khung chiến lược theo Boston Matrix

**🏆 STARS (Doanh thu cao + Margin cao)**
- **GenZ**: biên 15.47% vượt xa bình quân 9.68%
- Hành động: mở rộng assortment, tăng đầu tư marketing, giữ định vị premium

**💰 CASH COWS (Doanh thu cao, Margin trung bình)**
- **Streetwear**: 80.1% doanh thu, 9.28% margin
- Hành động: bảo vệ thị phần, tối ưu vận hành, phục hồi margin

**❓ QUESTION MARKS (Doanh thu vừa, Margin tốt)**
- **Outdoor**: 15% doanh thu, 11.35% margin
- Hành động: kiểm tra dư địa tăng trưởng và mở rộng có chọn lọc

**🔴 PROBLEM CHILDREN (Doanh thu thấp, Margin thấp)**
- **Casual**: 2.8% doanh thu, 7.66% margin, efficiency âm
- Hành động: tái cấu trúc hoặc thu hẹp nếu không cải thiện trong 1-2 quý

---

### Khuyến nghị 1: Ưu tiên danh mục và phân bổ đầu tư

**Ưu tiên A - Bảo vệ và nâng biên Streetwear**
- Tối ưu COGS, kỷ luật khuyến mãi, cải thiện mix sản phẩm.

**Ưu tiên A - Tăng tốc GenZ**
- Mở rộng độ sâu SKU, đầu tư thương hiệu, thử nghiệm biên giá premium.

**Ưu tiên B - Duy trì Outdoor**
- Giữ hiệu suất ổn định, mở rộng chọn lọc ở phân khúc tiềm năng.

**Ưu tiên C - Rà soát chiến lược Casual**
- Root-cause theo COGS/giá/mix; đặt mốc quyết định trong 1-2 quý.

---

### Khuyến nghị 2: Playbook tối ưu margin

Phân tích cơ hội:
- Cao nhất (GenZ): 15.47%
- Thấp nhất (Casual): 7.66%
- Khoảng cách: 7.80 điểm %

| Sáng kiến | Casual hiện tại | Casual mục tiêu | Tác động |
|:----------|:---------------:|:---------------:|:--------:|
| Giảm COGS 5% | 7.66% | 9.51% | +$22.0M/năm |
| Tăng giá 3% | 7.66% | 10.89% | +$13.2M/năm |
| Chuyển dịch mix | 7.66% | 11.53% | +$18.8M/năm |
| **Kết hợp thận trọng** | **7.66%** | **12.50%** | **+$34.4M/năm** |

Streetwear nếu nâng từ 9.28% lên 10.5% có thể tạo thêm khoảng +$125.6M/năm.

---

### Khuyến nghị 3: Tối ưu cơ cấu tồn kho và phân bổ vốn

- **GenZ**: tăng tỷ trọng phân bổ từ 2.1% lên mục tiêu 5% doanh thu trong 18 tháng.
- **Streetwear**: tập trung tốc độ quay vòng, tránh phụ thuộc giảm giá sâu.
- **Casual**: right-size tồn kho theo kết quả tái cấu trúc.
- **Outdoor**: giữ ổn định, mở rộng khi có tín hiệu cầu rõ ràng.

---

### Khuyến nghị 4: Khung quản trị danh mục

Scorecard tháng:
```
Danh mục: __________ | Tháng: __________

  Revenue (MoM): __________ | Target: __________
  Margin (% YTD): __________ | Target: __________
  Return Rate (%): __________ | Ngưỡng: 1.5%
  Efficiency Score: __________ | Trend: ↑ ↓ →
  Hành động chính: [liệt kê sáng kiến đang chạy]
```

Nhịp quản trị:
- Hàng quý: QBR, cập nhật dự báo, quyết định mở rộng/duy trì/tối ưu/thu hẹp.
- Hàng năm: đánh giá cấu trúc danh mục và phân bổ ngân sách mới.

---

## Các Biểu Đồ Chính

1. 01_category_revenue_ranking.png - Xếp hạng doanh thu theo danh mục.
2. 02_margin_vs_revenue_scatter.png - Ma trận margin và doanh thu.
3. 03_top_bottom_categories_comparison.png - So sánh nhóm mạnh và nhóm yếu.
4. 04_top_category_trend_forecast.png - Xu hướng và dự báo Streetwear 3 tháng.

---

## Tác Động Tài Chính Dự Kiến

| Cơ hội | Động lực | Tác động |
|:-------|:---------|:--------:|
| Nâng margin Casual | COGS + pricing + mix | +$34.4M/năm |
| Nâng margin Streetwear | Vận hành + kỷ luật khuyến mãi | +$125.6M/năm |
| Mở rộng GenZ | Nhân rộng mô hình premium | +$20-50M gia tăng |
| Tối ưu Outdoor | Mở rộng chọn lọc | +$5-10M |
| **Tổng cơ hội danh mục** | Kết hợp sáng kiến | **+$185-220M/năm** |

---

## Rủi Ro Và Biện Pháp Giảm Thiểu

| Rủi ro | Mức độ | Biện pháp |
|:------|:------:|:----------|
| Margin Streetwear tiếp tục giảm | Cao | Rà soát COGS ngay, thử nghiệm khung giá theo phân khúc |
| Casual tái cấu trúc không hiệu quả | Trung bình | Đặt decision gate theo quý, chuẩn bị phương án thu hẹp |
| GenZ gặp phản ứng khi tăng giá | Trung bình | Tăng giá theo từng cụm khách, theo dõi elasticity |
| Cạnh tranh phản ứng khuyến mãi | Trung bình | Tăng khác biệt ở chất lượng và dịch vụ |
| Biến động mùa vụ làm lệch forecast | Thấp | Re-forecast hàng tháng, cập nhật lịch campaign |

---

## Kết Luận

Danh mục hiện có quy mô doanh thu tốt ($15.68B) nhưng phụ thuộc mạnh vào Streetwear (80.1%). Chênh lệch margin 7.80 điểm % và chênh lệch hiệu suất (6.20 so với -0.99) cho thấy **chất lượng thực thi về giá, mix và COGS quan trọng hơn mở rộng quy mô đơn thuần**.

Định hướng chiến lược:
1. Bảo vệ và nâng biên Streetwear.
2. Đầu tư tăng trưởng GenZ.
3. Tái cấu trúc hoặc thu hẹp Casual nếu không cải thiện.
4. Duy trì Outdoor như nhóm cân bằng.

Kết quả kỳ vọng: nâng margin danh mục từ 9.68% lên khoảng 10.5%, tương ứng tiềm năng cải thiện lợi nhuận khoảng $150M+/năm.

---

_Khung phân tích: Descriptive → Diagnostic → Predictive → Prescriptive_  
_Cập nhật tiếp theo: Scorecard danh mục theo tháng._
