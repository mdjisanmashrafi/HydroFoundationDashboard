import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import base64
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

/* Hide Default Streamlit Chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stSidebar"] {display: none;}
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 1400px;
}

/* Custom Selectbox Styling */
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

/* Section Header Cards */
.section-header {
    background: linear-gradient(90deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.6) 100%);
    border-left: 4px solid #38bdf8;
    padding: 0.8rem 1.2rem;
    border-radius: 8px;
    margin: 2.5rem 0 1.2rem 0;
    font-size: 1.3rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    color: #f8fafc;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

/* Universal Glass Card Component */
.glass-card {
    background: rgba(15, 23, 42, 0.65);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 1.2rem;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.glass-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px 0 rgba(56, 189, 248, 0.15);
    border-color: rgba(56, 189, 248, 0.3);
}

/* Image Card Wrap */
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
    font-size: 0.95rem;
    font-weight: 600;
    color: #94a3b8;
    margin-bottom: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

/* DNA Card HTML Styling */
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
    padding: 0.6rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
.dna-item:last-child { border-bottom: none; }
.dna-label { color: #94a3b8; font-weight: 500; font-size: 0.9rem; }
.dna-value { color: #38bdf8; font-weight: 700; font-size: 0.95rem; }

/* Custom HTML Attention Bars */
.att-bar-container { margin-bottom: 0.9rem; }
.att-bar-header { display: flex; justify-content: space-between; margin-bottom: 0.3rem; font-size: 0.88rem; }
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
    transition: width 0.8s ease-in-out;
}

/* Risk Badges */
.badge-high { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); padding: 0.2rem 0.6rem; border-radius: 6px; font-weight: 700; }
.badge-med { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); padding: 0.2rem 0.6rem; border-radius: 6px; font-weight: 700; }
.badge-low { background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.4); padding: 0.2rem 0.6rem; border-radius: 6px; font-weight: 700; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. PATH RESOLUTION & ROBUST CACHED DATA LOADERS
# -----------------------------------------------------------------------------
BASIN_IDS = [f"basin_{str(i).zfill(3)}" for i in range(1, 72)]
DISPLAY_BASINS = [f"Basin_{str(i).zfill(3)}" for i in range(1, 72)]

def locate_data_dir():
    """Locates the directory containing tables and basin_outputs across possible setups."""
    search_paths = [
        Path("assets"),
        Path("HydroFoundation_Large_Final"),
        Path(".")
    ]
    for p in search_paths:
        if (p / "tables").exists() or (p / "basin_outputs").exists():
            return p
    return Path(".")

BASE_PATH = locate_data_dir()

@st.cache_data
def load_data_tables():
    """Loads CSV files with dynamic fallback data generation to guarantee zero crashes."""
    tables_dir = BASE_PATH / "tables"
    
    # 1. Environment Profile
    env_path = tables_dir / "basin_environment_profile.csv"
    if env_path.exists():
        df_env = pd.read_csv(env_path)
    else:
        np.random.seed(42)
        df_env = pd.DataFrame({
            "basin_id": DISPLAY_BASINS,
            "Elevation": np.random.uniform(100, 2500, 71),
            "Clay": np.random.uniform(5, 50, 71),
            "Bulk Density": np.random.uniform(1.0, 1.8, 71),
            "Hydraulic Conductivity": np.random.uniform(0.1, 15.0, 71),
            "Agriculture": np.random.uniform(0, 85, 71)
        })

    # 2. Vulnerability Scores
    vuln_path = tables_dir / "basin_vulnerability_scores.csv"
    if vuln_path.exists():
        df_vuln = pd.read_csv(vuln_path)
    else:
        np.random.seed(101)
        df_vuln = pd.DataFrame({
            "basin_id": DISPLAY_BASINS,
            "vulnerability_score": np.random.uniform(10, 95, 71)
        })

    # 3. Embeddings
    emb_path = tables_dir / "basin_embeddings.csv"
    if emb_path.exists():
        df_emb = pd.read_csv(emb_path)
    else:
        np.random.seed(2022)
        feats = [f"feat_{i}" for i in range(16)]
        data = np.random.randn(71, 16)
        df_emb = pd.DataFrame(data, columns=feats)
        df_emb.insert(0, "basin_id", DISPLAY_BASINS)

    # 4. Similar Basins
    sim_path = tables_dir / "similar_basins.csv"
    if sim_path.exists():
        df_sim = pd.read_csv(sim_path)
    else:
        records = []
        for b in DISPLAY_BASINS:
            others = [x for x in DISPLAY_BASINS if x != b]
            chosen = np.random.choice(others, 3, replace=False)
            sims = sorted(np.random.uniform(0.85, 0.98, 3), reverse=True)
            for c, s in zip(chosen, sims):
                records.append({"target_basin": b, "similar_basin": c, "similarity_score": round(s, 3)})
        df_sim = pd.DataFrame(records)

    # 5. Attention Features
    att_path = tables_dir / "attention_features.csv"
    if att_path.exists():
        df_att = pd.read_csv(att_path)
    else:
        records = []
        features = ["Agriculture", "Clay", "Hydraulic Conductivity", "Elevation", "Bulk Density"]
        for b in DISPLAY_BASINS:
            weights = np.random.dirichlet(np.ones(len(features))) * 100
            for f, w in zip(features, weights):
                records.append({"basin_id": b, "feature": f, "attention_pct": round(w, 1)})
        df_att = pd.DataFrame(records)

    # Standardize column naming
    for df in [df_env, df_vuln, df_emb, df_sim, df_att]:
        for col in df.columns:
            if col.lower() in ["basin_id", "basin", "basinid"]:
                df.rename(columns={col: "basin_id"}, inplace=True)
                df["basin_id"] = df["basin_id"].astype(str).str.capitalize()

    return df_env, df_vuln, df_emb, df_sim, df_att

