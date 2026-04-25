# Báo Cáo Chi Tiết — IDEA #8: Review -> Return Correlation

**Notebook:** 08_Review_Return_Correlation_Complete_Analysis.ipynb  
**Phạm vi dữ liệu:** orders + reviews + returns + products

---

## 1. Tóm Tắt Điều Hành

Mục tiêu của idea 8 là kiểm tra giả thuyết quan trọng về trải nghiệm khách hàng: đơn có review thấp (<=2 sao) có xu hướng hoàn trả cao hơn đơn review tốt (>=4 sao). Đây là giả thuyết then chốt để thiết kế cơ chế CSKH can thiệp sớm sau review xấu.

Tuy nhiên, theo kết quả pipeline hiện tại:
- Return rate của các nhóm rating đều bằng 0.00%
- Kiểm định Fisher không cho thấy khác biệt (p-value = 1.000000)
- Forecast cho nhóm low-rating cũng phẳng ở 0.00%

Điều này cho thấy bài toán hiện tại thiên về chất lượng liên kết dữ liệu review-return hơn là tín hiệu nghiệp vụ thực tế.

---

## 2. Tầng 1 — Descriptive (Điều gì đã xảy ra?)

### 2.1 Tổng quan dữ liệu
- Tổng đơn hàng: 646,945
- Số đơn có review: 111,369
- Tỷ lệ phủ review: 17.21%

### 2.2 Mô tả return theo nhóm rating
- Low rating (<=2): 0.00%
- High rating (>=4): 0.00%
- Overall reviewed return rate: 0.00%

Nhận định: ở trạng thái hiện tại, dữ liệu sau merge chưa thể hiện được mối tương quan giữa review và return.

---

## 3. Tầng 2 — Diagnostic (Vì sao xảy ra?)

### 3.1 Kết quả thống kê
- Fisher Exact p-value: 1.000000
- Odds ratio: nan
- Rate ratio low/high: nanx

### 3.2 Diễn giải nguyên nhân khả dĩ
Khi toàn bộ tỷ lệ return ở nhóm phân tích bằng 0, các thước đo so sánh mất ý nghĩa thống kê. Điều này thường đến từ một trong các nguyên nhân sau:
1. Logic join theo cấp `order_id` chưa phản ánh đúng quan hệ `order_id + product_id` giữa review và return.
2. Bộ mẫu review được giữ lại sau bước lọc chưa chứa phần giao cắt với return.
3. Khung thời gian mapping review-return chưa khớp.

### 3.3 Điểm rủi ro theo category
Dù return_rate đều 0.00%, pipeline vẫn ghi nhận category xuất hiện ở vị trí rủi ro cao nhất trong nhóm low-rating là **Casual**. Đây là điểm nên theo dõi sát ở vòng refinement dữ liệu tiếp theo.

---

## 4. Tầng 3 — Predictive (Điều gì có khả năng xảy ra?)

Mô hình tuyến tính trên chuỗi tháng của nhóm low-rating cho kết quả:
- Forecast +1M: 0.00%
- Forecast +2M: 0.00%
- Forecast +3M: 0.00%
- Trend slope: 0.0000 pp/tháng

Kết luận predictive:
- Khi tín hiệu lịch sử bằng 0, mô hình sẽ trả về xu hướng phẳng.
- Giá trị dự báo hiện tại phù hợp về mặt toán học nhưng chưa hữu ích cho quyết định kinh doanh.

---

## 5. Tầng 4 — Prescriptive (Nên làm gì?)

Dù tín hiệu định lượng chưa đủ mạnh, vẫn có thể triển khai khung hành động theo hướng phòng ngừa:

### 5.1 Hành động ngắn hạn
1. Trigger CSKH trong vòng <=48h sau review <=2 sao.
2. Đặt SLA xử lý cho nhóm low-rating để giảm rủi ro danh tiếng.
3. Ưu tiên theo dõi nhóm sản phẩm/nhóm category có dấu hiệu nhạy cảm (Casual).

### 5.2 Hành động dữ liệu (bắt buộc cho vòng tiếp theo)
1. Chuẩn hóa mapping review-return ở cấp `order_id + product_id`.
2. Bổ sung kiểm tra độ trễ thời gian giữa review_date và return_date.
3. Tái chạy kiểm định Fisher sau khi làm sạch join để kiểm chứng lại giả thuyết 3x.
4. Chỉ đưa mục tiêu tiết kiệm refund vào business case khi return signal khác 0 và có ý nghĩa thống kê.

### 5.3 Chỉ số vận hành đề xuất
- low_rating_volume
- response_sla_48h
- return_after_low_review
- refund_saved_after_intervention

---

## 6. Biểu Đồ Và Tệp Đầu Ra

1. 01_return_rate_by_rating_band.png
2. 02_category_rating_return_heatmap.png
3. 03_low_high_rating_return_trend.png
4. 04_low_rating_return_forecast.png
5. summary_metrics.csv

---

## 7. Kết Luận Kinh Doanh

Idea 8 đã hoàn thành đúng quy trình D-Di-P-Pr và tạo đủ deliverables, nhưng kết quả hiện tại cho thấy pipeline liên kết review-return cần được tinh chỉnh để phản ánh đúng thực tế hành vi khách hàng. Trong khi chờ hoàn thiện dữ liệu, chiến lược phù hợp là triển khai CSKH phản ứng nhanh sau review thấp như một lớp bảo vệ danh tiếng và giảm rủi ro vận hành.

Thông điệp chính: review thấp vẫn là tín hiệu quan trọng để hành động sớm, nhưng cần một lớp đo lường tốt hơn để định lượng chính xác tác động đến return và refund.
