"""
╔══════════════════════════════════════════════════════════════════╗
║         RETAIL SALES INTELLIGENCE DASHBOARD                     ║
║         Built with Streamlit + Pandas + Plotly                  ║
║         Production-grade portfolio project                      ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Retail Sales Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  THEME & CUSTOM CSS
# ─────────────────────────────────────────────
PALETTE = {
    "bg":        "#0F1117",
    "surface":   "#1A1D27",
    "surface2":  "#22263A",
    "accent":    "#4F8EF7",
    "accent2":   "#7C3AED",
    "green":     "#10B981",
    "red":       "#EF4444",
    "amber":     "#F59E0B",
    "text":      "#E2E8F0",
    "muted":     "#64748B",
    "border":    "#2D3250",
}

PLOTLY_COLORS = [
    "#4F8EF7", "#7C3AED", "#10B981", "#F59E0B",
    "#EF4444", "#EC4899", "#06B6D4", "#84CC16",
]

st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

  html, body, [class*="css"] {{
    font-family: 'DM Sans', sans-serif;
    background-color: {PALETTE['bg']};
    color: {PALETTE['text']};
  }}

  .stApp {{ background-color: {PALETTE['bg']}; }}

  /* Sidebar */
  section[data-testid="stSidebar"] {{
    background: {PALETTE['surface']};
    border-right: 1px solid {PALETTE['border']};
  }}
  section[data-testid="stSidebar"] * {{ color: {PALETTE['text']} !important; }}

  /* Main header */
  .dash-header {{
    background: linear-gradient(135deg, {PALETTE['surface']} 0%, {PALETTE['surface2']} 100%);
    border: 1px solid {PALETTE['border']};
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
  }}
  .dash-header::before {{
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, {PALETTE['accent']}22 0%, transparent 70%);
    border-radius: 50%;
  }}
  .dash-title {{
    font-size: 2rem; font-weight: 700;
    background: linear-gradient(90deg, {PALETTE['accent']}, {PALETTE['accent2']});
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0; letter-spacing: -0.5px;
  }}
  .dash-subtitle {{
    color: {PALETTE['muted']}; font-size: 0.95rem;
    margin-top: 4px; font-weight: 400;
  }}

  /* KPI cards */
  .kpi-card {{
    background: {PALETTE['surface']};
    border: 1px solid {PALETTE['border']};
    border-radius: 14px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
    transition: transform .2s;
  }}
  .kpi-card:hover {{ transform: translateY(-2px); }}
  .kpi-label {{
    font-size: 0.78rem; font-weight: 600; letter-spacing: .08em;
    text-transform: uppercase; color: {PALETTE['muted']};
  }}
  .kpi-value {{
    font-size: 2rem; font-weight: 700; margin: 6px 0 2px;
    font-family: 'DM Mono', monospace;
  }}
  .kpi-delta {{
    font-size: 0.82rem; font-weight: 500;
  }}
  .kpi-icon {{
    position: absolute; right: 20px; top: 20px;
    font-size: 2rem; opacity: .15;
  }}

  /* Section titles */
  .section-title {{
    font-size: 1.15rem; font-weight: 600;
    color: {PALETTE['text']}; margin: 0 0 16px;
    padding-bottom: 10px;
    border-bottom: 1px solid {PALETTE['border']};
  }}

  /* Chart wrappers */
  .chart-card {{
    background: {PALETTE['surface']};
    border: 1px solid {PALETTE['border']};
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 20px;
  }}

  /* Sidebar nav */
  .nav-item {{
    display: flex; align-items: center; gap: 10px;
    padding: 10px 14px; border-radius: 10px;
    cursor: pointer; font-weight: 500; font-size: .92rem;
    transition: background .15s;
    color: {PALETTE['muted']};
  }}
  .nav-item.active {{
    background: {PALETTE['accent']}22;
    color: {PALETTE['accent']};
    border: 1px solid {PALETTE['accent']}44;
  }}

  /* Metric override */
  div[data-testid="metric-container"] {{
    background: {PALETTE['surface']};
    border: 1px solid {PALETTE['border']};
    border-radius: 14px;
    padding: 16px 20px;
  }}
  div[data-testid="metric-container"] label {{
    color: {PALETTE['muted']} !important;
    font-size: .78rem !important;
    text-transform: uppercase; letter-spacing: .08em;
  }}
  div[data-testid="metric-container"] [data-testid="stMetricValue"] {{
    font-family: 'DM Mono', monospace !important;
    color: {PALETTE['text']} !important;
  }}

  /* Selectbox / slider */
  .stSelectbox > div > div,
  .stMultiSelect > div > div {{
    background: {PALETTE['surface2']} !important;
    border-color: {PALETTE['border']} !important;
    color: {PALETTE['text']} !important;
  }}
  .stSlider > div {{ color: {PALETTE['text']}; }}

  /* Download button */
  .stDownloadButton > button {{
    background: linear-gradient(135deg, {PALETTE['accent']}, {PALETTE['accent2']});
    color: white; border: none; border-radius: 10px;
    font-weight: 600; padding: 10px 20px;
    width: 100%; margin-top: 8px;
  }}
  .stDownloadButton > button:hover {{ opacity: .9; }}

  /* Divider */
  hr {{ border-color: {PALETTE['border']} !important; margin: 20px 0; }}

  /* Scrollbar */
  ::-webkit-scrollbar {{ width: 6px; }}
  ::-webkit-scrollbar-track {{ background: {PALETTE['bg']}; }}
  ::-webkit-scrollbar-thumb {{ background: {PALETTE['border']}; border-radius: 3px; }}

  /* Hide Streamlit branding */
  #MainMenu, footer, header {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  DATA GENERATION
# ─────────────────────────────────────────────
@st.cache_data
def generate_dataset(n: int = 5000) -> pd.DataFrame:
    """Generate a realistic retail sales dataset with intentional messy values."""
    rng = np.random.default_rng(42)

    categories  = ["Technology", "Furniture", "Office Supplies", "Clothing", "Electronics"]
    sub_cats    = {
        "Technology":      ["Laptops", "Phones", "Tablets", "Monitors", "Accessories"],
        "Furniture":       ["Chairs", "Desks", "Shelves", "Cabinets", "Sofas"],
        "Office Supplies": ["Paper", "Binders", "Pens", "Staples", "Labels"],
        "Clothing":        ["Shirts", "Trousers", "Jackets", "Shoes", "Hats"],
        "Electronics":     ["Cameras", "Headphones", "Speakers", "TVs", "Printers"],
    }
    regions     = ["West", "East", "Central", "South"]
    segments    = ["Consumer", "Corporate", "Home Office"]
    ship_modes  = ["Standard Class", "Second Class", "First Class", "Same Day"]

    records = []
    for i in range(n):
        cat     = rng.choice(categories)
        sub     = rng.choice(sub_cats[cat])
        region  = rng.choice(regions)
        segment = rng.choice(segments)
        ship    = rng.choice(ship_modes, p=[.60, .20, .15, .05])
        qty     = int(rng.integers(1, 15))

        base_price = {
            "Technology": 800, "Electronics": 500, "Furniture": 300,
            "Clothing": 80,    "Office Supplies": 25,
        }[cat]
        sales   = round(float(rng.lognormal(np.log(base_price), 0.5)) * qty, 2)
        margin  = rng.uniform(-0.05, 0.45)
        profit  = round(sales * margin, 2)

        order_date = datetime(2021, 1, 1) + timedelta(days=int(rng.integers(0, 365*3)))
        ship_date  = order_date + timedelta(days=int(rng.integers(1, 10)))

        records.append({
            "Order ID":        f"ORD-{100000 + i}",
            "Product Name":    f"{sub} {rng.integers(100, 999)}",
            "Category":        cat,
            "Sub-Category":    sub,
            "Region":          region,
            "Customer Segment":segment,
            "Shipping Mode":   ship,
            "Quantity":        qty,
            "Sales":           sales,
            "Profit":          profit,
            "Order Date":      order_date,
            "Ship Date":       ship_date,
        })

    df = pd.DataFrame(records)

    # ── Introduce intentional messiness for cleaning demo ──
    mess_idx = rng.choice(df.index, size=int(n * 0.03), replace=False)
    df.loc[mess_idx[:len(mess_idx)//3], "Sales"]  = np.nan
    df.loc[mess_idx[len(mess_idx)//3:2*len(mess_idx)//3], "Profit"] = np.nan
    df.loc[mess_idx[2*len(mess_idx)//3:], "Region"] = np.nan

    # duplicates
    dup_rows = df.sample(int(n * 0.01), random_state=1)
    df = pd.concat([df, dup_rows], ignore_index=True)

    return df


# ─────────────────────────────────────────────
#  DATA CLEANING
# ─────────────────────────────────────────────
@st.cache_data
def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Full data cleaning pipeline.
    Returns cleaned DataFrame + a report dict.
    """
    report = {}
    raw_shape = df.shape

    # 1. Remove duplicates
    before_dup = len(df)
    df = df.drop_duplicates()
    report["duplicates_removed"] = before_dup - len(df)

    # 2. Handle missing values
    report["missing_before"] = df.isnull().sum().to_dict()
    df["Sales"]  = df["Sales"].fillna(df["Sales"].median())
    df["Profit"] = df["Profit"].fillna(df["Profit"].median())
    df["Region"] = df["Region"].fillna(df["Region"].mode()[0])
    report["missing_after"] = df.isnull().sum().to_dict()

    # 3. Fix data types
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Ship Date"]  = pd.to_datetime(df["Ship Date"],  errors="coerce")
    df["Sales"]      = df["Sales"].astype(float).round(2)
    df["Profit"]     = df["Profit"].astype(float).round(2)
    df["Quantity"]   = df["Quantity"].astype(int)

    # 4. Derived columns
    df["Year"]          = df["Order Date"].dt.year
    df["Month"]         = df["Order Date"].dt.to_period("M").astype(str)
    df["Month_dt"]      = df["Order Date"].dt.to_period("M").dt.to_timestamp()
    df["Profit Margin"] = (df["Profit"] / df["Sales"]).replace([np.inf, -np.inf], 0).round(4)
    df["Order Value"]   = df["Sales"] / df["Quantity"]

    report["raw_shape"]    = raw_shape
    report["clean_shape"]  = df.shape
    return df, report


