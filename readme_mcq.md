# Phần 1: Giải bài trắc nghiệm (MCQ) - Datathon 2026 Round 1

Tài liệu này ghi chú lại kết quả giải quyết 10 câu hỏi trắc nghiệm (Part 1 - 20đ) và hướng dẫn reproduce (tái lập) kết quả. File này sẽ đi kèm cùng source code trên Github của team.

## 🏆 Đáp án chính thức

Dựa trên script phân tích dữ liệu, dưới đây là bộ đáp án được chốt để điền vào Form Nộp Bài của BTC:

| Câu hỏi | Lĩnh vực phân tích | Kịch bản / Logic | Lựa chọn cuối cùng |
|---------|-------------------|------------------|-------------------|
| **Q1** | Customer Behavior | Inter-order gap trung vị thực tế tính ra 144 ngày. | **C (180 ngày)** |
| **Q2** | Product Margin | Tính Gross Margin = `(price - cogs) / price`. | **D (Standard)** |
| **Q3** | Return Insight | Join `returns` và lọc `category='Streetwear'`. | **B (wrong_size)** |
| **Q4** | Web Analytics | Lọc nguồn có trung bình `bounce_rate` nhỏ nhất. | **C (email_campaign)** |
| **Q5** | Promo Strategy | Tỷ lệ dòng có áp dụng promo chính xác là 38.66%. | **C (39%)** |
| **Q6** | Customer Segment | Số lượng đơn `nunique()` / số lượng user `nunique()`. | **A (55+)** |
| **Q7** | Sales by Region | Doanh thu thuần cao nhất đạt **7.402.050.928 VNĐ**. | **C (East)** |
| **Q8** | Cancellation | Đếm tần suất payment type trên các đơn hủy. | **A (credit_card)** |
| **Q9** | Return Rate | Tỷ lệ trả hàng cao nhất đạt 5.65%. | **A (S)** |
| **Q10** | Installment | Trung bình payment theo kỳ đạt 24.447 VNĐ. | **C (6 kỳ)** |

## ⚙️ Hướng dẫn Reproduce (Tái lập kết quả)

Để tự động tính toán và xuất ra kết quả tương tự, chạy script đã được tích hợp sẵn:

1. Đảm bảo bạn đang ở thư mục gốc của project (nơi chứa thư mục `dataset-datathon-2026-round-1/`).
2. Mở terminal và chạy lệnh:
   ```bash
   python3 solve_mcq.py
   ```
3. *(Lựa chọn 2)*: Mở notebook `notebooks/02_mcq.ipynb` và Run All Cells (chứa chung logic source).

## 🧠 Logic Kinh Doanh Quan Trọng (Business Rules Applied)

Script giải quyết đề đã bám sát triệt để Data Dictionary và Business Rules của cuộc thi:
- **Câu 7 (Net Revenue)**: Rủi ro lớn nhất là nhầm lẫn Gross và Net. Script đã tính doanh thu bằng cách join `order_items` với `geography`, sau đó **trừ đi số tiền hoàn trả** (`refund_amount`) từ bảng `returns` để tuân thủ định nghĩa chặt chẽ của file `sales.csv`.
- **Định dạng tiền tệ**: Vì theo yêu cầu của team mệnh giá là VNĐ, code sử dụng formatter loại bỏ số thập phân và dùng `.` làm dấu ngăn cách hàng nghìn để tránh sai sót đọc hiểu (VD: 24.447 VNĐ thay vì 24,447).

---
*Thực hiện bởi: Hiển (Đội trưởng - Coordinator)*
