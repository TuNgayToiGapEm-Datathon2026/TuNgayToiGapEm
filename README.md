# TuNgayToiGapEm — Datathon 2026 · VinUniversity

**Đội:** Đỗ Minh Hiển (Trưởng nhóm) · Ngô Văn Trường Phúc (ML) · Đoàn Quốc Kiên (Insights) · Phạm Nguyễn Văn Đồng (Analyst)

**Kaggle:** [Competition Link](https://www.kaggle.com) | **Seed:** `42` | **Ngày nộp:** 2026-05-01

---

## Cấu trúc thư mục

```
TuNgayToiGapEm/
│
├── phan_1_trac_nghiem/          # Phần 1 — Trắc nghiệm (10 câu)
│   ├── 02_mcq.ipynb             # Notebook tính toán & đáp án 10 MCQ
│   └── Part1.md                 # Đề bài phần 1
│
├── phan_2_eda/                  # Phần 2 — Phân tích khám phá (EDA)
│   └── outputs/
│       ├── idea_1/              # Cohort & Customer Lifecycle
│       ├── idea_5/              # Product Category Performance
│       ├── idea_6/              # Web Traffic Funnel
│       ├── idea_7/              # Payment & Device Behaviour
│       ├── idea_8/              # Review–Return Correlation
│       ├── idea_9/              # Discount Cannibalization
│       ├── idea_10/             # Seasonality & STL (insight chính)
│       │   ├── 10_Seasonality_Complete_Analysis.ipynb
│       │   └── outputs/         # Charts + CSV kết quả
│       ├── idea_11/             # Margin Segment Analysis
│       └── idea_12/             # Shipping Return Analysis
│
├── phan_3_model/                # Phần 3 — Mô hình dự báo
│   ├── scripts/                 # Source code pipeline training & prediction
│   ├── plots/                   # Charts đánh giá kết quả (SHAP, CV, Forecast)
│   └── Part3.md                 # Đặc tả bài toán & pipeline
│
├── data/
│   └── datathon-2026-round-1/   # 14 CSV gốc (không sửa)
│       ├── sales.csv            # Target: Revenue + COGS hàng ngày
│       ├── orders.csv
│       ├── products.csv
│       └── ...                  # (11 file còn lại)
│
├── requirements.txt             # Dependencies
└── README.md
```

---

## Hướng dẫn chạy lại kết quả

### Yêu cầu

```bash
pip install -r requirements.txt
# pandas · numpy · scikit-learn · lightgbm · prophet · statsmodels
# jupyterlab · matplotlib · seaborn
```

### Phần 1 — Trắc nghiệm (10 MCQ)

```bash
cd phan_1_trac_nghiem/
jupyter notebook 02_mcq.ipynb
# Restart Kernel → Run All
# Đáp án in ra cuối notebook
```

### Phần 2 — EDA & Insights

Mỗi idea có 1 notebook độc lập. Chạy theo thứ tự tùy ý:

```bash
# Ví dụ: idea chính về mùa vụ
cd phan_2_eda/outputs/idea_10/
jupyter notebook 10_Seasonality_Complete_Analysis.ipynb
# Restart Kernel → Run All
```

Kết quả (chart + CSV) tự động lưu vào `outputs/` cùng thư mục.

### Phần 3 — Mô hình dự báo (Revenue & COGS, 2023–2024)

> **Pipeline:** `sales.csv` → log-transform → Feature engineering (Fourier, promo flags, Tết window) → Ensemble (Prophet + TimeMixer + LightGBM) → 3-fold Expanding Window CV (step=365, horizon=548 ngày) → `submission.csv`

```bash
cd phan_3_model/
jupyter notebook forecast_pipeline.ipynb
# Restart Kernel → Run All
# Output: submission.csv (548 dòng, khớp sample_submission.csv)
```

**Kết quả CV thực tế:**

| Fold | Revenue MAE | Revenue R² | COGS/Rev R² |
|------|-------------|------------|-------------|
| Fold 0 | 1.133.645 | 0.140 | 0.991 |
| Fold 1 | 521.267 | 0.772 | 0.992 |
| Fold 2 | 557.154 | 0.759 | 0.989 |
| **MEAN** | **737.355** | **0.557** | **0.991** |

*Fold 0 thấp vì train trước changepoint 2019; Fold 1–2 ổn định R²>0,75.*

---

## Tính tái lập (Reproducibility)

- `SEED = 42` — set nhất quán ở tất cả notebook (`numpy`, `random`, `lightgbm random_state`)
- Chỉ dùng 14 CSV gốc từ ban tổ chức — **không** dữ liệu ngoài
- GitHub Actions CI: mỗi push auto-run toàn bộ pipeline và kiểm tra output

```bash
# Clone & chạy lại từ đầu
git clone https://github.com/TuNgayToiGapEm-Datathon2026/TuNgayToiGapEm
cd TuNgayToiGapEm
pip install -r requirements.txt
# Mở từng notebook theo thứ tự: Phần 1 → Phần 2 → Phần 3
```