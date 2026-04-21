# Datathon 2026 - Brainstorm & Plan

## 1. Đọc nhanh đề bài

Bài thi có 3 phần:

1. **Phần 1 - Trắc nghiệm tính toán trực tiếp** trên các file CSV.
2. **Phần 2 - Phân tích và trực quan hoá**: cần kể chuyện bằng dữ liệu, không chỉ mô tả.
3. **Phần 3 - Forecast doanh thu**: dự báo `Revenue` cho tương lai, có ràng buộc chống leakage và cần giải thích mô hình.

## 2. Keyword và ý chính

- Bài toán là một **e-commerce fashion dataset**.
- Dữ liệu xoay quanh 4 cụm chính: **master data**, **transaction data**, **analytical data**, **operational data**.
- Trọng tâm đánh giá không chỉ là đúng số liệu, mà là **logic join**, **insight kinh doanh**, **khả năng giải thích**, và **tính tái lập**.
- Phần 2 ưu tiên mức phân tích **prescriptive**: từ mô tả sang khuyến nghị hành động.
- Phần 3 chấm theo **MAE, RMSE, R2** và có penalty nặng nếu bị **leakage** hoặc dùng dữ liệu ngoài.

## 3. Metric cốt lõi

### Phần 1
- Cần tính đúng các chỉ số từ dữ liệu: median inter-order gap, gross margin, tỉ lệ trả hàng, bounce rate, tỷ lệ promo, average orders per customer, revenue by region, cancelled payment method, return rate by size, average payment by installment.

### Phần 2
- Không có metric số cứng, nhưng hội đồng chấm theo:
  - chất lượng visual,
  - chiều sâu phân tích,
  - insight kinh doanh,
  - storytelling.

### Phần 3
- Metric chính: **MAE**, **RMSE**, **R2**.
- Ngoài điểm Kaggle, report còn cần pipeline sạch, reproducible, và có giải thích feature importance / SHAP.

## 4. Rủi ro dữ liệu: missing và imbalance

### Missing nổi bật
- Gần như toàn bộ bảng chính **không có missing value** ở các cột quan trọng.
- Missing tập trung gần như hoàn toàn ở các cột promo:
  - `order_items.csv`:
    - `promo_id`: 438,353 missing trên 714,669 dòng.
    - `promo_id_2`: 714,463 missing trên 714,669 dòng, gần như bỏ trống hoàn toàn.
  - `promotions.csv`:
    - `applicable_category`: 40 missing trên 50 dòng.
- Hệ quả thực tế:
  - Không nên mặc định coi `promo_id_2` là feature chính.
  - Nếu dùng promo features cho Part 2 hoặc Part 3 thì phải xử lý theo kiểu flag / active promo / promo count thay vì phụ thuộc raw id.

### Imbalance nổi bật
- `orders.csv`:
  - `order_status` lệch mạnh về `delivered` (516,716 / 646,945).
  - `payment_method` lệch về `credit_card` (356,352 / 646,945).
  - `order_source` lệch về `organic_search` và `paid_search`.
- `products.csv`:
  - `category` lệch mạnh, đặc biệt `Streetwear` chiếm lớn nhất.
  - `segment` không cân bằng hoàn toàn, nhưng vẫn đủ để so sánh nhóm.
- `customers.csv`:
  - `age_group` lệch về nhóm 25-34 và 35-44.
  - `gender` lệch nhẹ, có nhóm `Non-binary` nhỏ.
- `returns.csv`:
  - `return_reason` lệch về `wrong_size` (13,967 / 39,939).
- `reviews.csv`:
  - rating lệch về 4-5 sao, tức sentiment khá tích cực.
- `web_traffic.csv`:
  - `traffic_source` lệch về `organic_search`.
- `payments.csv`:
  - `installments` lệch mạnh về 1, 3, 6 kỳ; 12 kỳ ít hơn rõ rệt.
- `geography.csv`:
  - `region` chỉ có 3 vùng chính, lệch về East/Central.

### Ý nghĩa cho cách làm
- Vì dữ liệu sạch ở phần lớn bảng, team nên tập trung vào **feature engineering** và **business interpretation** thay vì dọn missing quá nhiều.
- Imbalance không phải lỗi dữ liệu, mà là tín hiệu kinh doanh thật, nên nên khai thác nó để kể chuyện ở Part 2.

