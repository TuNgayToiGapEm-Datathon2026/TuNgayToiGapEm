# 🎯 IDEA #11 — DETAILED REPORT

## Gross-margin × Segment Mix — Simpson's Paradox & Forecast 2023-2024 với 95% CI

**Lead Analyst**: Đồng (D + Pr) · **Reviewer**: Hiển · **Update**: 2026-04-27

---

## 🧠 PAIN — TRUTH — TENSION — MOTIVATION (TTM Framework)

### Pain
Ban điều hành chọn product mix 2023 dựa trên KPI **margin per-SKU** — Standard 31.3%, Premium 28.5%. Quyết định phân bổ marketing & inventory dựa trên 2 con số này → **blended margin của công ty đang pha loãng -1.2pp/year** (forecast).

### Truth (3 lớp số liệu)
| KPI | Cách tính | Standard | Premium | Trendy | Balanced |
|---|---|---|---|---|---|
| **per-SKU mean** (cell 11.1) | `mean[(price-cogs)/price]` per segment | **31.34%** #1 | 28.50% #2 | 19.20% #6 | — |
| **revenue-weighted (list)** (cell 11.1a) | `Σ(price·qty - cogs·qty) / Σ(price·qty)` | drops to #5 | down | up to #2 | — |
| **realized** (cell 11.1a) | `Σ(unit_price·qty - cogs·qty) / Σ(unit_price·qty)` actual | **14.88%** #5 | **7.12%** #8 (worst) | **20.45%** #1 | **10.38%** #7 |

**Simpson's gap (per-SKU − realized)**: Premium **+21.4pp**, Standard **+16.5pp**.

### Tension
"Standard = best margin" và "Premium = cash cow margin cao bị bỏ quên" — cả 2 belief đều **sai khi nhìn realized margin**. Customer Premium negotiate / chờ flash sale → realized thấp. Customer Trendy = young + impulse + chấp nhận giá list cao → realized cao.

### Motivation
Nếu Trendy + Activewear là realized champions thật sự (20.45% + 19.04%) nhưng share doanh thu nhỏ (2.51% + 6.66%), và **slope 2018-2022 cho thấy chúng KHÔNG tự scale** (Trendy -0.09pp/yr, Activewear -0.87pp/yr) → đây là **opportunity** mà industry VN đang miss.

### Insight one-liner (decision-ready, ≤20 từ)
🔄 *"Top-margin per-SKU là illusion. Chỉ realized margin (sau actual unit_price) mới drive blended GP — Premium realized worst, Trendy realized champion."*

---

## 📊 DỮ LIỆU & METHODOLOGY

### Datasets joined (5 bảng)
- `products` (n=2,412): segment, price, cogs.
- `orders` (n=646,945): order_id, order_date.
- `order_items` (n=714,669): unit_price (actual), quantity, discount_amount.
- `shipments` (n=566,067): support cho idea 12 trong cùng notebook.
- `returns` (n=39,939): support cross-validation.

### Công thức 3 margin (key — đã document trong cell 11.1a)
```
margin_per_SKU      = mean_p ∈ segment [(price_p − cogs_p) / price_p]
margin_rev_weighted = Σ_p (price_p − cogs_p) · qty_p
                      / Σ_p price_p · qty_p                      (list price)
margin_realized     = Σ_oi (unit_price_oi − cogs_oi) · qty_oi
                      / Σ_oi unit_price_oi · qty_oi              (actual order_items.unit_price)
```

### Forecast methodology với 95% CI (Hiển sửa cell 11.4a)
```
share_seg_t = β₀ + β₁·t + ε_t,    OLS trên window 2018-2022 (n=5)
                                   (KHÔNG dùng full 10y vì break-point 2014-2017)
slope SE   = σ̂ / √Σ(x_i − x̄)²
slope CI   = β̂₁ ± t_{α/2, n-2} · SE,   t_0.025,3 = 3.182
forecast SE = σ̂ · √(1/n + (x_* − x̄)² / Σ(x_i − x̄)²)
forecast CI = ŷ_* ± t_{α/2, n-2} · SE_forecast
renormalize Σ shares = 100% mỗi year (accounting identity)
```

---

## 🔮 PREDICTIVE RESULTS (cell 11.4 + Fig 11.4)

