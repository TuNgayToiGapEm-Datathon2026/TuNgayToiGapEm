# Checklist Reviewer: Đánh giá hoàn thành Nhiệm vụ 1 (MCQ)

Tài liệu này dành cho **Đội trưởng Hiển** và **Reviewer** dùng để rà soát (audit) chất lượng cho phần thi MCQ trước khi chốt đáp án đưa vào form submit nộp cho BTC. Mỗi câu MCQ đáng giá 2 điểm, do đó không được phép sai sót từ logic lập trình hoặc hiểu lầm metric kinh doanh.

---

## 🔍 I. Checklist Logic Kinh Doanh & Ràng Buộc Dữ Liệu

Đảm bảo người thực thi (Hiển) đã tuân thủ các điều kiện tiên quyết (theo `CLAUDE.md` và Đề thi PDF):

- [ ] **Q1 (Inter-order gap)**: Chỉ tính cho các khách hàng có **hơn 1 đơn hàng**. Gap được tính bằng `ngày`, lưu ý dùng toán tử lấy sai số đúng bằng ngày (ví dụ `dt.days`). Cần sắp xếp theo thời gian (`order_date`) trước khi tính gap.
- [ ] **Q2 (Gross Margin)**: Phải áp dụng đúng công thức của BTC: `(price - cogs) / price`. Tính nhầm thành markup `(price - cogs) / cogs` là sai hoàn toàn.
- [ ] **Q3 (Streetwear Returns)**: Đã join `returns` và `products` thành công theo khoá `product_id`. Hãy cẩn thận check string `"Streetwear"` (viết hoa chữ S).
- [ ] **Q4 (Bounce Rate thấp nhất)**: Phải lọc `traffic_source` trên bảng `web_traffic`. Hàm aggregation phải là `.mean()` chứ không phải tổng hay đếm. Trả về tên `traffic_source` có giá trị `mean` là bé nhất.
- [ ] **Q5 (Tỷ lệ dòng order_items khuyến mãi)**: Đã kiểm tra null check bằng `.notnull()` hoặc `.isna() == False` ở cột `promo_id`. Metric tính trên *dòng* (row count), không tính trên số lượng sản phẩm (`quantity`).
- [ ] **Q6 (Đơn hàng TB theo độ tuổi)**: Bỏ qua khách hàng có `age_group` bị null. "Đơn hàng TB trên mỗi khách hàng" = Tổng số *đơn hàng duy nhất* chia cho số *khách hàng duy nhất* trong nhóm đó. 
- [ ] **Q7 (Doanh thu cao nhất theo Vùng)**: Metric Revenue ở đây tính bằng `sum(quantity * unit_price)`. Đã nhớ join 3 bảng `order_items` -> `orders` -> `geography` vì trong bảng sales không có chi tiết Vùng. (Lưu ý: `unit_price` trong `order_items` đã là giá sau chiết khấu, không cần tính toán thêm discount nữa).
- [ ] **Q8 (Payment Method cho Cancelled orders)**: Cột `order_status` phải filter chính xác là `"cancelled"`.
- [ ] **Q9 (Tỷ lệ trả hàng cao nhất theo Size)**: Return rate = `(count(returns theo size) / count(order_items theo size))`. Đừng đếm quantity, phải đếm **bản ghi** (row count) theo đúng lời đề.
- [ ] **Q10 (Trả góp trung bình cao nhất)**: Aggregation `.mean()` của cột `payment_value` trên `installments`. Check xem có kỳ trả góp bất thường nào không (ví dụ 0 kỳ?).

---

## 💻 II. Checklist Kỹ thuật Code (Pandas)

- [ ] Đã chạy code trong môi trường Jupyter/Python 3.10+ đúng như thống nhất của team.
- [ ] Đã kiểm tra hiện tượng **Duplicate Join**: Khi join `order_items` với `orders` (1:1/1:N) hoặc bảng khác, liệu số lượng dòng có bị phình to (Cartesian explosion) không? (Kiểm tra len(df) trước và sau khi join).
- [ ] Đã test run notebook `02_mcq.ipynb` từ đầu đến cuối một cách trơn tru, không báo lỗi `KeyError` hay `SettingWithCopyWarning`.

---

## 🏆 III. Bước chốt cuối

1. **In đáp án**: Sau khi code xuất ra, so sánh các kết quả với list các phương án (A, B, C, D) đã cung cấp sẵn trong `CLAUDE.md`. (Ví dụ kết quả Q1 tính ra phải xấp xỉ một trong số các lựa chọn: 30, 90, 180, hoặc 365).
2. **Ghi chú**: Nếu kết quả tính toán có sự chênh lệch nhỏ (VD: tính ra 92 ngày nhưng đáp án là 90 ngày) → Hãy chốt đáp án gần nhất và comment trong code tại sao chọn đáp án đó.
3. **Approval**: Check off các mục trong file này sau đó upload notebook `02_mcq.ipynb` lên Github repo. Update bảng tiến độ trong `CLAUDE.md` sang trạng thái `✅ DONE`.