## 5. Điểm cần lưu ý ngay

- Tên file trong đề có thể khác tên thực tế trong thư mục, ví dụ `sales_train.csv` trong câu hỏi nhưng workspace đang có `sales.csv`.
- Một số câu Part 1 yêu cầu join nhiều bảng, nên cần chốt **cardinality** trước để tránh đếm sai.
- Phần 3 phải tránh dùng bất kỳ biến nào từ tập test làm feature.

## 6. Hướng brainstorm độc lập cho từng người

### Người 1: Part 1 + data validation
- Làm toàn bộ 10 câu trắc nghiệm.
- Chuẩn hoá join keys, kiểm tra cardinality, đếm trùng, kiểm tra null.
- Kết quả cần có bảng công thức ngắn gọn cho từng câu.

### Người 2: Part 2 - insight và storytelling
- Chọn 3-5 góc nhìn có business value, nhưng nên gom thành 1 câu chuyện xuyên suốt thay vì 5 chart rời.
- Cách kể chuyện nên đi theo pipeline:
  - **Traffic -> Order -> Fulfillment -> Return -> Revenue**.
  - Hoặc **Customer segment -> Promo -> Basket -> Return -> Profitability**.
- Các hypothesis nên kiểm tra:
  - Traffic source nào tạo nhiều sessions nhưng bounce cao, tức là kéo traffic kém chất lượng.
  - Promo nào tăng volume nhưng làm tăng return rate hoặc giảm margin.
  - Size / category nào có return rate bất thường, gợi ý vấn đề fit hoặc chất lượng.
  - Nhóm tuổi / kênh acquisition nào mua nhiều hơn nhưng giá trị đơn thấp hơn.
  - Vùng địa lý nào mạnh về doanh thu nhưng yếu về logistics hoặc fulfillment.
- Bộ biểu đồ gợi ý nên có:
  - **Line chart** theo thời gian cho revenue, orders, bounce rate, or return rate.
  - **Bar chart** so sánh theo segment, category, size, payment method, region.
  - **Heatmap** cho tương quan giữa promo, size, category, return reason.
  - **Stacked bar** cho order status theo payment method hoặc traffic source.
  - **Boxplot / violin plot** nếu muốn nhấn mạnh phân phối order value hoặc delivery time theo nhóm.
  - **Treemap / sunburst** nếu muốn kể câu chuyện category -> segment -> size.
- Với mỗi chart, nên viết theo công thức:
  - Câu hỏi business là gì.
  - Chart đang cho thấy gì.
  - Con số nào nổi bật nhất.
  - Tại sao điều đó quan trọng.
  - Nên làm gì tiếp theo.
- Một số insight có thể thành kết luận mạnh:
  - `wrong_size` đang là lý do return lớn nhất, nên sizing guide có thể tác động trực tiếp.
  - `organic_search` có thể là nguồn traffic lớn nhưng chưa chắc có conversion tốt nhất, cần so bounce và revenue cùng lúc.
  - Nhóm `25-34` và `35-44` là core customers, có thể so sánh hành vi mua và phản ứng với promo để tìm segment ưu tiên.
  - `Streetwear` có thể là category lớn nhất, nhưng cần kiểm tra margin và return để biết có thật sự là category tốt nhất không.
  - `East` / `Central` / `West` có thể khác nhau về doanh thu và shipping friction, là điểm để đề xuất logistics.
- Nếu nhóm muốn điểm storytelling cao hơn, có thể làm một narrative kiểu:
  - Tháng nào traffic tăng nhưng revenue không tăng tương ứng?
  - Phần nào của funnel đang rò rỉ: traffic, conversion, fulfillment hay returns?
  - Đâu là đòn bẩy ngắn hạn: promo, inventory, size chart, hay channel mix?
- Mỗi biểu đồ phải có: câu hỏi, số liệu chính, kết luận kinh doanh, hành động đề xuất.

### Người 3: Part 3 - forecasting
- Xây baseline trước, sau đó nâng cấp feature set. Không nên nhảy ngay vào model phức tạp trước khi có baseline sạch.
- Cần chốt first principles của bài toán:
  - Dữ liệu train là chuỗi theo ngày.
  - Mục tiêu là dự báo `Revenue`.
  - Không được dùng thông tin tương lai.
  - Mọi feature ngoại sinh phải có mặt đúng thời điểm dự báo.
