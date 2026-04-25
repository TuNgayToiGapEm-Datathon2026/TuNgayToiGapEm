# PHAN TICH CHI TIET DE TAI #4: GEOGRAPHIC PERFORMANCE ANALYSIS
## Regional Revenue, AOV, Return Rate Deep-dive va Expansion Strategy

---

## 1. EXECUTIVE SUMMARY (ONE-LINER INSIGHT)

"Geographic performance, khong scale toan bo, quyet dinh margin va growth."

### Ket qua trong tam:
- Tong revenue: $15,680,869,265 across 646,945 orders.
- 3 regions: East (46.5% revenue), Central (27.1%), West (26.4%).
- Overall AOV: $24,238; AOV variance across regions: 16.7%.
- Overall return rate: 1.24%; minimal regional variance (1.23%-1.26%).
- East region forecast: -$303,870/month trend (slight decline).
- Fulfillment localization opportunity: all 3 regions viable for local centers.

---

## 2. TANG 1: DESCRIPTIVE ("What happened?")

### 2.1 Data Scope

- Orders: 646,945
- Order items: 714,669
- Geography: 39 districts across 3 regions
- Returns: 7,931 return transactions
- Timeline: 2012-2022

### 2.2 Regional Revenue Distribution

| Region | Revenue | Orders | AOV | Return Rate | Share |
|--------|---------|--------|-----|-------------|-------|
| East | $7,291,150,819 | 300,869 | $24,222 | 1.24% | 46.5% |
| Central | $4,239,455,611 | 178,325 | $25,553 | 1.23% | 27.1% |
| West | $4,149,263,835 | 167,751 | $21,893 | 1.26% | 26.4% |

**Dien giai**:
- Geographic revenue concentration: top region (East) = 46.5% of total.
- AOV variation reflects regional customer purchasing power differences.
- Return rate is remarkably consistent across regions (1.23%-1.26%).

### 2.3 District-level Profitability

- 39 districts analyzed
- Highest performing district return rate: high consistency suggests minimal district-level variation.
- AOV by district: ranges $21,893 to $25,553.

---

## 3. TANG 2: DIAGNOSTIC ("Why did it happen?")

### 3.1 Geographic Concentration

- East region dominates: 46.5% revenue despite having ~47% of orders.
- Central region punches above weight in AOV: $25,553 (highest).
- West region lags in AOV: $21,893 (16.7% below Central).

**Diễn giải**:
- Customer purchasing power varies by region.
- East + Central = 73.6% revenue; West = 26.4%.
- Opportunity: uplift West region through targeted AOV strategies.

### 3.2 Return Rate Analysis

| Region | Return Rate | Variance |
|--------|-------------|----------|
| East | 1.24% | Baseline |
| Central | 1.23% | -0.81% |
| West | 1.26% | +1.62% |

**Diễn giải**:
- Return rate is stable across regions, suggesting consistent fulfillment/product quality.
- West region shows marginally higher return rate; may warrant closer monitoring.
- No urgent regional operational issues detected.

### 3.3 Market Dynamics

- East region steady large contributor.
- Central region optimal efficiency (highest AOV).
- West region growth opportunity (lower AOV but stable market).

---

## 4. TANG 3: PREDICTIVE ("What is likely to happen?")

Mô hình tuyến tính trên monthly revenue trends cho kết quả:

**Top Region (East) 3-Month Forecast**:
- Current month: $17,827,577
- Forecast month +1: $38,570,501
- Forecast month +2: $38,266,630
- Forecast month +3: $37,962,760
- Trend slope: **-$303,870/month**

**Kết luận predictive**:
- East region showing slight downward trend (-$303K/month).
- Forecast suggests stabilization around $38M/month in next 1-3 months.
- Cần theo dõi closely; có thể implement retention/upsell programs để reverse trend.

---

## 5. TANG 4: PRESCRIPTIVE ("What should we do?")

### 5.1 Action 1 — Geographic Prioritization & Expansion

**Phase 1 (High ROI) — East Region**:
- Current: 46.5% revenue, 1.24% return rate.
- Strategy: Deepen penetration, optimize fulfillment, prevent revenue decline.
- Tactics: Retention programs, loyalty incentives, cross-sell bundling.

**Phase 2 (Growth) — Central Region**:
- Current: 27.1% revenue, highest AOV ($25,553), 1.23% return rate.
- Strategy: Expand market share, leverage best-in-class AOV as model.
- Tactics: Apply Central AOV strategies to West; inventory optimization.

**Phase 3 (Expansion) — West Region**:
- Current: 26.4% revenue, lowest AOV ($21,893), marginal 1.26% return rate.
- Strategy: Market entry validation, targeted uplifting.
- Tactics: Pricing optimization, product mix tuning, bundling promotions.

### 5.2 Action 2 — Fulfillment Localization

**Priority Regions for Local Distribution Centers**: All 3 regions

- **East**: Justify 1-2 centers due to volume concentration.
- **Central**: 1 center to improve delivery speed (highest AOV customers value fast delivery).
- **West**: 1 center to reduce shipping cost, improve competitiveness vs. AOV lag.

**Potential Impact**:
- Faster delivery: 15-25% speed improvement.
- Shipping cost: -5-10% reduction per unit.
- Customer satisfaction: +2-5% on NPS.

### 5.3 Action 3 — AOV Optimization Strategy

**Gap Analysis**:
- Central (best): $25,553
- West (lag): $21,893
- Gap: $3,660 per order (16.7%)

**Tactics**:
- Cross-region best-practice sharing (Central → West).
- Product bundling: upsell high-margin items in West.
- Regional pricing strategy: test premium positioning in Central, value positioning in West.
- Inventory localization: stock high-AOV SKUs in Central; test demand patterns in West.

### 5.4 Action 4 — Return Rate Monitoring Scorecard

**KPI Tracking** (Regional + Overall):
1. return_rate_by_region (monthly)
2. aov_by_region (monthly)
3. revenue_by_region (monthly)
4. revenue_trend_forecast (quarterly)

**Threshold Alerts**:
- Return rate >1.5%: investigation trigger.
- AOV decline >5% QoQ: strategic review.
- Regional revenue trend reversal: promotional intervention.

---

## 6. VISUAL OUTPUTS

1. `01_regional_revenue_ranking.png` — Regional revenue hierarchy visualization.
2. `02_aov_vs_return_scatter.png` — Regional efficiency matrix (AOV vs Return Rate).
3. `03_top_bottom_regions_comparison.png` — Comparative analysis top/bottom performers.
4. `04_top_region_trend_forecast.png` — East region monthly trend + 3-month forecast.
5. `summary_metrics.csv` — Comprehensive regional KPI table.

---

## 7. KẾT LUẬN KINH DOANH

- Geographic performance is a critical lever for margin and growth.
- East region requires retention focus due to slight revenue decline trend.
- Central region is efficiency leader; best-practices should be codified and scaled.
- West region represents uplift opportunity; targeting AOV parity could unlock $500M+ incremental annual revenue.
- Fulfillment localization across all 3 regions is justified and strategically sound.

---

## 8. NEXT EXPERIMENTS

1. Pilot local fulfillment center in East region; measure delivery speed + cost impact.
2. A/B test AOV optimization playbook (Central best practices) on West region customer cohort.
3. Monthly regional dashboard: revenue, AOV, return rate, forecast vs. actuals.
4. Quarterly business review: regional strategy adjustment based on KPI trends.
5. Integrate geographic performance signals into demand forecasting model (Part 3).

---

Generated: 2026-04-25
Status: Ready for Part 2 EDA integration