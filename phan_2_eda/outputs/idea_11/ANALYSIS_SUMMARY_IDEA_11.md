## 📊 PHÂN TÍCH CHI TIẾT ĐỀ TÀI #11: GROSS-MARGIN × SEGMENT MIX
### Simpson's Paradox Reconcile (per-SKU vs revenue-weighted vs realized) + Forecast 2023-2024 với 95% CI

---

## ✅ ANALYSIS COMPLETION CHECKLIST

### ✓ Tầng 1: DESCRIPTIVE (D) — "What happened?"
- [x] Load 5 bảng (`products`, `orders`, `order_items`, `shipments`, `returns`) — n=646,945 orders, 714,669 line items, 2,412 SKU.
- [x] Tính `margin_pct = (price - cogs) / price` per SKU; mean theo segment (cell 11.1).
- [x] Bảng mean/median/n_skus/mean_price cho 8 segments — Standard top per-SKU 31.34%, Premium #2 28.5%.
- [x] Visualize Fig 11.1 — bar chart margin per-SKU sort giảm dần, highlight Standard (top) + Premium.
- [x] Bảng revenue share theo year × segment 2012-2022 (cell 11.2).
- [x] Visualize Fig 11.2 — line chart revenue share trends, highlight Balanced bành trướng + Premium ổn định.

**Key finding**:
- Standard top per-SKU mean margin (31.34%) — khớp MCQ Q2 đáp án D.
- Premium revenue share dao động 2.13-3.70%, KHÔNG giảm tuyến tính như giả thuyết.
- Câu chuyện thật là **Balanced bành trướng** từ 23.94% (2014) → 48.85% (2022), Δ +24.9pp.

---

### ✓ Tầng 2: DIAGNOSTIC (Di) — "Why did it happen?"
- [x] **Reconcile 3 khái niệm margin** (per-SKU mean / revenue-weighted list / realized) — section 11.1a.
- [x] Visualize Fig 11.1a — 3-bar grouped chart so sánh 3 KPI, sort theo realized.
- [x] Phát hiện **Simpson's paradox kinh điển**: Standard top per-SKU (31.34%) nhưng realized #5 (14.88%); gap 16.5pp.
- [x] Premium gap **21.4pp** giữa list (28.5%) và realized (7.12%) — realized **WORST** trong 8 segments.
- [x] Trendy là **realized champion 2022** (20.45%) nhưng share doanh thu chỉ 2.51%.
- [x] Discount intensity ~5-6% đều ở mọi segment → gap KHÔNG do discount, do **product mix nội segment**.
- [x] Ma trận Revenue share × Realized margin 2022 — Fig 11.3 BCG matrix custom với 4 quadrant Star/Cash Cow/Volume Play/Dead Zone.

**Key finding**: 3 hypothesis kiểm định:
- **H1** (Premium = top margin): **REFUTE** per-SKU + **REFUTE realized** (worst).
- **H2** (Premium share giảm): **REFUTE** — chỉ dao động 2.13-3.70%, Δ 2014→2022 +0.12pp.
- **H3** (Mix shift gây pha loãng): **SUPPORT** — Balanced 48.85% share / 10.38% realized = volume play pha loãng blended margin.

---

### ✓ Tầng 3: PREDICTIVE (P) — "What is likely to happen?"
- [x] **Linear OLS** trên window 2018-2022 (5 năm, không dùng 10y full vì break-point structural 2014-2017).
- [x] **95% CI cho slope + forecast point** (Hiển sửa cell 11.4a) — t-distribution với df=n-2=3, t_crit=3.182.
  - Công thức: `SE(ŷ_*) = σ̂ · √(1/n + (x_* − x̄)² / Σ(x_i − x̄)²)`; CI = ŷ ± t_{α/2,n-2} · SE.
- [x] Forecast 2023, 2024 share renormalized (Σ = 100%/year, accounting identity).
- [x] **Visualize Fig 11.4** với 95% CI band shaded (Hiển sửa) cho 3 segment quan trọng (Balanced, Trendy, Activewear).
- [x] **Scenario blended margin**:
  - Baseline 2023 = 12.474% (trend extrapolation).
  - Scenario A3 (3pp shift Balanced→Trendy/Activewear): +0.281pp → +3.29M GP/year.
  - Scenario aggressive (6pp shift): +0.562pp → +6.57M GP/year.