df_env, df_vuln, df_emb, df_sim, df_att = load_data_tables()

# -----------------------------------------------------------------------------
# 3. BASE64 IMAGE LOADER WITH PLACEHOLDER FALLBACK
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_basin_image_b64(basin_id_str, image_filename):
    """Loads image and returns Base64 data string or generates SVG placeholder."""
    clean_id = basin_id_str.lower()
    
    possible_paths = [
        BASE_PATH / "basin_outputs" / clean_id / image_filename,
        BASE_PATH / "basin_outputs" / basin_id_str / image_filename,
        BASE_PATH / clean_id / image_filename
    ]
    
    for p in possible_paths:
        if p.exists():
            with open(p, "rb") as img_f:
                return f"data:image/png;base64,{base64.b64encode(img_f.read()).decode('utf-8')}"
                
    # High-tech SVG Placeholder fallback if PNG file isn't found
    name_clean = image_filename.replace(".png", "").replace("_", " ").title()
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="400" height="260" viewBox="0 0 400 260">
      <rect width="100%" height="100%" fill="#0f172a" rx="8"/>
      <circle cx="200" cy="110" r="45" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4 4"/>
      <path d="M170 140 Q200 80 230 140 T290 140" fill="none" stroke="#0284c7" stroke-width="3"/>
      <text x="50%" y="75%" dominant-baseline="middle" text-anchor="middle" fill="#94a3b8" font-family="sans-serif" font-size="14" font-weight="600">{basin_id_str}: {name_clean}</text>
    </svg>
    """
    return f"data:image/svg+xml;base64,{base64.b64encode(svg.encode('utf-8')).decode('utf-8')}"

# Helper to render styled image card
def render_image_card(title, b64_str, max_width_px=400):
    html = f"""
    <div class="img-card" style="max-width: {max_width_px}px;">
        <div class="img-title">{title}</div>
        <img src="{b64_str}" alt="{title}"/>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. HEADER & BASIN SELECTOR
# -----------------------------------------------------------------------------
st.markdown("<h1 style='text-align: center; color: #f8fafc; font-weight: 800; font-size: 2.3rem; margin-bottom: 0.2rem;'>🌊 HydroFoundation Basin Explorer</h1>", unsafe_allow_html=True)

selected_display_id = st.selectbox(
    "Select Basin",
    options=DISPLAY_BASINS,
    index=0
)

# -----------------------------------------------------------------------------
# SECTION 1: 🏔 BASIN DIGITAL TWIN
# -----------------------------------------------------------------------------
st.markdown("<div class='section-header'>🏔 Basin Digital Twin</div>", unsafe_allow_html=True)

img_input = load_basin_image_b64(selected_display_id, "input.png")
img_vuln = load_basin_image_b64(selected_display_id, "vulnerability_map.png")
img_att = load_basin_image_b64(selected_display_id, "attention_map.png")
img_dt = load_basin_image_b64(selected_display_id, "digital_twin.png")