- Baseline nên làm theo thứ tự:
  - **Naive / seasonal naive**: dùng giá trị hôm trước hoặc cùng ngày tuần trước.
  - **Moving average / rolling mean**: lấy trung bình 7, 14, 28 ngày.
  - **Lag features**: lag 1, 7, 14, 28, 56.
  - **Calendar features**: day of week, month, week of year, holiday / pre-holiday nếu có thể tự suy ra từ date.
  - **Trend features**: ngày kể từ đầu chuỗi, rolling slope, rolling std.
- Feature engineering có thể thử:
  - từ `sales.csv`: lag, rolling mean, rolling std, growth rate, YoY-like change nếu đủ lịch sử.
  - từ `web_traffic.csv`: sessions, unique visitors, bounce rate, session duration, traffic source mix.
  - từ `inventory.csv`: stockout_days, fill_rate, reorder_flag, overstock_flag, sell_through_rate.
  - từ `promotions.csv`: promo active flag, promo intensity, stackable flag, min_order_value.
- Nếu join được hợp lệ, nên tạo thêm features dạng:
  - `traffic_to_revenue_ratio`
  - `stockout_pressure`
  - `promo_presence`
  - `promo_density`
  - `return_pressure` nếu có proxy theo thời gian
- Model candidates nên so sánh:
  - linear / ridge regression với lag features.
  - tree-based model như Random Forest, XGBoost, LightGBM nếu môi trường cho phép.
  - model chuỗi thời gian nếu team quen, nhưng chỉ nên dùng khi pipeline rõ ràng.
- Validation nên theo thời gian, không shuffle:
  - train/validation split theo cutoff date.
  - tốt hơn nữa là rolling / walk-forward validation.
  - report nên có bảng so sánh MAE, RMSE, R2 trên validation.
- Checklist chống leakage:
  - Không dùng target tương lai để tạo feature.
  - Không dùng rolling window lấy dữ liệu vượt quá cutoff.
  - Nếu có normalize, scaler phải fit trên train בלבד.
  - Nếu join inventory/promo/traffic, phải kiểm tra thời điểm sẵn có của dữ liệu.
- Phần giải thích mô hình nên trả lời:
  - Feature nào quan trọng nhất.
  - Feature đó nói gì về business.
  - Mô hình đang học seasonality, trend hay traffic-driven demand.
- Cách viết kết quả cho report:
  - Baseline nào.
  - Feature nào làm tốt hơn.
  - Tăng/giảm bao nhiêu theo MAE/RMSE/R2.
  - Business interpretation: demand tăng theo traffic hay bị nghẽn bởi stockout/promo.

## 7. Plan chung đề xuất

### Bước 1: Chốt dữ liệu và schema
- Xác nhận key join giữa các bảng.
- Xác nhận file nào là source thật cho từng phần.
- Tạo data dictionary ngắn cho nhóm.

### Bước 2: Chia việc
- Một người làm Part 1.
- Một người làm phân tích Part 2.
- Một người làm forecasting Part 3.
- Một người tổng hợp report và kiểm tra consistency.

### Bước 3: Làm report chung
- Gộp các phát hiện vào một narrative thống nhất.
- Phần 2 nên dẫn dắt bằng một câu chuyện kinh doanh rõ ràng, không xếp rời rạc theo từng bảng.
- Phần 3 nên có baseline, cải tiến, validation, và interpretation.

### Bước 4: Chuẩn bị nộp
- Kiểm tra format submission.
- Kiểm tra reproducibility từ notebook / script.
- Kiểm tra report PDF và link GitHub.

## 8. Gợi ý góc nhìn mạnh cho Part 2

1. **Promo hiệu quả đến đâu**: tỷ lệ dùng promo, tác động lên doanh thu, margin, return rate.
2. **Return pain points**: size, category, reason, delivery delay, review rating.
3. **Customer behavior**: age group, acquisition channel, device, order frequency, repeat purchase.
4. **Geo performance**: region/city revenue, logistics, shipping friction, fulfillment issues.
5. **Traffic-to-sales funnel**: traffic source, bounce rate, session duration, revenue proxy.
6. **Product mix strategy**: category/segment/size nào tạo doanh thu tốt nhưng ít return hơn.
7. **Operational bottlenecks**: stockout, fill rate, reorder flag và impact lên sales.

