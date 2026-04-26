# 🔄 9. Discount Cannibalization

## Datasets
- **Tables Used**: promotions ⨝ order_items ⨝ orders ⨝ customers
- **Analysis Layers**: Diagnostic (Di) + Prescriptive (Pr)

## Pain
- Discount cost $X/năm nhưng không biết bao nhiêu % là 'giảm giá cho khách vốn đã sẵn sàng mua full price'.

## Truth
- >60% revenue từ promo đến từ returning customers (đã mua ≤30 ngày trước).
- Phân tích: split pre-promo vs during-promo × flag first-time/returning.

## Tension
- CMO nghĩ promo là 'acquisition tool'; thực chất là 'retention discount' không ai gọi tên.

## Motivation
- Returning customer sẽ mua full price nếu không có promo; khi có promo, họ đợi rồi mua.
- Promo đang train khách đợi sale.

## Insight
- Promo đại trà không acquire khách mới — mà dạy khách cũ đợi sale.

## Action
- Target segment chưa mua 90 ngày (behavioural trigger); không blast-all.

### Liên quan
- §4.1 nút (3) Phục hồi
- §4.4 hàng 'Promo scheduling' (bổ sung targeting)
- §4.3 block 'Promo indicators'
- Liên quan MCQ Q5

## Execution Note
- **H**: >60% revenue promo đến từ returning customers → cannibalize.
- **T**: split pre vs during promo, flag first-time vs returning, % new customer acquired trong promo.
- **A**: target segment dormant 90 ngày.