# ─────────────────────────────────────────────
#  PLOTLY CHART THEME
# ─────────────────────────────────────────────
def chart_layout(fig: go.Figure, title: str = "") -> go.Figure:
    """Apply consistent dark theme to every Plotly figure."""
    fig.update_layout(
        title=dict(text=title, font=dict(size=15, color=PALETTE["text"], family="DM Sans"), x=0, xanchor="left"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color=PALETTE["text"]),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor=PALETTE["border"],
            borderwidth=1,
        ),
        xaxis=dict(gridcolor=PALETTE["border"], linecolor=PALETTE["border"], zerolinecolor=PALETTE["border"]),
        yaxis=dict(gridcolor=PALETTE["border"], linecolor=PALETTE["border"], zerolinecolor=PALETTE["border"]),
        margin=dict(l=10, r=10, t=45, b=10),
        hoverlabel=dict(bgcolor=PALETTE["surface2"], bordercolor=PALETTE["border"], font_family="DM Sans"),
    )
    return fig


# ─────────────────────────────────────────────
#  VISUALIZATION FUNCTIONS
# ─────────────────────────────────────────────

def chart_sales_by_region(df: pd.DataFrame) -> go.Figure:
    agg = df.groupby("Region", as_index=False).agg(
        Sales=("Sales", "sum"), Orders=("Order ID", "count"), Profit=("Profit", "sum")
    ).sort_values("Sales", ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=agg["Region"], x=agg["Sales"],
        orientation="h",
        marker=dict(
            color=agg["Sales"],
            colorscale=[[0, PALETTE["accent2"]], [1, PALETTE["accent"]]],
            showscale=False,
        ),
        text=[f"${v/1e6:.2f}M" for v in agg["Sales"]],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Sales: $%{x:,.0f}<extra></extra>",
    ))
    return chart_layout(fig, "💰 Total Sales by Region")