### Bộ câu hỏi phân tích nên chốt
- Nguồn traffic nào kéo người dùng vào nhiều nhưng chất lượng kém nhất?
- Có promo nào làm tăng volume nhưng đánh đổi bằng margin hoặc return rate không?
- Size nào bị return nhiều nhất, và khác biệt này có rõ theo category không?
- Age group nào vừa mua nhiều vừa có hành vi ổn định hơn về rating / return?
- Vùng nào bán tốt nhưng logistics xấu, tức doanh thu cao nhưng trải nghiệm thấp?
- Sản phẩm nào thuộc nhóm bán tốt về volume nhưng kém về profitability?

### Gợi ý visual theo mục tiêu
- Nếu muốn nhấn mạnh **xu hướng thời gian**: dùng line chart, rolling average, annotated events.
- Nếu muốn nhấn mạnh **so sánh nhóm**: dùng bar chart sorted descending và highlight top/bottom 3.
- Nếu muốn nhấn mạnh **mối liên hệ**: dùng scatter plot / bubble chart / heatmap.
- Nếu muốn nhấn mạnh **tỷ trọng**: dùng stacked bar, treemap, or sunburst.

### Cách viết insight cho mỗi biểu đồ
1. Biểu đồ nói gì.
2. Số nào quan trọng nhất.
3. Vì sao nó quan trọng cho business.
4. Hành động cụ thể nào nên làm tiếp.

## 9. Gợi ý storyboard cho Part 2

### Story 1: Doanh thu không chỉ nằm ở traffic
- Bắt đầu bằng traffic sources.
- Chứng minh nguồn nào có bounce thấp hơn và tốt hơn về revenue.
- Kết luận: không phải traffic nào nhiều cũng tốt.

### Story 2: Khuyến mãi có thể là con dao hai lưỡi
- So sánh order value, discount usage, return rate, product mix.
- Kết luận: cần tối ưu promo theo segment / category thay vì chạy rộng.

### Story 3: Tồn kho và size ảnh hưởng trực tiếp trải nghiệm
- Kết nối inventory với returns và reviews.
- Kết luận: sizing / stockout đang tạo chi phí ngầm.

### Story 4: Nhóm khách hàng mục tiêu
- Chia theo age group, acquisition channel, device.
- Kết luận: tập trung ngân sách vào nhóm có CLV cao hơn, không chỉ nhóm mua nhiều.

## 10. Việc nên làm ngay

- Chốt câu trả lời Part 1 bằng một sheet tính toán riêng.
- Chọn trước 3 câu chuyện chính cho Part 2, và mỗi câu chuyện có 2-3 biểu đồ hỗ trợ.
- Dựng baseline forecasting sớm để có mốc so sánh.
- Nếu làm report, ưu tiên structure: problem -> evidence -> business implication -> recommendation.

## 11. Part 2 - version chi tiết hơn để họp phân công

### 11.1 Mục tiêu của Part 2
- Không chỉ trả lời “điều gì xảy ra”, mà phải giải thích “vì sao” và “nên làm gì tiếp theo”.
- Nên nhắm tới 1 câu chuyện chính và 2-3 nhánh phụ, thay vì liệt kê rời rạc nhiều chart.
- Mỗi insight nên có số liệu cụ thể, tránh câu kết luận chung chung như “có xu hướng tăng” hoặc “có tương quan”.

### 11.2 Bộ insight có thể khai thác sâu

#### A. Funnel traffic -> revenue
- So sánh `traffic_source` theo:
  - sessions
  - bounce_rate
  - avg_session_duration_sec
  - revenue proxy nếu join được với sales theo thời gian
- Câu hỏi cần trả lời:
  - Nguồn nào nhiều traffic nhưng chất lượng thấp?
  - Nguồn nào ít traffic hơn nhưng chuyển đổi tốt hơn?
  - Có thời điểm nào traffic tăng nhưng revenue không tăng tương ứng không?
- Kết luận business có thể hướng tới:
  - tối ưu ngân sách marketing theo chất lượng traffic,
  - giảm chi cho nguồn traffic có bounce cao,
  - ưu tiên kênh có session dài và revenue ổn định.

#### B. Promo, discount và trade-off
- So sánh các đơn có promo và không có promo theo:
  - order value / payment_value
  - return rate
  - rating
  - product category / segment
