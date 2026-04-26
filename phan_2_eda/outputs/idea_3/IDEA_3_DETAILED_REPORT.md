# PHAN TICH CHI TIET DE TAI #3: RETURN REASON x SIZE x CATEGORY
## Wrong-size la driver chinh cua refund leakage va can quan tri den cap category-size cell

---

## 1. EXECUTIVE SUMMARY (ONE-LINER INSIGHT)

"Return khong chi la van hanh, do la bai toan fit giua san pham va ky vong khach hang."

Ket qua trong tam:
- Tong return lines: 39,939; tong refund amount: $510,598,507.
- wrong_size la return reason lon nhat, chiem 35.0% return lines.
- wrong_size dong gop 34.6% tong refund leakage.
- Category co return rate cao nhat: GenZ (5.72%).
- Du bao wrong_size rate 3 thang toi: 34.68%.
- Neu giam wrong_size 30%, co the tiet kiem ~$53,006,160.

---

## 2. TANG 1: DESCRIPTIVE ("What happened?")

### 2.1 Data Scope

- Products: 2,412
- Order items: 714,669
- Returns: 39,939
- Reviews: 113,551
- Return reasons: 5 nhom

### 2.2 Return Reason Distribution

| Return Reason | Share |
|--------------|-------|
| wrong_size | 34.97% |
| defective | 20.08% |
| not_as_described | 17.61% |
| changed_mind | 17.35% |
| late_delivery | 9.98% |

Dien giai:
- wrong_size la van de lon nhat, vuot xa cac ly do con lai.
- Giai bai toan fit-size se tac dong truc tiep den leakage.

### 2.3 Return Rate by Size and Category

- Worst size by return rate: S (5.65%)
- Worst category by return rate: GenZ (5.72%)

Dien giai:
- Return risk khong phan bo deu; co cum tap trung theo category-size.
- Can toi uu theo cell-level thay vi policy dong deu cho toan bo catalog.

---

## 3. TANG 2: DIAGNOSTIC ("Why did it happen?")

### 3.1 Refund Leakage by Reason

- Total refund: $510,598,507
- Wrong-size refund: $176,687,201
- Wrong-size refund share: 34.6%

Dien giai:
- Cu 1 USD refund thi co ~0.346 USD den tu wrong_size.
- wrong_size la diem roi loi nhuan lon nhat trong he thong returns.

### 3.2 Top Risk Cells

Top risk category-size theo return rate:
1. GenZ - XL: 6.17%
2. GenZ - M: 5.81%
3. Outdoor - S: 5.78%
4. GenZ - S: 5.76%
5. Outdoor - L: 5.68%

Dien giai:
- Van de fit khong dong deu theo size chung, ma theo combo category-size.
- Dieu nay ho tro huong tiep can "micro policy" cho size guide va PDP messaging.

### 3.3 Streetwear Check

- Streetwear wrong_size share: 35.0%

Dien giai:
- Streetwear la nhom can uu tien can thiep trong rollout dau tien.

---

## 4. TANG 3: PREDICTIVE ("What is likely to happen?")

Mo hinh trend tuyen tinh tren monthly wrong_size rate cho ket qua:

- Forecast wrong_size rate (3M): 34.68%
- Trend slope: -0.000032 per month

Dien giai:
- Trend giam rat nhe, gan nhu di ngang.
- Neu khong can thiep, wrong_size leakage se tiep tuc duy tri muc cao.

---

## 5. TANG 4: PRESCRIPTIVE ("What should we do?")

### 5.1 Action 1 - Fix Size Guide cho Top Risk Cells

- Uu tien top 10 category-size cells co return rate cao nhat.
- Canh chinh size chart theo nhom GenZ/Streetwear va size risk cao.

### 5.2 Action 2 - Size Advisor tai PDP/Checkout

- De xuat size theo return profile lich su theo category-size.
- Canh bao fit risk cho SKU co dau hieu wrong_size cao.

### 5.3 Action 3 - Post-purchase Fit Confirmation

- Trigger CSKH som voi don high-risk de giam return phat sinh.
- Ket hop message huong dan fit sau mua cho nhom de tra hang.

### 5.4 Action 4 - Return Scorecard Governance

KPI bat buoc:
1. wrong_size_share
2. wrong_size_refund_share
3. top-risk-cell return rate
4. monthly wrong_size trend

Muc tieu business:
- Giam wrong_size 30% => est. savings: $53,006,160.

---

## 6. VISUAL OUTPUTS

1. 01_return_reason_distribution.png - Return reason distribution.
2. 02_category_size_heatmap.png - Return rate heatmap theo category-size.
3. 03_wrong_size_trend.png - Monthly wrong-size trend + trend line.
4. 04_refund_by_reason.png - Refund leakage by return reason.
5. summary_metrics.csv - Bang KPI tong hop.

---

## 7. KET LUAN KINH DOANH

- Wrong-size la driver lon nhat cua return leakage trong bo du lieu nay.
- Co the tao tac dong tai chinh dang ke neu can thiep dung vao nhom category-size risk cao.
- Return management can chuyen tu cach tiep can overall sang cell-level governance.

---

## 8. NEXT EXPERIMENTS

1. A/B test 2 phien ban size-guide tren top-risk cells.
2. Thu nghiem fit advisory message theo category-size o PDP.
3. Theo doi scorecard hang thang de do hieu qua can thiep.
4. Dua return-risk features vao phan model du bao (Part 3).

---

Generated: 2026-04-24
Status: Ready for Part 2 EDA integration