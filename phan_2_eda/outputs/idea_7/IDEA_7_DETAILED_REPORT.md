# Báo Cáo Chi Tiết — IDEA #7: Payment & Device Behaviour

**Notebook:** `07_Payment_Device_Behaviour_Complete_Analysis.ipynb`  
**Phạm vi dữ liệu:** `orders` + `payments` trên toàn bộ lịch sử giao dịch

---

## 1. Tóm Tắt Điều Hành

Phân tích hành vi thanh toán và thiết bị cho thấy rủi ro hủy đơn tập trung mạnh ở COD, đặc biệt khi kết hợp với thiết bị tablet. Đây là tín hiệu quan trọng vì tỷ lệ hủy cao làm thất thoát doanh thu thực nhận và tạo thêm chi phí vận hành (pick-pack, xử lý hoàn trạng thái, cơ hội bán bị bỏ lỡ).

Kết quả nổi bật:
- COD có cancel rate 16.00% (cao nhất trong 5 phương thức).
- Bank transfer chỉ 7.89% (thấp nhất).
- Chênh lệch rủi ro giữa cao nhất và thấp nhất là 8.11 điểm phần trăm.
- Cụm rủi ro cao nhất theo tổ hợp là `tablet x cod` với 16.93%.
- Nếu giảm COD từ 16.00% xuống 11.00%, có thể giữ lại khoảng 4,834 đơn, tương ứng ~$117.17M.

---

## 2. Tầng 1 — Descriptive (Điều gì đã xảy ra?)

### 2.1 Tổng quan hệ thống
- Tổng số đơn: 646,945
- Tổng đơn hủy: 59,462
- Tỷ lệ hủy toàn hệ thống: 9.19%
- Giá trị thanh toán trung bình: $24,238.33

### 2.2 Phân bổ theo phương thức thanh toán
Xếp hạng cancel rate:
1. COD: 16.00%
2. PayPal: xấp xỉ 8%
3. Apple Pay: xấp xỉ 8%
4. Credit Card: xấp xỉ 8%
5. Bank Transfer: 7.89%

Nhận định: COD là outlier rõ rệt và cần tách riêng chiến lược vận hành/khuyến khích thanh toán.

---

## 3. Tầng 2 — Diagnostic (Vì sao xảy ra?)

### 3.1 Chẩn đoán theo payment method
- Khoảng cách 8.11 pp giữa COD và bank_transfer cho thấy bản chất rủi ro không đồng đều giữa các phương thức.
- COD phản ánh độ do dự hoặc niềm tin chưa đủ tại thời điểm đặt đơn.

### 3.2 Chẩn đoán theo tổ hợp device × payment
- Điểm nóng rủi ro: `tablet x cod` (16.93%).
- Điểm tốt nhất: `mobile x bank_transfer` (7.77%).

Hàm ý:
- Cần đi sâu vào luồng checkout theo thiết bị thay vì chỉ xem payment độc lập.
- Tablet có thể là thiết bị phát sinh “đặt thử” nhiều hơn ở nhóm COD.

### 3.3 Chỉ số rủi ro tổng hợp
`risk_score = cancel_rate * log(1 + order_count)` xác nhận COD là nhóm cần ưu tiên xử lý trước.

---

## 4. Tầng 3 — Predictive (Điều gì có khả năng xảy ra?)

Phân tích chuỗi tháng cho payment rủi ro cao nhất (COD):
- Cancel rate hiện tại: 14.09% (tháng cuối quan sát)
- Dự báo +1M: 15.93%
- Dự báo +2M: 15.93%
- Dự báo +3M: 15.93%
- Độ dốc xu hướng: +0.0004 pp/tháng

Diễn giải:
- Mức hủy COD có khả năng duy trì cao nếu không có can thiệp.
- Dấu hiệu xu hướng gần đi ngang, nghĩa là hệ thống chưa tự cải thiện theo thời gian.

---

## 5. Tầng 4 — Prescriptive (Nên làm gì?)

### 5.1 Mục tiêu ưu tiên
Giảm cancel COD 5 điểm phần trăm (16.00% -> 11.00%).

### 5.2 Gói hành động khuyến nghị
1. **Ưu đãi prepaid cho nhóm COD đủ điều kiện**
- Áp dụng voucher 2% cho khách có lịch sử mua thành công.
- Mục tiêu chuyển đổi dần từ COD sang prepaid ở nhóm rủi ro cao.

2. **Can thiệp theo cụm rủi ro `tablet x cod`**
- Rút gọn checkout steps.
- Hiển thị thông điệp cam kết giao nhanh và xác nhận đơn rõ ràng.
- Bổ sung nhắc xác nhận trước xử lý đơn.

3. **Thiết lập scorecard theo tháng**
- Cancel rate theo payment_method.
- Cancel rate theo device × payment.
- Tỷ trọng đơn COD trong tổng đơn.
- Giá trị bị mất ước tính do hủy.

4. **Vòng lặp tối ưu 4 tuần/lần**
- Kiểm tra cohort chịu tác động (khách mới vs khách quay lại).
- Điều chỉnh incentive theo hiệu suất thực tế.

### 5.3 Tác động định lượng
- Đơn giữ lại ước tính: 4,834
- Doanh thu giữ lại ước tính: $117,169,321

---

## 6. Các Biểu Đồ Đầu Ra

1. `01_cancel_rate_by_payment_method.png`: So sánh tỷ lệ hủy theo phương thức thanh toán.
2. `02_device_payment_cancel_heatmap.png`: Heatmap rủi ro theo tổ hợp thiết bị và thanh toán.
3. `03_top_risk_payment_cancel_trend.png`: Xu hướng hủy theo tháng của phương thức rủi ro cao nhất.
4. `04_installment_avg_payment_value.png`: Mối quan hệ installments và giá trị thanh toán trung bình.
5. `summary_metrics.csv`: Bộ chỉ số tổng hợp để theo dõi và trình bày.

---

## 7. Kết Luận Kinh Doanh

Idea 7 xác nhận rằng COD là điểm nghẽn lớn trong phễu hoàn tất đơn hàng. Chỉ cần can thiệp có mục tiêu vào đúng cụm rủi ro (đặc biệt theo device × payment), doanh nghiệp có thể cải thiện đáng kể tỷ lệ giữ đơn và doanh thu thực nhận mà không cần tăng traffic đầu vào.

Trọng tâm vận hành trong giai đoạn tới:
- Tối ưu conversion ở bước thanh toán.
- Giảm rủi ro COD có kiểm soát.
- Theo dõi liên tục bằng scorecard theo tháng để duy trì hiệu quả.