- Câu hỏi cần trả lời:
  - Promo có thật sự tăng doanh thu hay chỉ tăng số đơn?
  - Promo có làm tăng return do khách mua “cho thử” không?
  - Loại promo nào tốt hơn: giảm % hay giảm số tiền cố định?
- Kết luận business có thể hướng tới:
  - không chạy promo đại trà,
  - thiết kế promo theo category / segment,
  - đặt ngưỡng min_order_value để tránh phá margin.

#### C. Returns và vấn đề fit/chất lượng
- So sánh return theo:
  - size
  - category
  - return_reason
  - rating
  - maybe delivery time nếu join shipments
- Câu hỏi cần trả lời:
  - Size nào bị return nhiều nhất?
  - Category nào có vấn đề fit hoặc chất lượng rõ nhất?
  - Return do late delivery có làm rating giảm không?
- Kết luận business có thể hướng tới:
  - cải thiện size guide,
  - chặn các SKU có return rate cao,
  - phối hợp ops và logistics để giảm late delivery.

#### D. Customer segmentation
- So sánh theo:
  - age_group
  - gender
  - acquisition_channel
  - device_type
- Câu hỏi cần trả lời:
  - Nhóm khách nào mua nhiều nhất?
  - Nhóm nào có chất lượng đơn hàng tốt hơn: ít return, rating cao, value cao?
  - Kênh acquisition nào tạo khách hàng tốt hơn về dài hạn?
- Kết luận business có thể hướng tới:
  - tập trung ngân sách vào nhóm khách có giá trị tốt hơn,
  - cá nhân hoá promo theo segment,
  - ưu tiên trải nghiệm mobile nếu mobile chiếm chủ đạo.

#### E. Geography và logistics
- So sánh theo:
  - region
  - city
  - shipping_fee
  - delivery_date / ship_date nếu dùng được
  - revenue
- Câu hỏi cần trả lời:
  - Vùng nào tạo doanh thu cao nhưng chi phí vận chuyển cũng cao?
  - Có region nào mạnh về revenue nhưng yếu về fulfillment không?
  - Geography có liên quan đến return hoặc rating không?
- Kết luận business có thể hướng tới:
  - tối ưu kho theo region,
  - ưu tiên tuyến logistics tốt hơn,
  - điều chỉnh SLA theo vùng.

### 11.3 Đề xuất bộ chart tối thiểu nên có
- 1 line chart cho revenue / orders theo thời gian.
- 1 bar chart cho traffic source hoặc category / segment.
- 1 bar chart cho return reason hoặc size return rate.
- 1 stacked bar hoặc heatmap cho promo / payment / order status.
- 1 scatter chart cho relationship giữa traffic, bounce, revenue hoặc between discount and return.
- 1 chart về geography hoặc customer segment.

### 11.4 Template viết insight cho từng chart
- **Observation**: biểu đồ đang thấy gì.
- **Evidence**: số nào, chênh lệch bao nhiêu, nhóm nào cao nhất/thấp nhất.
- **Interpretation**: tại sao điều này có thể xảy ra.
- **Action**: nên làm gì nếu là business team.

### 11.5 Nếu muốn bài nhìn “cao điểm” hơn
- Đưa ra 1 kết luận trái ngược trực giác, ví dụ:
  - traffic cao không đồng nghĩa revenue cao,
  - promo nhiều không chắc tốt hơn,
  - category bán nhiều chưa chắc lợi nhuận tốt,
  - vùng doanh thu cao có thể đi kèm return hoặc shipping xấu.
- Chốt 1-2 đề xuất hành động có tính định lượng, ví dụ:
  - giảm spend ở nguồn traffic bounce cao,
  - tập trung promo vào nhóm sản phẩm có margin tốt,
  - sửa size guide cho nhóm SKU return nhiều.

## 12. Part 3 - version chi tiết hơn để họp phân công

### 12.1 Mục tiêu của Part 3
- Làm một pipeline forecast có thể chạy lại.
- Có baseline rõ ràng rồi mới nâng cấp.
- Giải thích được mô hình đang học gì từ dữ liệu.

### 12.2 Cấu trúc pipeline nên đi theo
1. Đọc `sales.csv` và chuẩn hoá date index.
2. Tạo split theo thời gian, không shuffle.
3. Dựng baseline 1: naive / seasonal naive.
4. Dựng baseline 2: rolling mean / lag features.
5. Thử mô hình supervised tabular.
6. So sánh bằng validation time-based.
7. Chốt model cuối, train lại trên full train, dự báo test.
8. Xuất submission đúng format.

