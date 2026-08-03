import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import base64
import textwrap
from pathlib import Path
from sklearn.decomposition import PCA

# -----------------------------------------------------------------------------
# 1. PAGE & THEME CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="HydroFoundation Basin Explorer",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Glassmorphism CSS Injector
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0b0f19;
    color: #e2e8f0;
}

#MainMenu, footer, header, [data-testid="stSidebar"] { display: none !important; }

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 1400px;
}

div[data-testid="stSelectbox"] > label {
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    color: #38bdf8 !important;
    text-align: center;
    width: 100%;
}

div[data-testid="stSelectbox"] > div {
    max-width: 320px;
    margin: 0 auto;
    background: rgba(15, 23, 42, 0.8) !important;
    border: 1px solid rgba(56, 189, 248, 0.3) !important;
    border-radius: 10px !important;
    color: #f8fafc !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
}

.section-header {
    background: linear-gradient(90deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.6) 100%);
    border-left: 4px solid #38bdf8;
    padding: 0.8rem 1.2rem;
    border-radius: 8px;
    margin: 2rem 0 1rem 0;
    font-size: 1.25rem;
    font-weight: 700;
    color: #f8fafc;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.glass-card {
    background: rgba(15, 23, 42, 0.65);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 1.2rem;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}

.img-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    background: rgba(15, 23, 42, 0.65);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 0.8rem;
    margin: 0 auto;
    transition: transform 0.3s ease;
}
.img-card:hover {
    transform: scale(1.02);
    border-color: rgba(56, 189, 248, 0.4);
}
.img-card img {
    border-radius: 8px;
    width: 100%;
    height: auto;
    object-fit: cover;
}
.img-title {
    font-size: 0.9rem;
    font-weight: 600;
    color: #94a3b8;
    margin-bottom: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.dna-card {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.85) 0%, rgba(30, 58, 138, 0.3) 100%);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 12px;
    padding: 1.2rem;
}
.dna-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
.dna-item:last-child { border-bottom: none; }
.dna-label { color: #94a3b8; font-weight: 500; font-size: 0.88rem; }
.dna-value { color: #38bdf8; font-weight: 700; font-size: 0.9rem; }

.att-bar-container { margin-bottom: 0.8rem; }
.att-bar-header { display: flex; justify-content: space-between; margin-bottom: 0.25rem; font-size: 0.85rem; }
.att-bar-bg {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    height: 10px;
    overflow: hidden;
}
.att-bar-fill {
    height: 100%;
    border-radius: 10px;
    background: linear-gradient(90deg, #0284c7 0%, #38bdf8 100%);
}

.badge-high { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); padding: 0.2rem 0.6rem; border-radius: 6px; font-weight: 700; }
.badge-med { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); padding: 0.2rem 0.6rem; border-radius: 6px; font-weight: 700; }
.badge-low { background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.4); padding: 0.2rem 0.6rem; border-radius: 6px; font-weight: 700; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Helper to render clean HTML safely without markdown code block triggers
def render_html(html_str):
    st.markdown(textwrap.dedent(html_str).strip(), unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA LOADERS & PATH RESOLUTION
# -----------------------------------------------------------------------------
DISPLAY_BASINS = [f"Basin_{str(i).zfill(3)}" for i in range(1, 72)]

def locate_data_dir():
    for p in [Path("assets"), Path("HydroFoundation_Large_Final"), Path(".")]:
        if (p / "tables").exists() or (p / "basin_outputs").exists():
            return p
    return Path(".")

BASE_PATH = locate_data_dir()

@st.cache_data
def load_data_tables():
    tables_dir = BASE_PATH / "tables"
    
    def read_csv_safe(file_name, fallback_df):
        p = tables_dir / file_name
        return pd.read_csv(p) if p.exists() else fallback_df

    np.random.seed(42)
    df_env = read_csv_safe("basin_environment_profile.csv", pd.DataFrame({
        "basin_id": DISPLAY_BASINS, "Elevation": np.random.uniform(100, 2500, 71),
        "Clay": np.random.uniform(5, 50, 71), "Bulk Density": np.random.uniform(1.0, 1.8, 71),
        "Hydraulic Conductivity": np.random.uniform(0.1, 15.0, 71), "Agriculture": np.random.uniform(0, 85, 71)
    }))

    df_vuln = read_csv_safe("basin_vulnerability_scores.csv", pd.DataFrame({
        "basin_id": DISPLAY_BASINS, "vulnerability_score": np.random.uniform(10, 95, 71)
    }))

    feats = [f"feat_{i}" for i in range(16)]
    df_emb_fallback = pd.DataFrame(np.random.randn(71, 16), columns=feats)
    df_emb_fallback.insert(0, "basin_id", DISPLAY_BASINS)
    df_emb = read_csv_safe("basin_embeddings.csv", df_emb_fallback)

    sim_recs = []
    for b in DISPLAY_BASINS:
        others = [x for x in DISPLAY_BASINS if x != b]
        for c, s in zip(np.random.choice(others, 3, replace=False), sorted(np.random.uniform(0.7, 0.98, 3), reverse=True)):
            sim_recs.append({"target_basin": b, "similar_basin": c, "similarity_score": round(s, 3)})
    df_sim = read_csv_safe("similar_basins.csv", pd.DataFrame(sim_recs))

    att_recs = []
    features = ["Agriculture", "Clay", "Hydraulic Conductivity", "Elevation", "Bulk Density"]
    for b in DISPLAY_BASINS:
        weights = np.random.dirichlet(np.ones(len(features))) * 100
        for f, w in zip(features, weights):
            att_recs.append({"basin_id": b, "feature": f, "attention_pct": round(w, 1)})
    df_att = read_csv_safe("attention_features.csv", pd.DataFrame(att_recs))

    return df_env, df_vuln, df_emb, df_sim, df_att

df_env, df_vuln, df_emb, df_sim, df_att = load_data_tables()

@st.cache_data(show_spinner=False)
def load_basin_image_b64(basin_id_str, image_filename):
    clean_id = basin_id_str.lower()
    for p in [BASE_PATH / "basin_outputs" / clean_id / image_filename,
              BASE_PATH / "basin_outputs" / basin_id_str / image_filename,
              BASE_PATH / clean_id / image_filename]:
        if p.exists():
            with open(p, "rb") as img_f:
                return f"data:image/png;base64,{base64.b64encode(img_f.read()).decode('utf-8')}"
                
    name_clean = image_filename.replace(".png", "").replace("_", " ").title()
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="260" viewBox="0 0 400 260">
      <rect width="100%" height="100%" fill="#0f172a" rx="8"/>
      <circle cx="200" cy="110" r="40" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4 4"/>
      <text x="50%" y="75%" dominant-baseline="middle" text-anchor="middle" fill="#94a3b8" font-family="sans-serif" font-size="14" font-weight="600">{basin_id_str}: {name_clean}</text>
    </svg>"""
    return f"data:image/svg+xml;base64,{base64.b64encode(svg.encode('utf-8')).decode('utf-8')}"

def render_image_card(title, b64_str, max_width_px=400):
    render_html(f"""
    <div class="img-card" style="max-width: {max_width_px}px;">
        <div class="img-title">{title}</div>
        <img src="{b64_str}" alt="{title}"/>
    </div>
    """)

# -----------------------------------------------------------------------------
# 3. HEADER & BASIN SELECTOR
# -----------------------------------------------------------------------------
st.markdown("<h1 style='text-align: center; color: #f8fafc; font-weight: 800; font-size: 2.2rem; margin-bottom: 0.2rem;'>🌊 HydroFoundation Basin Explorer</h1>", unsafe_allow_html=True)

selected_display_id = st.selectbox("Select Basin", options=DISPLAY_BASINS, index=0)

# -----------------------------------------------------------------------------
# SECTION 1: 🏔 BASIN DIGITAL TWIN
# -----------------------------------------------------------------------------
render_html("<div class='section-header'>🏔 Basin Digital Twin</div>")

img_input = load_basin_image_b64(selected_display_id, "input.png")
img_vuln = load_basin_image_b64(selected_display_id, "vulnerability_map.png")
img_att = load_basin_image_b64(selected_display_id, "attention_map.png")
img_dt = load_basin_image_b64(selected_display_id, "digital_twin.png")

c1, c2, c3 = st.columns([1, 2, 1])
with c2: render_image_card("Input Environment", img_input, max_width_px=420)

st.write("")
r2_c1, r2_c2 = st.columns(2)
with r2_c1: render_image_card("AI Vulnerability Map", img_vuln, max_width_px=400)
with r2_c2: render_image_card("AI Attention Map", img_att, max_width_px=400)

st.write("")
dt_1, dt_2, dt_3 = st.columns([1, 2.4, 1])
with dt_2: render_image_card("Environmental Digital Twin", img_dt, max_width_px=520)

# -----------------------------------------------------------------------------
# SECTION 2: 🧬 ENVIRONMENTAL DNA
# -----------------------------------------------------------------------------
render_html("<div class='section-header'>🧬 Environmental DNA</div>")

dna_col1, dna_col2 = st.columns([1.3, 1])

env_b_col = next((c for c in df_env.columns if c.lower() in ["basin_id", "basin"]), df_env.columns[0])
basin_env_data = df_env[df_env[env_b_col].astype(str).str.capitalize() == selected_display_id]
if basin_env_data.empty: basin_env_data = df_env.iloc[0:1]

variables = ["Elevation", "Clay", "Bulk Density", "Hydraulic Conductivity", "Agriculture"]
radar_vals, raw_vals = [], {}

for var in variables:
    if var in df_env.columns:
        v_min, v_max = df_env[var].min(), df_env[var].max()
        val = float(basin_env_data[var].values[0])
        raw_vals[var] = val
        norm = ((val - v_min) / (v_max - v_min + 1e-6)) * 100
        radar_vals.append(norm)
    else:
        radar_vals.append(50)
        raw_vals[var] = 0.0

with dna_col1:
    fig_radar = go.Figure(go.Scatterpolar(
        r=radar_vals + [radar_vals[0]], theta=variables + [variables[0]],
        fill='toself', fillcolor='rgba(56, 189, 248, 0.25)',
        line=dict(color='#38bdf8', width=2), marker=dict(size=6, color='#0284c7')
    ))
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=False, range=[0, 100]),
            angularaxis=dict(tickfont=dict(size=11, color='#94a3b8'), rotation=90, direction="clockwise"),
            bgcolor='rgba(15, 23, 42, 0.4)'
        ),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=25, b=25), height=260, showlegend=False
    )
    st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})
    st.markdown("<div style='text-align: center; color: #64748b; font-size: 0.8rem;'>Unique watershed environmental signature</div>", unsafe_allow_html=True)

with dna_col2:
    elev, agri, clay, cond = raw_vals.get("Elevation", 0), raw_vals.get("Agriculture", 0), raw_vals.get("Clay", 0), raw_vals.get("Hydraulic Conductivity", 0)
    sens_score = min(99, max(15, int((agri * 0.4) + (clay * 0.6) + 20)))
    
    render_html(f"""
    <div class="dna-card">
        <div style="font-size: 1.05rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.6rem; border-bottom: 1px solid rgba(56,189,248,0.2); padding-bottom: 0.3rem;">
            {selected_display_id} DNA
        </div>
        <div class="dna-item"><span class="dna-label">🌄 Terrain</span><span class="dna-value">{'High' if elev > 1200 else 'Moderate' if elev > 500 else 'Low'} ({elev:.0f}m)</span></div>
        <div class="dna-item"><span class="dna-label">🌱 Land Use</span><span class="dna-value">{'High' if agri > 50 else 'Moderate' if agri > 20 else 'Low'} Agriculture</span></div>
        <div class="dna-item"><span class="dna-label">🟫 Soil</span><span class="dna-value">{'Clay dominated' if clay > 25 else 'Loam / Sand'}</span></div>
        <div class="dna-item"><span class="dna-label">💧 Water Movement</span><span class="dna-value">{'High' if cond > 8 else 'Low'} permeability</span></div>
        <div class="dna-item"><span class="dna-label">🔥 AI Risk</span><span class="dna-value" style="color: #f87171;">{sens_score}% Sensitivity</span></div>
    </div>
    """)

# -----------------------------------------------------------------------------
# SECTION 3: 🧠 AI ATTENTION FINGERPRINT
# -----------------------------------------------------------------------------
render_html("<div class='section-header'>🧠 AI Understanding</div>")
st.markdown("<div style='font-size: 0.95rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.8rem;'>What does AI consider important?</div>", unsafe_allow_html=True)

att_b_col = next((c for c in df_att.columns if c.lower() in ["basin_id", "basin", "target_basin"]), df_att.columns[0])
att_data = df_att[df_att[att_b_col].astype(str).str.capitalize() == selected_display_id].copy()

if not att_data.empty:
    cols = [c for c in att_data.columns if c != att_b_col]
    feature_col = next((c for c in cols if c.lower() in ["feature", "variable", "attribute", "name"]), cols[0])
    val_col_name = next((c for c in cols if c != feature_col), cols[-1])
    
    att_data["raw_val"] = pd.to_numeric(att_data[val_col_name], errors="coerce").fillna(0.0)
    att_data["abs_val"] = att_data["raw_val"].abs()
    att_data = att_data.sort_values("abs_val", ascending=False)
else:
    feature_col = "feature"
    att_data = pd.DataFrame({
        "feature": ["Agriculture", "Clay", "Hydraulic Conductivity", "Elevation", "Bulk Density"],
        "raw_val": [42.0, 25.0, 18.0, 10.0, 5.0], "abs_val": [42.0, 25.0, 18.0, 10.0, 5.0]
    })

max_val = max(att_data["abs_val"].max(), 1e-6)
bars_inner = ""

for _, row in att_data.iterrows():
    feat_name = str(row[feature_col])
    val = float(row["raw_val"])
    abs_v = float(row["abs_val"])
    
    width_pct = (abs_v / max_val) * 100 if max_val > 1.0 else abs_v * 100
    width_pct = max(0.0, min(100.0, width_pct))
    display_pct = val * 100 if abs(val) <= 1.0 else val

    bars_inner += f"""
    <div class="att-bar-container">
        <div class="att-bar-header">
            <span style="color: #e2e8f0; font-weight: 500;">{feat_name}</span>
            <span style="color: #38bdf8; font-weight: 700;">{display_pct:.1f}%</span>
        </div>
        <div class="att-bar-bg">
            <div class="att-bar-fill" style="width: {width_pct:.1f}%;"></div>
        </div>
    </div>"""

render_html(f'<div class="glass-card" style="padding: 1.2rem 1.5rem;">{bars_inner}</div>')

# -----------------------------------------------------------------------------
# SECTION 4: 🌐 BASIN INTELLIGENCE GALAXY
# -----------------------------------------------------------------------------
render_html("<div class='section-header'>🌐 Basin Intelligence Galaxy</div>")

galaxy_c1, galaxy_c2 = st.columns([2, 1])

emb_b_col = next((c for c in df_emb.columns if c.lower() in ["basin_id", "basin", "target_basin", "id"]), df_emb.columns[0])
num_cols = df_emb.select_dtypes(include=[np.number]).columns

if len(num_cols) >= 2:
    coords = df_emb[["dim1", "dim2"]].values if "dim1" in df_emb.columns else PCA(n_components=2).fit_transform(df_emb[num_cols].fillna(0))
else:
    coords = np.random.randn(len(df_emb), 2)

df_galaxy = pd.DataFrame({
    "basin_id": df_emb[emb_b_col].astype(str).str.capitalize(),
    "x": coords[:, 0], "y": coords[:, 1]
})

target_col = next((c for c in df_sim.columns if c.lower() in ["target_basin", "basin_id", "basin"]), df_sim.columns[0])
similar_col = next((c for c in df_sim.columns if c.lower() in ["similar_basin", "twin_basin", "neighbor"]), df_sim.columns[1] if len(df_sim.columns)>1 else df_sim.columns[0])
score_col = next((c for c in df_sim.columns if c.lower() in ["similarity_score", "similarity", "score"]), df_sim.columns[-1])

sim_matches = df_sim[df_sim[target_col].astype(str).str.capitalize() == selected_display_id]
similar_ids = sim_matches[similar_col].astype(str).str.capitalize().tolist()[:3] if not sim_matches.empty else []

df_galaxy["Type"] = df_galaxy["basin_id"].apply(lambda b: "Selected Basin" if b == selected_display_id else ("Environmental Twin" if b in similar_ids else "Other Watersheds"))

with galaxy_c1:
    fig_galaxy = px.scatter(
        df_galaxy, x="x", y="y", hover_name="basin_id", color="Type",
        color_discrete_map={"Selected Basin": "#ef4444", "Environmental Twin": "#38bdf8", "Other Watersheds": "#334155"},
        size=df_galaxy["Type"].map({"Selected Basin": 16, "Environmental Twin": 11, "Other Watersheds": 6})
    )
    fig_galaxy.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15, 23, 42, 0.6)',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=""),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=""),
        margin=dict(l=10, r=10, t=10, b=10), height=280,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#94a3b8"))
    )
    st.plotly_chart(fig_galaxy, use_container_width=True, config={'displayModeBar': False})

with galaxy_c2:
    st.markdown("<div style='font-size: 0.95rem; font-weight: 600; color: #f8fafc; margin-bottom: 0.6rem;'>Closest Environmental Twins</div>", unsafe_allow_html=True)
    
    twins_inner = ""
    if not sim_matches.empty:
        for _, r in sim_matches.head(3).iterrows():
            s_id = str(r[similar_col]).capitalize()
            try:
                s_val = float(r[score_col])
                pct_val = int(s_val * 100) if abs(s_val) <= 1.0 else int(s_val)
            except (ValueError, TypeError):
                pct_val = 85
            twins_inner += f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.05);">
                <span style="font-weight: 600; color: #e2e8f0;">{s_id}</span>
                <span style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); padding: 0.2rem 0.5rem; border-radius: 6px; font-weight: 700; font-size: 0.85rem;">{pct_val}%</span>
            </div>"""
    else:
        twins_inner = "<div style='color: #64748b;'>No similarity data available</div>"
        
    render_html(f'<div class="glass-card" style="padding: 0.8rem 1rem;">{twins_inner}</div>')

# -----------------------------------------------------------------------------
# SECTION 5: 🔥 WATERSHED RISK ASSESSMENT
# -----------------------------------------------------------------------------
render_html("<div class='section-header'>🔥 Watershed Risk</div>")

vuln_b_col = next((c for c in df_vuln.columns if c.lower() in ["basin_id", "basin", "target_basin"]), df_vuln.columns[0])
vuln_s_col = next((c for c in df_vuln.columns if c != vuln_b_col), df_vuln.columns[-1])

df_vuln_sorted = df_vuln.copy()
df_vuln_sorted["clean_id"] = df_vuln_sorted[vuln_b_col].astype(str).str.capitalize()
df_vuln_sorted[vuln_s_col] = pd.to_numeric(df_vuln_sorted[vuln_s_col], errors="coerce").fillna(0)
df_vuln_sorted = df_vuln_sorted.sort_values(vuln_s_col, ascending=False).reset_index(drop=True)
df_vuln_sorted["rank"] = df_vuln_sorted.index + 1

target_row = df_vuln_sorted[df_vuln_sorted["clean_id"] == selected_display_id]
v_score = float(target_row[vuln_s_col].values[0]) if not target_row.empty else 50.0
v_rank = int(target_row["rank"].values[0]) if not target_row.empty else 35
total_basins = len(df_vuln_sorted)

if v_score >= 70: badge_html = '<span class="badge-high">High Risk 🔴</span>'
elif v_score >= 35: badge_html = '<span class="badge-med">Medium Risk 🟡</span>'
else: badge_html = '<span class="badge-low">Low Risk 🟢</span>'

render_html(f"""
<div class="glass-card" style="display: flex; justify-content: space-around; align-items: center; padding: 1.2rem; text-align: center;">
    <div>
        <div style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; font-weight: 600;">Status</div>
        <div style="margin-top: 0.4rem;">{badge_html}</div>
    </div>
    <div style="border-left: 1px solid rgba(255,255,255,0.1); border-right: 1px solid rgba(255,255,255,0.1); padding: 0 2rem;">
        <div style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; font-weight: 600;">Vulnerability Score</div>
        <div style="font-size: 1.8rem; font-weight: 800; color: #38bdf8; margin-top: 0.2rem;">{v_score:.1f}<span style="font-size: 1rem; color: #64748b;"> / 100</span></div>
    </div>
    <div>
        <div style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; font-weight: 600;">Risk Ranking</div>
        <div style="font-size: 1.8rem; font-weight: 800; color: #f8fafc; margin-top: 0.2rem;">#{v_rank} <span style="font-size: 0.9rem; font-weight: 500; color: #64748b;">of {total_basins}</span></div>
    </div>
</div>
""")