**Key finding**:
- **Balanced slope +4.74pp/yr** [95% CI ±2.65pp] significant → 2024 chạm 60% revenue (CI [56.4%, 63.2%]).
- **Trendy slope -0.09pp/yr** [CI bao 0] → flat, KHÔNG tự scale.
- **Activewear -0.87pp/yr** [significant] → đang giảm.
- → 2 segment realized champion KHÔNG tự scale → cần intervention chủ động.

---

### ✓ Tầng 4: PRESCRIPTIVE (Pr) — "What should we do?"
- [x] **3 Action TTM-mapped** (cell 11.5):
  - **A1**: Mở rộng SKU Trendy + Activewear +30 SKU; combined share 9.2% → 15% trong 12 tháng. KPI: blended realized margin +≥0.5pp.
  - **A2**: Audit SKU Premium (chia tier giá P10/P50/P90, discontinue tier "giả Premium"). KPI: realized margin Premium ≥12% sau 6 tháng.
  - **A3**: Cap Balanced volume ≤50%; tái phân bổ marketing → Trendy/Activewear. KPI: mix shift ≥3pp/9 tháng.
- [x] Impact định lượng từ Predictive: 3pp shift = +3.29M GP/yr; 6pp shift = +6.57M GP/yr.
- [x] **Caveat**: linear OLS có thể over-estimate Balanced 2024 nếu đường cong uốn; Prophet/quadratic mở cho Phase 5b.

---

## 🔑 KEY COUNTER-INTUITIVE FINDINGS (cho narrative PDF, T2 block)

🔄 **Insight 1**: Top-margin per-SKU là ILLUSION. Standard top per-SKU 31.34% nhưng realized chỉ #5 (14.88%) — Simpson's paradox.

🔄 **Insight 2**: Premium = realized WORST (7.12%), KHÔNG phải "cash cow margin cao bị bỏ quên". Gap list vs realized 21.4pp cảnh báo product mix Premium có vấn đề.

🔄 **Insight 3**: Trendy + Activewear là realized champions (20.45% + 19.04%) nhưng KHÔNG tự scale (slope -0.09 và -0.87pp/yr). Cần marketing intervention.

🔄 **Insight 4**: Balanced bành trướng +4.74pp/yr → forecast 2024 đạt 60% revenue → blended margin pha loãng -1.2pp nếu không can thiệp.

---

## 📁 OUTPUT FILES GENERATED

- `figures/11_1_margin_by_segment.png` — Fig 11.1 per-SKU margin bar chart.
- `figures/11_1a_margin_reconcile.png` — Fig 11.1a 3-KPI margin reconcile (Simpson's paradox).
- `figures/11_2_revenue_share_trend.png` — Fig 11.2 revenue share trends 2012-2022.
- `figures/11_3_matrix_share_margin.png` — **Fig 11.3 BCG matrix realized × share** (chart đắt nhất, F3 narrative T2).
- `figures/11_4_share_forecast.png` — **Fig 11.4 forecast với 95% CI band** (F4 narrative T3).

---

## 🔗 LIÊN KẾT NGƯỢC

- **§4.1 node**: (1) Quá khứ tăng trưởng + (2) Mix segment.
- **§4.4 row**: 1 — Pricing & discount (Business goal: Promo planning).
- **MCQ Q2**: Standard top per-SKU margin (31.34%) — đáp án D.
- **Narrative PDF v3**: T2 Diagnostic Simpson's Paradox + T3 Predictive Convergence sub-T3.1.
- **Phần 3 Forecasting**: Predictive forecast 11.4 KHÔNG feed vào Phần 3 (model target là Revenue/COGS daily, không phải segment share annual). Insight này feed vào TTM block T2 để justify Action.

---

## ⚠️ CAVEAT & LIMITATIONS

- Linear OLS bỏ qua non-linearity. Balanced 2021→2022 đã chậm (Δ +2.6pp vs 2020→2021 +3.4pp) → forecast 59.8% có thể over-estimate.
- Margin per-segment 2022 dùng làm proxy cho 2023 — nếu cost shock (cotton/logistics) đánh nặng Trendy → uplift co lại.
- Trendy n nhỏ 2022 (13,983 units) → realized margin 20.45% có CI rộng; cần A/B test trước khi commit budget lớn.
- Discount intensity ~5-6% đều ở mọi segment **chưa control time** — có thể có spike trong promo campaign.
