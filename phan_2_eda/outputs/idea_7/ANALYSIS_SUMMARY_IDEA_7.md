# Tóm Tắt Phân Tích — IDEA #7: Payment & Device Behaviour

**Notebook:** `07_Payment_Device_Behaviour_Complete_Analysis.ipynb`

---

## Danh Sách Kiểm Tra Hoàn Thành

- [x] Đã nạp dữ liệu từ `orders` và `payments`
- [x] Đã xây dựng fact table theo `payment_method` và `device_type`
- [x] Đã hoàn thành đủ 4 tầng D-Di-P-Pr
- [x] Đã tạo 4 biểu đồ và xuất `summary_metrics.csv`
- [x] Đã định lượng tác động kinh doanh cho kịch bản giảm cancel COD

---

## Phát Hiện Chính

| Chỉ số | Giá trị |
|:--|:--|
| Tổng Orders | 646,945 |
| Tổng Cancelled Orders | 59,462 |
| Tỷ lệ Hủy Toàn Hệ Thống | 9.19% |
| Giá Trị Thanh Toán Trung Bình | $24,238.33 |
| Số Payment Methods | 5 |
| Payment Rủi Ro Cao Nhất | `cod` |
| Cancel Rate Cao Nhất | 16.00% |
| Payment Ổn Định Nhất | `bank_transfer` |
| Cancel Rate Thấp Nhất | 7.89% |
| Khoảng Cách Rủi Ro | 8.11 điểm phần trăm |
| Ô Device–Payment Rủi Ro Nhất | `tablet x cod` |
| Cancel Rate Ô Rủi Ro Nhất | 16.93% |
| Installment Plan Có Giá Trị Cao Nhất | 6 kỳ |
| Giá Trị Thanh Toán TB (Plan tốt nhất) | $24,446.65 |
| Dự Báo Cancel COD +1M | 15.93% |
| Độ Dốc Xu Hướng Cancel COD | 0.0004 pp/tháng |
| Mục Tiêu Cancel COD Sau Tối Ưu | 11.00% |
| Số Đơn Có Thể Giữ Lại | 4,834 |
| Doanh Thu Có Thể Giữ Lại | $117,169,321 |

---

## Điểm Nhấn Một Câu

> **COD không chỉ là phương thức thanh toán; đó là bài toán niềm tin khách hàng và tốc độ hoàn tất đơn.**

---

## Kết Luận Theo 4 Tầng

### 1) Descriptive — Điều gì đã xảy ra?
- COD là phương thức có tỷ lệ hủy cao nhất (16.00%).
- Bank transfer có tỷ lệ hủy thấp nhất (7.89%).
- Mặt bằng chung toàn hệ thống đang ở mức 9.19% đơn hủy.

### 2) Diagnostic — Vì sao xảy ra?
- Chênh lệch rủi ro theo payment method rất lớn (8.11 pp giữa cao nhất và thấp nhất).
- Cụm rủi ro cao nhất nằm ở `tablet x cod` với 16.93%.
- Điều này cho thấy rủi ro hủy không chỉ do payment, mà còn liên quan đến ngữ cảnh thiết bị.

### 3) Predictive — Điều gì có khả năng xảy ra tiếp theo?
- Nếu giữ nguyên hiện trạng, cancel rate của COD tháng tới vẫn quanh 15.93%.
- Xu hướng ngắn hạn gần như đi ngang (slope nhỏ dương), chưa có tín hiệu cải thiện tự nhiên.

### 4) Prescriptive — Nên làm gì?
1. Chạy chương trình ưu đãi prepaid cho nhóm COD đã mua thành công trước đó.
2. Ưu tiên xử lý cụm `tablet x cod` bằng UX rút gọn checkout và nhắc thanh toán trước.
3. Thiết lập cảnh báo sớm theo scorecard hằng tháng: cancel theo payment, cancel theo device-payment, và tỷ trọng COD.
4. Mục tiêu pha 1: kéo cancel COD từ 16.00% về 11.00%.

---

## Tệp Đầu Ra

- `01_cancel_rate_by_payment_method.png`
- `02_device_payment_cancel_heatmap.png`
- `03_top_risk_payment_cancel_trend.png`
- `04_installment_avg_payment_value.png`
- `summary_metrics.csv`

**Thư mục:** `phan_2_eda/outputs/idea_7/outputs/`