def chart_profit_by_category(df: pd.DataFrame) -> go.Figure:
    agg = df.groupby("Category", as_index=False).agg(
        Profit=("Profit", "sum"), Sales=("Sales", "sum")
    )
    agg["Margin"] = (agg["Profit"] / agg["Sales"] * 100).round(1)
    agg = agg.sort_values("Profit", ascending=False)
    colors = [PALETTE["green"] if p > 0 else PALETTE["red"] for p in agg["Profit"]]

    fig = go.Figure(go.Bar(
        x=agg["Category"], y=agg["Profit"],
        marker_color=colors,
        text=[f"${p/1e3:.1f}K<br>{m:.1f}%" for p, m in zip(agg["Profit"], agg["Margin"])],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Profit: $%{y:,.0f}<extra></extra>",
    ))
    return chart_layout(fig, "📦 Profit by Category")


def chart_monthly_trend(df: pd.DataFrame) -> go.Figure:
    agg = df.groupby("Month_dt", as_index=False).agg(
        Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "count")
    ).sort_values("Month_dt")

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(
        x=agg["Month_dt"], y=agg["Sales"],
        mode="lines", name="Sales",
        line=dict(color=PALETTE["accent"], width=2.5),
        fill="tozeroy", fillcolor=f'{PALETTE["accent"]}18',
        hovertemplate="Sales: $%{y:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=agg["Month_dt"], y=agg["Profit"],
        mode="lines", name="Profit",
        line=dict(color=PALETTE["green"], width=2, dash="dot"),
        hovertemplate="Profit: $%{y:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        x=agg["Month_dt"], y=agg["Orders"],
        name="Orders", opacity=0.25,
        marker_color=PALETTE["amber"],
        yaxis="y2",
        hovertemplate="Orders: %{y}<extra></extra>",
    ), secondary_y=True)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color=PALETTE["text"]),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=PALETTE["border"], borderwidth=1),
        xaxis=dict(gridcolor=PALETTE["border"], linecolor=PALETTE["border"]),
        yaxis=dict(gridcolor=PALETTE["border"], linecolor=PALETTE["border"]),
        yaxis2=dict(gridcolor="rgba(0,0,0,0)", showgrid=False),
        margin=dict(l=10, r=10, t=45, b=10),
        title=dict(text="📅 Monthly Sales & Profit Trend", font=dict(size=15, color=PALETTE["text"]), x=0),
        hoverlabel=dict(bgcolor=PALETTE["surface2"], font_family="DM Sans"),
    )
    return fig


