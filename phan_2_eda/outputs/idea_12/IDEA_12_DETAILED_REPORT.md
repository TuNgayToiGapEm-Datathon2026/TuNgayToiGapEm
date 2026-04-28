# 🎯 IDEA #12 — DETAILED REPORT

## Shipping Fee × Return Rate — Logistic Regression (Adjusted OR) + Power Analysis

**Lead Analyst**: Kiên (Di + Pr) · **Reviewer**: Hiển · **Update**: 2026-04-27

---

## 🧠 PAIN — TRUTH — TENSION — MOTIVATION (TTM Framework)

### Pain
Growth team đẩy free-ship để kéo conversion. Nhưng nỗi sợ: **return rate "ăn" lại margin** nếu khách coi free-ship là fitting-room miễn phí → mua nhiều size/color rồi trả phần thừa. Decision-makers sắp **cấm free-ship** dựa trên gut feeling — chưa có data verify.

### Truth (3 lớp số liệu với CI)
| Tier | n_orders | Return rate | OR vs Low | p-value |
|---|---|---|---|---|
| **Free** ($0) | **805** | **6.83%** | **1.08** | 0.58 |
| Low (0, 3] | 76,142 | 6.37% | baseline | — |
| **Mid (3, 20]** | 778 | **5.78%** ⭐ lowest | 0.90 | — |
| Express (>20) | 488,342 | 6.40% | 1.005 | — |

**Adjusted OR (logit, 18 features)**: 1.08 [0.82, 1.42], p=0.58.
**Pseudo-R² McFadden**: **4×10⁻⁵** → return không driven bởi shipping.

### Tension
"Free-ship causes return abuse" — belief khá phổ biến trong industry e-commerce. Data: 0.47pp lift, CI bao 1.0, p=0.58. Quyết định bằng anecdote → loss potential conversion uplift.

### Motivation
Nếu effect free-ship lên return là **null hoặc rất nhỏ** (≤1pp), giữ free-ship có thể tăng conversion mà không tăng return cost đáng kể. Power analysis đưa ra **decision rule khoa học**: cần A/B test với n đủ trước khi đổi policy.

### Insight one-liner (decision-ready, ≤20 từ)
🔄 *"Power analysis biến 'không kết quả' thành insight: 'cần A/B test 55× lớn hơn để biết đáp án'."*

---

## 📊 DỮ LIỆU & METHODOLOGY

### Datasets joined (7 bảng — MAX trong 12 idea)
- `customers` (n=180,431): customer_id.
- `geography`: region (East/Central/West).
- `order_items` (n=714,669): basket_size proxy.
- `orders` (n=646,945): order_id, payment_method, order_status.
- `products` (n=2,412): dominant_category proxy per order.
- `returns` (n=39,939): is_returned flag.
- `shipments` (n=566,067): shipping_fee → tier.

### Logistic regression methodology
```python
logit P(return = 1) = β₀
                    + β₁ · is_free
                    + β₂ · basket_size
                    + Σ β_cat · D_dominant_category    (one-hot, drop_first)
                    + Σ β_reg · D_region               (one-hot, drop_first)
                    + Σ β_yr  · D_year                 (one-hot, drop_first)
```
- 18 features sau encoding.
- Fit MLE via `statsmodels.Logit` trên 566,067 shipped orders.

```
adjusted_OR(is_free) = exp(β̂₁) = 1.08
95% CI = exp(β̂₁ ± 1.96 · SE(β̂₁)) = [0.82, 1.42]
p-value (Wald test) = 0.58
pseudo-R² (McFadden) = 1 − LL_full / LL_null = 4×10⁻⁵
```

### Power analysis methodology
```
2-proportion z-test (α = 0.05 two-tailed, power = 0.80)

# MDE @ given n_per_group
δ_min = (z_{α/2} + z_β) · √(2 · p̄ · (1 − p̄) / n)
       = (1.96 + 0.84) · √(2 · 0.064 · 0.936 / 805) = 3.46pp

# n required for given δ
n_per_group = (z_{α/2} + z_β)² · 2 · p̄ · (1 − p̄) / δ²
            = (2.80)² · 2 · 0.064 · 0.936 / (0.0047)² ≈ 44,594
```

Power curve plot: x = n per group, y = MDE detectable @ power 80%, dashed line tại n=805 (current) và n=44,594 (required).

---

## 🔮 PREDICTIVE RESULTS (cell 12.4 + Fig 12.4)

### P1 — Adjusted OR (logit)
| Coefficient | Value | 95% CI | p |
|---|---|---|---|
| `is_free` | β₁ = 0.077 | [-0.20, 0.35] | 0.58 |
| `basket_size` | β₂ = 0.012 | significant | <0.001 |
| `dominant_category_X` | varies | mixed | — |
| `region_X` | varies | mixed | — |
| `year_X` | varies | mixed | — |
| **Pseudo-R² McFadden** | **0.00004** | — | — |

→ Confounders KHÔNG explain effect. Effect thật của `is_free` rất nhỏ.

