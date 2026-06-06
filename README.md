# Retail-sales-intelligence-dashboard
# 📊 Retail Sales Intelligence Dashboard

> A production-grade analytics dashboard built with **Streamlit + Pandas + Plotly**  
> Designed as a portfolio-quality project for data analysts and data engineers.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-5.19%2B-3F4F75?logo=plotly)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

### 🏠 Overview Dashboard
- **5 KPI Cards**: Total Sales, Total Profit, Total Orders, Average Order Value, Profit Margin
- **Sales by Region** — horizontal bar chart with gradient fill
- **Profit by Category** — bar chart with positive/negative colour coding
- **Monthly Sales & Profit Trend** — dual-axis combo chart (line + bar)

### 📈 Sales Analytics
- **Customer Segment Analysis** — pie + bar hybrid layout
- **Shipping Mode Analysis** — order distribution + avg sales comparison
- **Top 10 Products by Sales** — overlapping bar chart (Sales vs Profit)

### 💡 Profit Analysis
- **Profit vs Sales Scatter** — bubble chart coloured by category
- **Category × Region Heatmap** — interactive sales heatmap
- **Margin Summary Table** — sortable data table

### 🔍 Deep Dive Explorer
- **Dynamic Scatter Plot** — user-selectable X/Y axes + colour dimension
- **Box Plot** — profit margin distribution by category

### 🧹 Data Quality Report
- Before/after cleaning metrics
- Missing value breakdown
- Data type summary
- Raw data preview

---

## 🗂️ Project Structure

```
retail_dashboard/
├── app.py                    # Main Streamlit application (~550 lines)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── .streamlit/
    └── config.toml           # Streamlit theme & server config
```

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/retail-sales-dashboard.git
cd retail-sales-dashboard
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the dashboard
```bash
streamlit run app.py
```

The app opens at **http://localhost:8501** 🎉

---

## 🧹 Data Cleaning Pipeline

The application runs a full cleaning pipeline on load:

| Step | Action |
|------|--------|
| **Duplicates** | `drop_duplicates()` — removes exact row duplicates |
| **Missing Values** | Numeric columns → filled with median; Categorical → filled with mode |
| **Data Types** | Dates → `pd.to_datetime`; Sales/Profit → `float64`; Quantity → `int64` |
| **Derived Features** | Year, Month period, Profit Margin %, Order Value per unit |

---

## 🎛️ Interactive Filters (Sidebar)

| Filter | Type | Description |
|--------|------|-------------|
| **Region** | Multi-select | West, East, Central, South |
| **Category** | Multi-select | 5 product categories |
| **Customer Segment** | Multi-select | Consumer, Corporate, Home Office |
| **Order Date Range** | Date slider | 2021–2023 data range |

All charts and KPIs update reactively when filters change.

---

## 📊 Dataset Schema

The dashboard generates a synthetic but realistic retail dataset:

| Column | Type | Description |
|--------|------|-------------|
| `Order ID` | string | Unique order identifier |
| `Product Name` | string | Sub-category + SKU number |
| `Category` | string | Technology, Furniture, Office Supplies, Clothing, Electronics |
| `Sub-Category` | string | 5 sub-categories per category |
| `Region` | string | West / East / Central / South |
| `Customer Segment` | string | Consumer / Corporate / Home Office |
| `Shipping Mode` | string | Standard / Second / First / Same Day |
| `Quantity` | int | Units ordered (1–14) |
| `Sales` | float | Revenue in USD |
| `Profit` | float | Net profit in USD |
| `Order Date` | datetime | Order placement date |
| `Ship Date` | datetime | Shipment dispatch date |

> **Note:** The generator intentionally injects ~3% missing values and ~1% duplicates to demonstrate the cleaning pipeline.

---

## 🎨 Design System

| Token | Value |
|-------|-------|
| Background | `#0F1117` |
| Surface | `#1A1D27` |
| Accent Blue | `#4F8EF7` |
| Accent Purple | `#7C3AED` |
| Success Green | `#10B981` |
| Warning Amber | `#F59E0B` |
| Danger Red | `#EF4444` |
| Font | DM Sans + DM Mono |

---

## 📥 Export

Use the **Export CSV** button at the bottom of any page to download the currently filtered dataset as a timestamped CSV file.

---

## 🛠️ Tech Stack

| Library | Version | Purpose |
|---------|---------|---------|
| `streamlit` | ≥ 1.32 | UI framework & reactivity |
| `pandas` | ≥ 2.1 | Data manipulation & aggregation |
| `numpy` | ≥ 1.26 | Numerical operations & synthetic data |
| `plotly` | ≥ 5.19 | All interactive visualisations |

---

## 🤝 Contributing

Pull requests are welcome! For major changes, open an issue first to discuss what you'd like to change.

---

## 📄 License

MIT © 2024 — free to use and adapt for your own portfolio projects.