def chart_customer_segment(df: pd.DataFrame) -> go.Figure:
    agg = df.groupby("Customer Segment", as_index=False).agg(
        Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "count")
    )
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "bar"}]])
    fig.add_trace(go.Pie(
        labels=agg["Customer Segment"], values=agg["Sales"],
        hole=.55,
        marker=dict(colors=PLOTLY_COLORS[:3]),
        textinfo="label+percent",
        hovertemplate="<b>%{label}</b><br>Sales: $%{value:,.0f}<extra></extra>",
        textfont_size=12,
    ), row=1, col=1)
    fig.add_trace(go.Bar(
        x=agg["Customer Segment"], y=agg["Profit"],
        marker=dict(color=PLOTLY_COLORS[:3]),
        text=[f"${p/1e3:.1f}K" for p in agg["Profit"]],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Profit: $%{y:,.0f}<extra></extra>",
    ), row=1, col=2)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color=PALETTE["text"]),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        showlegend=False,
        title=dict(text="👥 Customer Segment Analysis", font=dict(size=15, color=PALETTE["text"]), x=0),
        margin=dict(l=10, r=10, t=45, b=10),
        xaxis2=dict(gridcolor=PALETTE["border"]),
        yaxis2=dict(gridcolor=PALETTE["border"]),
        hoverlabel=dict(bgcolor=PALETTE["surface2"], font_family="DM Sans"),
    )
    return fig