### 12.3 Feature engineering cụ thể hơn
- **Calendar features**:
  - day_of_week
  - week_of_month
  - month
  - quarter
  - year
  - is_weekend
- **Lag features**:
  - lag_1, lag_7, lag_14, lag_28, lag_56
- **Rolling features**:
  - rolling_mean_7, rolling_mean_14, rolling_mean_28
  - rolling_std_7, rolling_std_14, rolling_std_28
- **Trend features**:
  - day_index
  - cumulative mean
  - delta vs rolling mean
- **External signals nếu hợp lệ theo thời gian**:
  - traffic sessions
  - bounce rate
  - inventory stockout_flag / fill_rate
  - promo active flag

### 12.4 Cách kiểm soát leakage
- Chỉ dùng dữ liệu có sẵn tại thời điểm dự báo.
- Không dùng future window trong rolling.
- Không dùng target test để sinh feature.
- Nếu merge bảng ngoài sales, phải xác định rõ nó là snapshot trước ngày dự báo hay sau ngày dự báo.
- Nếu không chắc về thời điểm của feature, bỏ khỏi model.

### 12.5 Model candidate theo mức độ rủi ro
- **Mức 1 - an toàn**:
  - naive
  - seasonal naive
  - ridge regression
- **Mức 2 - cân bằng**:
  - random forest
  - gradient boosting
  - XGBoost / LightGBM nếu môi trường có
- **Mức 3 - khi đã có thời gian**:
  - model chuỗi thời gian riêng
  - ensemble giữa forecast truyền thống và model tabular

### 12.6 Validation nên report như thế nào
- Cần ít nhất 1 validation split theo thời gian.
- Nếu có thời gian, làm rolling backtest để chắc hơn.
- Report nên có bảng:
  - model name
  - features used
  - MAE
  - RMSE
  - R2
  - nhận xét ngắn
- Nếu model phức tạp hơn nhưng không tốt hơn baseline rõ ràng, không nên giữ.

### 12.7 Giải thích business cho model
- Nếu feature quan trọng nhất là lag / rolling mean, nghĩa là doanh thu có tính tự tương quan mạnh.
- Nếu traffic features quan trọng, nghĩa là demand chịu ảnh hưởng đáng kể từ marketing.
- Nếu inventory features quan trọng, nghĩa là supply constraint đang chạm vào doanh thu.
- Nếu promo features quan trọng, nghĩa là revenue bị kéo bởi campaign.

## 13. Gợi ý phân công cho team

### Người A - Part 1
- Tính 10 câu trắc nghiệm.
- Viết công thức, join path, và kết quả cuối.
- Kiểm tra lại những câu có thể sai do join many-to-many.

### Người B - Part 2, nhánh traffic / customer / geography
- Làm traffic funnel, customer segment, geography.
- Chuẩn bị 3-4 chart chính.
- Viết insight theo template observation -> evidence -> interpretation -> action.

### Người C - Part 2, nhánh promo / returns / product mix
- Làm promo impact, returns, size/category.
- So sánh return rate, rating, margin proxy nếu có.
- Chốt 2 chart mạnh nhất cho report.

### Người D - Part 3
- Dựng baseline forecasting.
- Tạo validation theo thời gian.
- Thử 2-3 model, chọn model tốt nhất.
- Viết phần explainability.

### Người E - Tổng hợp report
- Ghép narrative cho Part 2 và Part 3.
- Đảm bảo style đồng nhất.
- Kiểm tra giới hạn 4 trang và thứ tự nội dung.

## 14. Kịch bản họp Meet nên chốt

1. Chốt mỗi người phụ trách phần nào.
2. Chốt 3 insight lớn của Part 2.
3. Chốt baseline và model chính của Part 3.
4. Chốt deadline nội bộ cho bản nháp và bản final.
5. Chốt ai chịu trách nhiệm merge report và kiểm tra submission.

## 15. Output cuối mong muốn của cả nhóm

- 1 file trả lời Part 1.
- 1 bộ chart + narrative Part 2.
- 1 notebook / script forecasting Part 3.
- 1 report PDF ngắn gọn, có logic và số liệu rõ.
- 1 submission file đúng format Kaggle.