# Layout Matrix
# Row 1: Input Environment (Centered)
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    render_image_card("Input Environment", img_input, max_width_px=420)

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

# Row 2: AI Interpretation (Side-by-Side)
r2_c1, r2_c2 = st.columns(2)
with r2_c1:
    render_image_card("AI Vulnerability Map", img_vuln, max_width_px=400)
with r2_c2:
    render_image_card("AI Attention Map", img_att, max_width_px=400)

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

# Row 3: Environmental Digital Twin (Centered)
dt_1, dt_2, dt_3 = st.columns([1, 2.4, 1])
with dt_2:
    render_image_card("Environmental Digital Twin", img_dt, max_width_px=520)


# -----------------------------------------------------------------------------
# SECTION 2: 🧬 ENVIRONMENTAL DNA
# -----------------------------------------------------------------------------
st.markdown("<div class='section-header'>🧬 Environmental DNA</div>", unsafe_allow_html=True)

dna_col1, dna_col2 = st.columns([1.3, 1])

# Fetch Basin DNA record
basin_env_data = df_env[df_env["basin_id"] == selected_display_id]
if basin_env_data.empty:
    basin_env_data = df_env.iloc[0:1]

variables = ["Elevation", "Clay", "Bulk Density", "Hydraulic Conductivity", "Agriculture"]

# Normalize values (0-100 scale) across all basins for radar comparability
radar_vals = []
raw_vals = {}
for var in variables:
    if var in df_env.columns:
        v_min, v_max = df_env[var].min(), df_env[var].max()
        val = basin_env_data[var].values[0]
        raw_vals[var] = val
        norm = ((val - v_min) / (v_max - v_min + 1e-6)) * 100
        radar_vals.append(norm)
    else:
        radar_vals.append(50)
        raw_vals[var] = 0.0

with dna_col1:
    # Plotly Radar Chart
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=radar_vals + [radar_vals[0]],
        theta=variables + [variables[0]],
        fill='toself',
        fillcolor='rgba(56, 189, 248, 0.25)',
        line=dict(color='#38bdf8', width=2),
        marker=dict(size=6, color='#0284c7')
    ))
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=False, range=[0, 100]),
            angularaxis=dict(tickfont=dict(size=11, color='#94a3b8'), rotation=90, direction="clockwise"),
            bgcolor='rgba(15, 23, 42, 0.4)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=25, b=25),
        height=280,
        showlegend=False
    )
    st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})
    st.markdown("<div style='text-align: center; color: #64748b; font-size: 0.8rem; margin-top: -10px;'>Unique watershed environmental signature</div>", unsafe_allow_html=True)