| Segment | Slope (pp/yr) | 95% CI | Significant? | 2023 forecast | 2024 forecast | 95% CI 2024 |
|---|---|---|---|---|---|---|
| **Balanced** | **+4.74** | [+2.10, +7.39] | ✅ YES | 55.09% | **59.84%** | [56.40%, 63.20%] |
| Trendy | −0.09 | [−0.52, +0.34] | ❌ NO (flat) | 2.23% | 2.13% | wide |
| Activewear | −0.87 | [−1.43, −0.31] | ✅ YES (declining) | 6.22% | 5.35% | narrow |
| Performance | −1.46 | [−2.21, −0.71] | ✅ YES (declining) | 8.77% | 7.32% | narrow |
| Everyday | −2.77 | [−4.05, −1.49] | ✅ YES (declining) | 18.57% | 15.80% | narrow |
| Premium | +0.11 | [−0.41, +0.64] | ❌ NO | 2.92% | 3.03% | wide |
| Standard | +0.10 | [−0.36, +0.55] | ❌ NO | 1.90% | 2.00% | wide |
| All-weather | +0.24 | [−0.34, +0.81] | ❌ NO | 4.29% | 4.53% | wide |

### Scenario blended margin (cell 11.4b)
- **Baseline 2023** (trend extrapolation): blended realized margin = **12.474%**.
- **Scenario A3** (-3pp Balanced → +1.5pp Trendy + 1.5pp Activewear): **+0.281pp** → incremental GP **3.29M/yr**.
- **Scenario aggressive** (-6pp Balanced → +3pp Trendy + 3pp Activewear): **+0.562pp** → incremental GP **6.57M/yr**.

---

## 💼 PRESCRIPTIVE — 3 ACTIONS (TTM-mapped, Execution-Ready)

### Action A1 — Mở rộng SKU Trendy + Activewear
| Field | Value |
|---|---|
| **What** | Launch +30 SKU Trendy/Activewear; ưu tiên inventory re-order |
| **Trigger** | Q3 2026 planning |
| **Threshold** | Combined share Trendy+Activewear: 9.2% (2022) → 15% trong 12 tháng |
| **Rollback** | Nếu share không +1pp trong 6 tháng → revisit (có thể canh tăng marketing thay launch SKU) |
| **Owner** | Merchandising + Inventory |
| **Telemetry** | Monthly realized margin per segment; alarm nếu Trendy realized <18% |
| **Impact** | A3 conservative: +3.29M GP/yr · Aggressive: +6.57M GP/yr |

### Action A2 — Audit SKU Premium
| Field | Value |
|---|---|
| **What** | Chia Premium thành tier giá (P10/P50/P90); tính realized margin từng tier; discontinue tier "giả Premium" (giá thấp + cogs ratio xấu) |
| **Trigger** | Q3 2026 (đồng thời A1) |
| **Threshold** | Realized margin Premium ≥ 12% sau 6 tháng |
| **Rollback** | Nếu sau audit không tìm được tier "giả Premium" rõ ràng → giữ nguyên + sang Action khác |
| **Owner** | Product |
| **Telemetry** | Realized margin Premium per tier (P10/P50/P90 monthly) |

### Action A3 — Cap Balanced growth + tái phân bổ marketing
| Field | Value |
|---|---|
| **What** | Cap Balanced share ≤ 50% qua giảm trade-in promo; tái phân bổ 30% Balanced marketing budget → Trendy/Activewear |
| **Trigger** | Q3 2026 budget review |
| **Threshold** | Mix shift ≥ 3pp sang Trendy+Activewear trong 9 tháng |
| **Rollback** | Nếu Balanced revenue absolute drop >5% YoY → restore 50% budget |
| **Owner** | Growth + Marketing Lead |
| **Telemetry** | Quarterly mix tracking; alarm nếu Balanced share >55% |

---

## 🔗 CROSS-REFERENCE

- **§4.1 node**: (1) Quá khứ tăng trưởng + (2) Mix segment.
- **§4.4 row**: 1 — Pricing & discount (Business goal: Promo planning).
- **MCQ Q2**: Đáp án D = Standard top per-SKU margin (31.34%) — verify từ cell 11.1.
- **Narrative PDF v3**:
  - T2 Diagnostic chính (BCG matrix Fig 11.3 = F3 chart).
  - T3 sub-T3.1 (Margin forecast Fig 11.4 = F4 chart với CI band).

## ⚠️ COUNTER-ARGUMENTS & RESPONSES (phản biện cuối narrative)

1. **"Linear forecast bỏ qua non-linearity, có thể bể 2024"** → Đã CI ±3.4pp + plan quarterly re-run.
2. **"Margin 2022 proxy cho 2023 có thể sai nếu cost shock"** → Sensitivity: ±10% cogs Trendy/Activewear → uplift co/giãn ±1.2M GP, vẫn dương.
3. **"Trendy realized 20.45% có thể overfit do n nhỏ"** → Đã ghi caveat; A/B test trước commit budget lớn.
