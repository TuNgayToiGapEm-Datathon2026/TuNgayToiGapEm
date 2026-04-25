**TỔNG QUAN BỘ DỮ LIỆU**

Bộ dữ liệu gồm **15 file CSV** được chia thành 4 lớp dữ liệu chính:

1. **Master Data:** Dữ liệu tham chiếu về sản phẩm, khách hàng, khuyến mãi và địa lý.

2. **Transaction Data:** Lịch sử giao dịch, thanh toán, vận chuyển và phản hồi.

3. **Analytical Data:** Dữ liệu đã được tổng hợp để phục vụ huấn luyện mô hình dự báo.

4. **Operational Data:** Dữ liệu vận hành về tồn kho và lưu lượng truy cập website.

## ---

**1\. LỚP DỮ LIỆU MASTER (DỮ LIỆU GỐC)**

### **1.1. products.csv (Danh mục sản phẩm)**

Chứa thông tin chi tiết về các mặt hàng đang kinh doanh.

* **product\_id:** Mã sản phẩm (Khóa chính).

* **category / segment:** Danh mục sản phẩm và phân khúc thị trường.

* **price / cogs:** Giá bán lẻ và giá vốn hàng bán (Ràng buộc: cogs \< price).

* **size / color:** Kích cỡ và màu sắc.

### **1.2. customers.csv (Thông tin khách hàng)**

Thông tin định danh và đặc điểm của khách hàng.

* **customer\_id:** Mã khách hàng (Khóa chính).

* **zip / city:** Mã bưu chính và thành phố cư trú.

* **signup\_date:** Ngày đăng ký tài khoản.

* **age\_group / gender / acquisition\_channel:** Nhóm tuổi, giới tính và kênh tiếp thị.

### **1.3. promotions.csv (Chương trình khuyến mãi)**

Chi tiết các chiến dịch ưu đãi.

* **promo\_type:** Loại giảm giá (theo % hoặc số tiền cố định).

* **discount\_value:** Giá trị giảm giá tương ứng.

* **stackable\_flag:** Cờ cho phép áp dụng đồng thời nhiều khuyến mãi.

* **min\_order\_value:** Giá trị đơn hàng tối thiểu để được áp dụng.

### **1.4. geography.csv (Địa lý)**

Bảng tra cứu vùng miền theo mã bưu chính.

* **zip:** Mã bưu chính (Khóa chính).

* **district / city / region:** Quận/huyện, thành phố và vùng địa lý (North, Central, South, West, East) .

## ---

**2\. LỚP DỮ LIỆU TRANSACTION (GIAO DỊCH)**

### **2.1. orders.csv & order\_items.csv**

Thông tin tổng quát và chi tiết từng dòng sản phẩm trong đơn hàng.

* **order\_status:** Trạng thái đơn (shipped, delivered, returned, cancelled,...).

* **order\_source / device\_type:** Kênh đặt hàng và thiết bị sử dụng.

* **unit\_price / discount\_amount:** Đơn giá sau giảm và tổng tiền được giảm cho sản phẩm đó.

### **2.2. payments.csv & shipments.csv**

* **payments:** Phương thức thanh toán (COD, Credit Card,...) và số kỳ trả góp (installments) .

* **shipments:** Ngày gửi/giao hàng và phí vận chuyển (shipping\_fee).

### **2.3. returns.csv & reviews.csv**

* **returns:** Lý do trả hàng (defective, wrong\_size,...) và số tiền hoàn lại (refund\_amount) .

* **reviews:** Điểm đánh giá (rating từ 1-5) và nội dung nhận xét từ khách hàng.

## ---

**3\. LỚP DỮ LIỆU ANALYSTICAL & OPERATIONAL**

### **3.1. sales.csv (Dữ liệu doanh thu \- Dùng cho Phần 3\)**

Dữ liệu đã được tổng hợp theo ngày để huấn luyện mô hình.

* **Date:** Ngày đặt hàng.

* **Revenue:** Tổng doanh thu thuần trong ngày.

* **COGS:** Tổng giá vốn hàng bán trong ngày.

### **3.2. inventory.csv (Tồn kho)**

Ảnh chụp trạng thái kho hàng vào cuối mỗi tháng.

* **stockout\_days:** Số ngày hết hàng trong tháng.

* **fill\_rate:** Tỷ lệ đơn hàng được đáp ứng đủ từ tồn kho.

* **overstock\_flag / reorder\_flag:** Các cờ cảnh báo tồn kho vượt mức hoặc cần nhập thêm hàng.

### **3.3. web\_traffic.csv (Lưu lượng truy cập)**

Hiệu suất của website bán hàng hàng ngày.

* **sessions / unique\_visitors:** Tổng số phiên và số khách truy cập duy nhất.

* **bounce\_rate:** Tỷ lệ thoát (truy cập 1 trang rồi rời đi).

* **avg\_session\_duration\_sec:** Thời gian trung bình mỗi phiên truy cập.

## ---

**MỐI QUAN HỆ GIỮA CÁC BẢNG (CARDINALITY)**

Để join dữ liệu chính xác cho các câu hỏi ở Phần 1 và 2, bạn cần lưu ý:

* **orders $\\leftrightarrow$ payments:** 1:1.

* **orders $\\leftrightarrow$ shipments:** 1:0 hoặc 1 (tùy trạng thái đơn hàng).

* **orders $\\leftrightarrow$ returns/reviews:** 1:0 hoặc nhiều.

* **products $\\leftrightarrow$ inventory:** 1:Nhiều (mỗi sản phẩm có 1 dòng trạng thái cho mỗi tháng).