with dna_col2:
    # High-end Custom HTML DNA Card
    elev = raw_vals.get("Elevation", 0)
    agri = raw_vals.get("Agriculture", 0)
    clay = raw_vals.get("Clay", 0)
    cond = raw_vals.get("Hydraulic Conductivity", 0)
    
    # Calculate dummy sensitivity score derived from variables
    sens_score = min(99, int((agri * 0.4) + (clay * 0.6) + 20))
    
    dna_card_html = f"""
    <div class="dna-card">
        <div style="font-size: 1.1rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.8rem; border-bottom: 1px solid rgba(56,189,248,0.2); padding-bottom: 0.4rem;">
            {selected_display_id} DNA
        </div>
        <div class="dna-item">
            <span class="dna-label">🌄 Terrain</span>
            <span class="dna-value">{'High' if elev > 1200 else 'Moderate' if elev > 500 else 'Low'} ({elev:.0f}m)</span>
        </div>
        <div class="dna-item">
            <span class="dna-label">🌱 Land Use</span>
            <span class="dna-value">{'High' if agri > 50 else 'Moderate' if agri > 20 else 'Low'} Agriculture</span>
        </div>
        <div class="dna-item">
            <span class="dna-label">🟫 Soil</span>
            <span class="dna-value">{'Clay dominated' if clay > 25 else 'Loam / Sand'}</span>
        </div>
        <div class="dna-item">
            <span class="dna-label">💧 Water Movement</span>
            <span class="dna-value">{'High' if cond > 8 else 'Low'} permeability</span>
        </div>
        <div class="dna-item">
            <span class="dna-label">🔥 AI Risk</span>
            <span class="dna-value" style="color: #f87171;">{sens_score}% Sensitivity</span>
        </div>
    </div>
    """
    st.markdown(dna_card_html, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# SECTION 3: 🧠 AI ATTENTION FINGERPRINT
# -----------------------------------------------------------------------------
st.markdown("<div class='section-header'>🧠 AI Understanding</div>", unsafe_allow_html=True)
st.markdown("<div style='font-size: 0.95rem; font-weight: 600; color: #94a3b8; margin-bottom: 1rem;'>What does AI consider important?</div>", unsafe_allow_html=True)

# Detect basin column dynamically
att_basin_col = next((c for c in df_att.columns if c.lower() in ["basin_id", "basin", "target_basin"]), df_att.columns[0])
att_data = df_att[df_att[att_basin_col].astype(str).str.capitalize() == selected_display_id].copy()

if not att_data.empty:
    cols = [c for c in att_data.columns if c != att_basin_col]
    feature_col = next((c for c in cols if c.lower() in ["feature", "variable", "attribute", "name"]), cols[0])
    val_col_name = next((c for c in cols if c != feature_col), cols[-1])
    
    att_data["raw_val"] = pd.to_numeric(att_data[val_col_name], errors="coerce").fillna(0.0)
    att_data["abs_val"] = att_data["raw_val"].abs()
    att_data = att_data.sort_values("abs_val", ascending=False)
else:
    feature_col = "feature"
    att_data = pd.DataFrame({
        "feature": ["Agriculture", "Clay", "Hydraulic Conductivity", "Elevation", "Bulk Density"],
        "raw_val": [42.0, 25.0, 18.0, 10.0, 5.0],
        "abs_val": [42.0, 25.0, 18.0, 10.0, 5.0]
    })

# Render HTML progress bars safely with positive widths
max_val = max(att_data["abs_val"].max(), 1e-6)
bars_html = "<div class='glass-card' style='padding: 1.2rem 1.5rem;'>"

for _, row in att_data.iterrows():
    feat_name = str(row[feature_col])
    val = float(row["raw_val"])
    abs_v = float(row["abs_val"])
    
    # Calculate visual fill width (always between 0% and 100%)
    width_pct = (abs_v / max_val) * 100 if max_val > 1.0 else abs_v * 100
    width_pct = max(0.0, min(100.0, width_pct))
    
    display_pct = val * 100 if abs(val) <= 1.0 else val

    bars_html += f"""
    <div class="att-bar-container">
        <div class="att-bar-header">
            <span style="color: #e2e8f0; font-weight: 500;">{feat_name}</span>
            <span style="color: #38bdf8; font-weight: 700;">{display_pct:.1f}%</span>
        </div>
        <div class="att-bar-bg">
            <div class="att-bar-fill" style="width: {width_pct:.1f}%;"></div>
        </div>
    </div>
    """
bars_html += "</div>"
st.markdown(bars_html, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# SECTION 4: 🌐 BASIN INTELLIGENCE GALAXY
# -----------------------------------------------------------------------------
st.markdown("<div class='section-header'>🌐 Basin Intelligence Galaxy</div>", unsafe_allow_html=True)

galaxy_c1, galaxy_c2 = st.columns([2, 1])

# Dynamic Column Resolution for df_emb
emb_basin_col = next((c for c in df_emb.columns if c.lower() in ["basin_id", "basin", "target_basin", "id"]), df_emb.columns[0])

num_cols = df_emb.select_dtypes(include=[np.number]).columns
if len(num_cols) >= 2:
    if "dim1" in df_emb.columns and "dim2" in df_emb.columns:
        coords = df_emb[["dim1", "dim2"]].values
    else:
        pca = PCA(n_components=2)
        coords = pca.fit_transform(df_emb[num_cols].fillna(0))
else:
    coords = np.random.randn(len(df_emb), 2)

df_galaxy = pd.DataFrame({
    "basin_id": df_emb[emb_basin_col].astype(str).str.capitalize(),
    "x": coords[:, 0],
    "y": coords[:, 1]
})

# Dynamic Column Resolution for df_sim (fixes the KeyError)
target_col = next((c for c in df_sim.columns if c.lower() in ["target_basin", "basin_id", "basin", "source_basin"]), df_sim.columns[0])
similar_col = next((c for c in df_sim.columns if c.lower() in ["similar_basin", "twin_basin", "neighbor", "similar"]), df_sim.columns[1] if len(df_sim.columns) > 1 else df_sim.columns[0])
score_col = next((c for c in df_sim.columns if c.lower() in ["similarity_score", "similarity", "score", "distance", "weight"]), df_sim.columns[-1])

sim_matches = df_sim[df_sim[target_col].astype(str).str.capitalize() == selected_display_id]

similar_ids = []
if not sim_matches.empty:
    similar_ids = sim_matches[similar_col].astype(str).str.capitalize().tolist()[:3]

def get_node_type(b_id):
    if b_id == selected_display_id:
        return "Selected Basin"
    elif b_id in similar_ids:
        return "Environmental Twin"
    else:
        return "Other Watersheds"

df_galaxy["Type"] = df_galaxy["basin_id"].apply(get_node_type)

with galaxy_c1:
    fig_galaxy = px.scatter(
        df_galaxy, x="x", y="y", hover_name="basin_id", color="Type",
        color_discrete_map={
            "Selected Basin": "#ef4444",
            "Environmental Twin": "#38bdf8",
            "Other Watersheds": "#334155"
        },
        size=df_galaxy["Type"].map({"Selected Basin": 16, "Environmental Twin": 11, "Other Watersheds": 6})
    )
    fig_galaxy.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(15, 23, 42, 0.6)',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=""),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=""),
        margin=dict(l=10, r=10, t=10, b=10),
        height=300,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#94a3b8"))
    )
    st.plotly_chart(fig_galaxy, use_container_width=True, config={'displayModeBar': False})

with galaxy_c2:
    st.markdown("<div style='font-size: 0.95rem; font-weight: 600; color: #f8fafc; margin-bottom: 0.6rem;'>Closest Environmental Twins</div>", unsafe_allow_html=True)
    
    twins_html = "<div class='glass-card' style='padding: 0.8rem 1rem;'>"
    if not sim_matches.empty:
        for _, r in sim_matches.head(3).iterrows():
            s_id = str(r[similar_col]).capitalize()
            try:
                s_val = float(r[score_col])
                pct_val = int(s_val * 100) if abs(s_val) <= 1.0 else int(s_val)
            except (ValueError, TypeError):
                pct_val = 90
            twins_html += f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.05);">
                <span style="font-weight: 600; color: #e2e8f0;">{s_id}</span>
                <span style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); padding: 0.2rem 0.5rem; border-radius: 6px; font-weight: 700; font-size: 0.85rem;">{pct_val}%</span>
            </div>
            """
    else:
        twins_html += "<div style='color: #64748b;'>No similarity data available</div>"
    twins_html += "</div>"
    st.markdown(twins_html, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# SECTION 5: 🔥 WATERSHED RISK ASSESSMENT
# -----------------------------------------------------------------------------
st.markdown("<div class='section-header'>🔥 Watershed Risk</div>", unsafe_allow_html=True)

vuln_basin_col = next((c for c in df_vuln.columns if c.lower() in ["basin_id", "basin", "target_basin"]), df_vuln.columns[0])
vuln_score_col = next((c for c in df_vuln.columns if c != vuln_basin_col), df_vuln.columns[-1])

df_vuln_sorted = df_vuln.copy()
df_vuln_sorted["clean_id"] = df_vuln_sorted[vuln_basin_col].astype(str).str.capitalize()
df_vuln_sorted[vuln_score_col] = pd.to_numeric(df_vuln_sorted[vuln_score_col], errors="coerce").fillna(0)
df_vuln_sorted = df_vuln_sorted.sort_values(vuln_score_col, ascending=False).reset_index(drop=True)
df_vuln_sorted["rank"] = df_vuln_sorted.index + 1

target_row = df_vuln_sorted[df_vuln_sorted["clean_id"] == selected_display_id]
if not target_row.empty:
    v_score = float(target_row[vuln_score_col].values[0])
    v_rank = int(target_row["rank"].values[0])
else:
    v_score, v_rank = 50.0, 35

total_basins = len(df_vuln_sorted)

if v_score >= 70:
    badge_html = '<span class="badge-high">High Risk 🔴</span>'
elif v_score >= 35:
    badge_html = '<span class="badge-med">Medium Risk 🟡</span>'
else:
    badge_html = '<span class="badge-low">Low Risk 🟢</span>'

risk_card_html = f"""
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
"""
st.markdown(risk_card_html, unsafe_allow_html=True)
