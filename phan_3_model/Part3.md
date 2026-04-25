PHẦN 3: MÔ HÌNH DỰ BÁO DOANH THU (SALES FORECASTING)

1\. Bối cảnh kinh doanh

Bạn đóng vai trò là một nhà khoa học dữ liệu tại một doanh nghiệp thương mại điện tử thời trang tại Việt Nam. Nhiệm vụ của bạn là dự báo nhu cầu ở mức chi tiết để doanh nghiệp tối ưu hóa tồn kho, lập kế hoạch khuyến mãi và quản lý logistics.

2\. Định nghĩa bài toán

Bạn cần dự báo giá trị tại cột **Revenue** cho khoảng thời gian trong tương lai. Mỗi dòng trong tập dữ liệu kiểm tra là một bộ giá trị duy nhất gồm (**Date**, **Revenue**, **COGS**).

3\. Dữ liệu sử dụng

| Phân loại | File dữ liệu | Khoảng thời gian |
| :---- | :---- | :---- |
| **Huấn luyện (Train)** | sales.csv | 04/07/2012 – 31/12/2022 |
| **Kiểm tra (Test)** | sales\_test.csv | 01/01/2023 – 01/07/2024 |

**Lưu ý:** Tập test không được công bố mà dùng để đánh giá trên Kaggle. File nộp bài phải đúng định dạng như sample\_submission.csv.

4\. Chỉ số đánh giá

Mô hình của bạn sẽ được chấm điểm dựa trên 3 chỉ số chính:

* **Mean Absolute Error (MAE):** Đo độ lệch tuyệt đối trung bình.

  $$MAE=\\frac{1}{n}\\sum\_{i=1}^{n}|F\_{i}-A\_{i}|$$

* **Root Mean Squared Error (RMSE):** Phạt nặng hơn các sai số lớn.

  $$RMSE=\\sqrt{\\frac{1}{n}\\sum\_{i=1}^{n}(F\_{i}-A\_{i})^{2}}$$

* **Hệ số xác định ($R^{2}$):** Thể hiện tỷ lệ phương sai được giải thích bởi mô hình (càng gần 1 càng tốt).

  $$R^{2}=1-\\frac{\\sum\_{i=1}^{n}(A\_{i}-F\_{i})^{2}}{\\sum\_{i=1}^{n}(A\_{i}-\\overline{A})^{2}}$$

5\. Các ràng buộc quan trọng (Rất quan trọng\!)

* **Không dùng dữ liệu ngoài:** Chỉ sử dụng các đặc trưng (features) được tạo từ các file dữ liệu do Ban tổ chức cung cấp.

* **Tính tái lập (Reproducibility):** Phải đính kèm mã nguồn và đặt random\_seed để Ban giám khảo có thể chạy lại kết quả.

* **Khả năng giải thích:** Phải có phần giải thích các yếu tố tác động đến doanh thu (Sử dụng Feature Importances, SHAP values,...) bằng ngôn ngữ kinh doanh.

6\. Thang điểm (Tổng 20 điểm)

| Thành phần | Mô tả | Điểm tối đa |
| :---- | :---- | :---- |
| **Hiệu suất mô hình** | Dựa trên thứ hạng Kaggle (MAE, RMSE, $R^{2}$ thấp/cao tương ứng). | 12 điểm |
| **Báo cáo kỹ thuật** | Chất lượng pipeline, kỹ thuật xử lý dữ liệu, kiểm soát leakage và tính giải thích. | 8 điểm |

---

**⚠️ Cảnh báo loại bài:** Nhóm sẽ bị **0 điểm** Phần 3 nếu:

1. Sử dụng chính Revenue/COGS từ tập test làm đặc trưng (leakage).

2. Sử dụng dữ liệu bên ngoài.

3. Không nộp mã nguồn hoặc kết quả không thể chạy lại được.