def chart_top_products(df: pd.DataFrame) -> go.Figure:
    agg = df.groupby("Product Name", as_index=False).agg(
        Sales=("Sales", "sum"), Profit=("Profit", "sum")
    ).sort_values("Sales", ascending=False).head(10)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=agg["Product Name"][::-1], x=agg["Sales"][::-1],
        orientation="h", name="Sales",
        marker=dict(color=PALETTE["accent"], opacity=.85),
        hovertemplate="<b>%{y}</b><br>Sales: $%{x:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        y=agg["Product Name"][::-1], x=agg["Profit"][::-1],
        orientation="h", name="Profit",
        marker=dict(color=PALETTE["green"], opacity=.85),
        hovertemplate="<b>%{y}</b><br>Profit: $%{x:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        barmode="overlay",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color=PALETTE["text"]),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=PALETTE["border"], borderwidth=1),
        xaxis=dict(gridcolor=PALETTE["border"]),
        yaxis=dict(gridcolor="rgba(0,0,0,0)"),
        title=dict(text="🏆 Top 10 Products by Sales", font=dict(size=15, color=PALETTE["text"]), x=0),
        margin=dict(l=10, r=10, t=45, b=10),
        hoverlabel=dict(bgcolor=PALETTE["surface2"], font_family="DM Sans"),
    )
    return fig


def chart_shipping_mode(df: pd.DataFrame) -> go.Figure:
    agg = df.groupby("Shipping Mode", as_index=False).agg(
        Orders=("Order ID", "count"),
        Sales=("Sales", "sum"),
        Avg_Days=("Ship Date", lambda x: (
            (df.loc[x.index, "Ship Date"] - df.loc[x.index, "Order Date"])
            .dt.days.mean()
        )),
    )
    fig = make_subplots(rows=1, cols=2,
        subplot_titles=("Order Distribution", "Avg. Sales per Order"))
    fig.add_trace(go.Pie(
        labels=agg["Shipping Mode"], values=agg["Orders"],
        hole=.5,
        marker=dict(colors=PLOTLY_COLORS),
        textinfo="label+percent",
        hovertemplate="<b>%{label}</b><br>Orders: %{value:,}<extra></extra>",
    ), row=1, col=1)
    fig.add_trace(go.Bar(
        x=agg["Shipping Mode"],
        y=(agg["Sales"] / agg["Orders"]).round(0),
        marker=dict(color=PLOTLY_COLORS),
        text=[(agg["Sales"] / agg["Orders"]).round(0).astype(int)],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Avg Sales: $%{y:,.0f}<extra></extra>",
    ), row=1, col=2)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color=PALETTE["text"]),
        showlegend=False,
        title=dict(text="🚚 Shipping Mode Analysis", font=dict(size=15, color=PALETTE["text"]), x=0),
        margin=dict(l=10, r=10, t=55, b=10),
        xaxis2=dict(gridcolor=PALETTE["border"]),
        yaxis2=dict(gridcolor=PALETTE["border"]),
        hoverlabel=dict(bgcolor=PALETTE["surface2"], font_family="DM Sans"),
    )
    fig.update_annotations(font_color=PALETTE["muted"])
    return fig


def chart_profit_vs_sales(df: pd.DataFrame) -> go.Figure:
    sample = df.sample(min(1500, len(df)), random_state=42)
    fig = px.scatter(
        sample, x="Sales", y="Profit",
        color="Category", size="Quantity",
        size_max=20, opacity=0.7,
        color_discrete_sequence=PLOTLY_COLORS,
        hover_data={"Product Name": True, "Region": True, "Quantity": True},
        labels={"Sales": "Sales ($)", "Profit": "Profit ($)"},
    )
    # Zero-profit reference line
    fig.add_hline(y=0, line_dash="dash", line_color=PALETTE["red"], opacity=.5)
    return chart_layout(fig, "🔍 Profit vs Sales Scatter")