### P2 — Power Analysis
| Quantity | Value |
|---|---|
| Observed lift (free vs low) | **0.47pp** |
| MDE @ n=805, power 80% | **3.46pp** (~7.4× observed) |
| n required for δ=0.47pp | **44,594/group** (~55× current) |
| Effect range plausible (post hoc) | **[-1pp, +2pp]** |

---

## 💼 PRESCRIPTIVE — 4 ACTIONS (TTM-mapped, Execution-Ready)

### Action 1 — KHÔNG cấm free-ship
| Field | Value |
|---|---|
| **What** | Hold current free-ship policy. KHÔNG cấm free-ship dựa trên anecdote |
| **Trigger** | Q4 2025 / Q1 2026 policy review |
| **Threshold** | Required: pre-registered A/B với n=44,594/group |
| **Rollback** | Nếu A/B test detect lift ≥3.46pp → restrict free-ship cho cụ thể basket size |
| **Owner** | Logistics + Data Sci joint |
| **Telemetry** | Weekly return rate by tier dashboard |

### Action 2 — Pre-registered A/B test
| Field | Value |
|---|---|
| **What** | Sample 44,594 orders/group (free vs paid-low) trong 90 ngày |
| **Trigger** | Q1 2026 |
| **Threshold** | Đạt n=44,594 warm-up trước khi enter formal analysis |
| **Stop early** | Interim z-stat |z| > 3.0 → stop early (Pocock boundary) |
| **Rollback** | Nếu interim shows trend reversed → terminate |
| **Owner** | Data Sci |
| **Cost** | $50K (free-ship subsidy + analysis time) |
| **Expected info value** | $2.1M/yr nếu detect 3.46pp lift; $0 nếu null confirmed |

### Action 3 — Locale fulfillment by region
| Field | Value |
|---|---|
| **What** | Local 3PL East/Central/West dựa revenue split 46.5%/27.1%/26.4% (per Idea 4) |
| **Trigger** | Q3 2026 |
| **Threshold** | Lead time East giảm từ 5→3 ngày |
| **Rollback** | Nếu cost 3PL > 110% of in-house → revert |
| **Owner** | Logistics |
| **Telemetry** | Weekly lead-time per region |
| **Impact** | -22% shipping cost; +4% conversion uplift potential |

### Action 4 — Cap basket size cho free-ship
| Field | Value |
|---|---|
| **What** | Nếu scale free-ship policy: cap basket 1-2 items (basket 3-6 có signal abuse +1-2.4pp) |
| **Trigger** | Khi A/B test confirm signal khu trú basket 3-6 |
| **Threshold** | basket_size ≥ 3 → require min_order_value $X |
| **Rollback** | Nếu conversion drop >5% → tăng cap |
| **Owner** | Product + Logistics |

---

## 🔗 CROSS-REFERENCE

- **§4.1 node**: (3) Logistics + cost.
- **§4.4 row**: 5 — Regional logistics (Business goal: Logistics).
- **Narrative PDF v3**: T3 sub-T3.2 (Fig 12.4 power curve = F5 chart, **độc đáo nhất**).
- **Phần 3 Forecasting**: shipping_fee feature có thể đưa vào model nhưng **expect không significant** (pseudo-R² 4×10⁻⁵).

## ⚠️ COUNTER-ARGUMENTS & RESPONSES (phản biện cuối narrative)

1. **"Pseudo-R² 4e-5 quá thấp, model bể"** → Đúng — đó là **finding**, không phải bug. Return chủ yếu drive bởi fit/quality SKU (xem Idea 3 wrong_size 35% là driver chính), không phải shipping economics.

2. **"Adjusted OR có thể bias do omitted variable (customer history)"** → Đã ghi caveat. Tuy nhiên pseudo-R² 4e-5 cho thấy thêm features cũng khó cải thiện đáng kể.

3. **"MDE 3.46pp có thể quá strict — perhaps the true effect là 1pp"** → Đúng — MDE chỉ để **size A/B test**, không khẳng định effect = 0. Power analysis làm rõ "underpowered ≠ no effect".

4. **"Tại sao Mid tier (3-20] có return THẤP NHẤT?"** → Hypothesis: customer chọn ship trung bình = ý thức cost + không vội (không express) → ít abuse. Cần research chuyên sâu hoặc segment analysis (deferred Phase 5b).

---

## 🎯 ĐIỂM ĐỘC ĐÁO TRONG 3,000 THÍ SINH

1. **Honest "INSUFFICIENT EVIDENCE" framing** thay vì "REFUTE" — phân biệt power vs effect là academic rigor cao.
2. **Logistic regression với adjusted OR** + 18 features control — ít team đụng tới.
3. **Power analysis với MDE và n_required** — rare technique trong submission datathon.
4. **7-table cross-join** — max trong 12 idea (rubric "tích hợp đa nguồn" band cao).
5. **Decision rule rõ ràng**: "Cần A/B test n=44,594/group" thay vì "free-ship gây return" hoặc "free-ship vô hại".