def chart_heatmap(df: pd.DataFrame) -> go.Figure:
    pivot = df.pivot_table(
        values="Sales", index="Category", columns="Region",
        aggfunc="sum", fill_value=0,
    )
    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale=[[0, PALETTE["surface2"]], [0.5, PALETTE["accent2"]], [1, PALETTE["accent"]]],
        text=[[f"${v/1e3:.0f}K" for v in row] for row in pivot.values],
        texttemplate="%{text}",
        hovertemplate="<b>%{y}</b> / %{x}<br>Sales: %{z:,.0f}<extra></extra>",
    ))
    return chart_layout(fig, "🗺️ Sales Heatmap: Category × Region")


# ─────────────────────────────────────────────
#  KPI HELPERS
# ─────────────────────────────────────────────
def kpi_card(label: str, value: str, delta: str, icon: str, color: str) -> str:
    return f"""
    <div class="kpi-card">
      <div class="kpi-icon">{icon}</div>
      <div class="kpi-label">{label}</div>
      <div class="kpi-value" style="color:{color}">{value}</div>
      <div class="kpi-delta" style="color:{PALETTE['muted']}">{delta}</div>
    </div>
    """


def fmt_currency(v: float) -> str:
    if abs(v) >= 1e6:
        return f"${v/1e6:.2f}M"
    if abs(v) >= 1e3:
        return f"${v/1e3:.1f}K"
    return f"${v:.0f}"


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
def render_sidebar(df_clean: pd.DataFrame) -> dict:
    with st.sidebar:
        st.markdown("""
        <div style="padding:12px 0 20px;">
          <div style="font-size:1.3rem;font-weight:700;color:#4F8EF7">📊 Retail Intel</div>
          <div style="font-size:.8rem;color:#64748B;margin-top:2px">Sales Intelligence v1.0</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Navigation ──
        pages = {
            "🏠 Overview":        "overview",
            "📈 Sales Analytics": "sales",
            "💡 Profit Analysis": "profit",
            "🔍 Deep Dive":       "deep",
            "🧹 Data Quality":    "quality",
        }
        page = st.radio("Navigation", list(pages.keys()), label_visibility="collapsed")

        st.markdown("---")
        st.markdown('<div style="font-size:.78rem;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:#64748B;margin-bottom:10px">Filters</div>', unsafe_allow_html=True)

        # Region
        all_regions = sorted(df_clean["Region"].unique())
        sel_region  = st.multiselect("Region", all_regions, default=all_regions)

        # Category
        all_cats  = sorted(df_clean["Category"].unique())
        sel_cat   = st.multiselect("Category", all_cats, default=all_cats)

        # Segment
        all_segs  = sorted(df_clean["Customer Segment"].unique())
        sel_seg   = st.multiselect("Customer Segment", all_segs, default=all_segs)

        # Date range
        min_d = df_clean["Order Date"].min().date()
        max_d = df_clean["Order Date"].max().date()
        date_range = st.date_input("Order Date Range", value=(min_d, max_d),
                                   min_value=min_d, max_value=max_d)

        st.markdown("---")
        # Dataset info
        st.markdown(f"""
        <div style="font-size:.8rem;color:#64748B;line-height:1.8">
          <div>📁 Records: <b style="color:#E2E8F0">{len(df_clean):,}</b></div>
          <div>📅 Date span: <b style="color:#E2E8F0">{min_d.year}–{max_d.year}</b></div>
          <div>🏷️ Categories: <b style="color:#E2E8F0">{df_clean['Category'].nunique()}</b></div>
        </div>
        """, unsafe_allow_html=True)

    return {
        "page":       pages[page],
        "regions":    sel_region,
        "categories": sel_cat,
        "segments":   sel_seg,
        "date_range": date_range,
    }


# ─────────────────────────────────────────────
#  FILTER DATA
# ─────────────────────────────────────────────
def apply_filters(df: pd.DataFrame, f: dict) -> pd.DataFrame:
    mask = (
        df["Region"].isin(f["regions"]) &
        df["Category"].isin(f["categories"]) &
        df["Customer Segment"].isin(f["segments"])
    )
    if len(f["date_range"]) == 2:
        start, end = f["date_range"]
        mask &= (df["Order Date"].dt.date >= start) & (df["Order Date"].dt.date <= end)
    return df[mask].copy()


# ─────────────────────────────────────────────
#  PAGE: OVERVIEW
# ─────────────────────────────────────────────
def page_overview(df: pd.DataFrame):
    total_sales   = df["Sales"].sum()
    total_profit  = df["Profit"].sum()
    total_orders  = df["Order ID"].nunique()
    avg_order_val = df["Sales"].mean()
    profit_margin = total_profit / total_sales * 100 if total_sales else 0

    # Header
    st.markdown("""
    <div class="dash-header">
      <div class="dash-title">Retail Sales Intelligence Dashboard</div>
      <div class="dash-subtitle">Real-time insights across regions, categories and customer segments</div>
    </div>
    """, unsafe_allow_html=True)

    # KPI row
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(kpi_card("Total Sales", fmt_currency(total_sales),
                    f"{len(df):,} transactions", "💰", PALETTE["accent"]), unsafe_allow_html=True)
    with c2:
        color = PALETTE["green"] if total_profit > 0 else PALETTE["red"]
        st.markdown(kpi_card("Total Profit", fmt_currency(total_profit),
                    f"{profit_margin:.1f}% margin", "📈", color), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card("Total Orders", f"{total_orders:,}",
                    f"Unique order IDs", "🛒", PALETTE["amber"]), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card("Avg Order Value", fmt_currency(avg_order_val),
                    "Per transaction", "🎯", PALETTE["accent2"]), unsafe_allow_html=True)
    with c5:
        color = PALETTE["green"] if profit_margin > 10 else PALETTE["amber"]
        st.markdown(kpi_card("Profit Margin", f"{profit_margin:.1f}%",
                    "Overall blended", "📊", color), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 1
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(chart_sales_by_region(df), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(chart_profit_by_category(df), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # Row 2 – full width trend
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(chart_monthly_trend(df), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    # Download
    _download_widget(df)


# ─────────────────────────────────────────────
#  PAGE: SALES ANALYTICS
# ─────────────────────────────────────────────
def page_sales(df: pd.DataFrame):
    st.markdown('<div class="section-title">📈 Sales Analytics</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(chart_customer_segment(df), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(chart_shipping_mode(df), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(chart_top_products(df), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    _download_widget(df)


# ─────────────────────────────────────────────
#  PAGE: PROFIT ANALYSIS
# ─────────────────────────────────────────────
def page_profit(df: pd.DataFrame):
    st.markdown('<div class="section-title">💡 Profit Analysis</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(chart_profit_vs_sales(df), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(chart_heatmap(df), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    # Margin by category table
    st.markdown('<div class="section-title" style="margin-top:8px">Margin Summary by Category</div>', unsafe_allow_html=True)
    summary = df.groupby("Category").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "count"),
    ).reset_index()
    summary["Margin %"] = (summary["Profit"] / summary["Sales"] * 100).round(1)
    summary["Sales"]    = summary["Sales"].map(fmt_currency)
    summary["Profit"]   = summary["Profit"].map(fmt_currency)
    st.dataframe(
        summary.sort_values("Margin %", ascending=False),
        use_container_width=True, hide_index=True,
    )
    _download_widget(df)


# ─────────────────────────────────────────────
#  PAGE: DEEP DIVE
# ─────────────────────────────────────────────
def page_deep(df: pd.DataFrame):
    st.markdown('<div class="section-title">🔍 Deep Dive Explorer</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        x_axis = st.selectbox("X Axis", ["Sales", "Profit", "Quantity", "Order Value"])
    with col2:
        y_axis = st.selectbox("Y Axis", ["Profit", "Sales", "Quantity", "Order Value"], index=0)

    color_by = st.selectbox("Colour by", ["Category", "Region", "Customer Segment", "Shipping Mode"])

    sample = df.sample(min(2000, len(df)), random_state=7)
    fig = px.scatter(
        sample, x=x_axis, y=y_axis, color=color_by,
        size="Quantity", size_max=18, opacity=.7,
        color_discrete_sequence=PLOTLY_COLORS,
        hover_data={"Product Name": True, "Region": True},
    )
    fig = chart_layout(fig, f"{y_axis} vs {x_axis} coloured by {color_by}")
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    # Box plots
    fig2 = px.box(
        df, x="Category", y="Profit Margin",
        color="Category", color_discrete_sequence=PLOTLY_COLORS,
        points="outliers",
    )
    fig2 = chart_layout(fig2, "Profit Margin Distribution by Category")
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    _download_widget(df)


# ─────────────────────────────────────────────
#  PAGE: DATA QUALITY
# ─────────────────────────────────────────────
def page_quality(df_raw: pd.DataFrame, report: dict):
    st.markdown('<div class="section-title">🧹 Data Quality Report</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Raw Records",     f"{report['raw_shape'][0]:,}")
    with c2:
        st.metric("After Cleaning",  f"{report['clean_shape'][0]:,}")
    with c3:
        st.metric("Duplicates Removed", f"{report['duplicates_removed']:,}")

    st.markdown("### Missing Values (before cleaning)")
    mv = {k: v for k, v in report["missing_before"].items() if v > 0}
    if mv:
        mv_df = pd.DataFrame({"Column": list(mv.keys()), "Missing": list(mv.values())})
        mv_df["%"] = (mv_df["Missing"] / report["raw_shape"][0] * 100).round(2)
        st.dataframe(mv_df, use_container_width=True, hide_index=True)
    else:
        st.success("No missing values detected.")

    st.markdown("### Data Type Summary (clean dataset)")
    dtype_df = pd.DataFrame({
        "Column": df_raw.columns.tolist(),
        "Type":   [str(t) for t in df_raw.dtypes.tolist()],
        "Non-Null": df_raw.notnull().sum().tolist(),
        "Unique": df_raw.nunique().tolist(),
    })
    st.dataframe(dtype_df, use_container_width=True, hide_index=True)

    st.markdown("### Raw Data Preview (first 100 rows)")
    st.dataframe(df_raw.head(100), use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
#  DOWNLOAD WIDGET
# ─────────────────────────────────────────────
def _download_widget(df: pd.DataFrame):
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<div style="color:{PALETTE["muted"]};font-size:.85rem">📥 Download filtered dataset ({len(df):,} rows)</div>',
                    unsafe_allow_html=True)
    with col2:
        buf = io.BytesIO()
        df.to_csv(buf, index=False)
        st.download_button(
            label="Export CSV",
            data=buf.getvalue(),
            file_name=f"retail_sales_filtered_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
        )


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    # Load & clean
    with st.spinner("Loading dataset…"):
        raw_df          = generate_dataset(5000)
        clean_df, report = clean_data(raw_df)

    # Sidebar filters
    filters = render_sidebar(clean_df)

    # Apply filters
    df_filtered = apply_filters(clean_df, filters)

    if df_filtered.empty:
        st.warning("⚠️ No data matches current filters. Please adjust the sidebar.")
        return

    # Route pages
    page = filters["page"]
    if page == "overview":
        page_overview(df_filtered)
    elif page == "sales":
        page_sales(df_filtered)
    elif page == "profit":
        page_profit(df_filtered)
    elif page == "deep":
        page_deep(df_filtered)
    elif page == "quality":
        page_quality(clean_df, report)


if __name__ == "__main__":
    main()
