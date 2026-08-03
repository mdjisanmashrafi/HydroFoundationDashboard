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
    page_title="HydroFoundation AI Explorer",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

PREMIUM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    background-color: #020617; /* Slate 950 */
    color: #e2e8f0;
    font-family: 'Inter', sans-serif;
}

#MainMenu, footer, header, [data-testid="stSidebar"] { display: none !important; }

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
    max-width: 1200px;
}

/* Premium Selectbox Container */
div[data-testid="stSelectbox"] > label {
    display: none;
}
div[data-testid="stSelectbox"] {
    max-width: 300px;
    margin: 0 auto;
}
div[data-testid="stSelectbox"] > div {
    background: rgba(15, 23, 42, 0.8) !important;
    border: 1px solid rgba(14, 165, 233, 0.4) !important;
    border-radius: 12px !important;
    color: #38bdf8 !important;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 1.1rem;
    box-shadow: 0 0 20px rgba(14, 165, 233, 0.15);
    transition: all 0.3s ease;
}
div[data-testid="stSelectbox"] > div:hover {
    box-shadow: 0 0 30px rgba(14, 165, 233, 0.3);
    border-color: rgba(14, 165, 233, 0.8) !important;
}

/* Typography & Dividers */
.app-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 2.5rem;
    text-align: center;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
    letter-spacing: -0.02em;
}

.app-subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 1rem;
    font-weight: 500;
    margin-bottom: 2rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.section-divider {
    height: 1px;
    background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(14,165,233,0.3) 50%, rgba(255,255,255,0) 100%);
    margin: 3rem 0;
}

.section-header {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.4rem;
    font-weight: 600;
    color: #f8fafc;
    text-align: center;
    margin-bottom: 2rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    text-shadow: 0 0 20px rgba(255,255,255,0.2);
}

/* Glassmorphism Cards */
.glass-panel {
    background: rgba(30, 41, 59, 0.4);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.glass-panel:hover {
    border-color: rgba(14, 165, 233, 0.2);
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.6), 0 0 20px rgba(14, 165, 233, 0.1);
}

/* Premium Images */
.premium-img-container {
    margin: 0 auto 2rem auto;
    text-align: center;
}
.premium-img-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.85rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin-bottom: 0.8rem;
    font-weight: 600;
}
.img-wrapper {
    overflow: hidden;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 15px 35px rgba(0,0,0,0.6);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    background: #0f172a;
}
.img-wrapper:hover {
    transform: scale(1.03);
    border-color: rgba(14, 165, 233, 0.5);
    box-shadow: 0 20px 45px rgba(0,0,0,0.8), 0 0 30px rgba(14, 165, 233, 0.2);
}
.img-wrapper img {
    display: block;
    width: 100%;
    height: auto;
    object-fit: cover;
}

/* DNA Compact Card */
.dna-card-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: 100%;
}
.dna-row {
    display: flex;
    justify-content: space-between;
    padding: 0.8rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 0.95rem;
}
.dna-row span:first-child { color: #94a3b8; }
.dna-row span:last-child { color: #f8fafc; font-weight: 600; }
.dna-sensitivity {
    margin-top: 1.5rem;
    padding: 1rem;
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(245, 158, 11, 0.05));
    border: 1px solid rgba(239, 68, 68, 0.2);
    border-radius: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.dna-sensitivity .label { font-family: 'Space Grotesk', sans-serif; color: #f87171; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
.dna-sensitivity .val { font-size: 1.5rem; font-weight: 800; color: #f8fafc; }

/* AI Attention Bars */
@keyframes fillBar { from { width: 0; } }
.ai-att-row { margin-bottom: 1.2rem; }
.ai-att-label { display: flex; justify-content: space-between; margin-bottom: 0.4rem; font-size: 0.9rem; }
.ai-att-label .feat { color: #cbd5e1; font-weight: 500; display: flex; align-items: center; gap: 8px;}
.ai-att-label .pct { color: #38bdf8; font-family: 'Space Grotesk', sans-serif; font-weight: 700; }
.ai-att-track { background: rgba(15, 23, 42, 0.8); border-radius: 8px; height: 8px; overflow: hidden; border: 1px solid rgba(255,255,255,0.05); }
.ai-att-fill { height: 100%; border-radius: 8px; background: linear-gradient(90deg, #0284c7, #38bdf8, #818cf8); box-shadow: 0 0 10px rgba(56, 189, 248, 0.5); animation: fillBar 1.2s cubic-bezier(0.1, 0.7, 0.1, 1) forwards; }

/* Risk Card */
.risk-panel {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2.5rem 2rem;
    border-radius: 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.risk-panel::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(circle at center, rgba(255,255,255,0.05) 0%, transparent 70%);
}
.risk-label { font-family: 'Space Grotesk', sans-serif; color: #94a3b8; font-size: 1rem; text-transform: uppercase; letter-spacing: 0.2em; margin-bottom: 1rem; z-index: 1; }
.risk-score { font-size: 4.5rem; font-weight: 800; line-height: 1; margin-bottom: 0.5rem; font-family: 'Space Grotesk', sans-serif; z-index: 1; text-shadow: 0 0 30px currentColor; }
.risk-text { font-size: 1.2rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 1.5rem; z-index: 1; }
.risk-rank { display: inline-block; padding: 0.4rem 1rem; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; color: #cbd5e1; font-size: 0.9rem; font-weight: 500; z-index: 1; }

.risk-high { background: linear-gradient(135deg, rgba(127, 29, 29, 0.8), rgba(69, 10, 10, 0.9)); border: 1px solid rgba(239, 68, 68, 0.3); }
.risk-high .risk-score, .risk-high .risk-text { color: #f87171; }
.risk-med { background: linear-gradient(135deg, rgba(120, 53, 15, 0.8), rgba(69, 26, 3, 0.9)); border: 1px solid rgba(245, 158, 11, 0.3); }
.risk-med .risk-score, .risk-med .risk-text { color: #fbbf24; }
.risk-low { background: linear-gradient(135deg, rgba(20, 83, 45, 0.8), rgba(5, 46, 22, 0.9)); border: 1px solid rgba(34, 197, 94, 0.3); }
.risk-low .risk-score, .risk-low .risk-text { color: #4ade80; }

</style>
"""
st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

def render_html(html_str):
    st.markdown(textwrap.dedent(html_str).strip(), unsafe_allow_html=True)

def find_col(df, possible_names):
    for c in df.columns:
        c_clean = str(c).lower().strip().replace("_", " ")
        for p in possible_names:
            if p.lower().strip().replace("_", " ") in c_clean:
                return c
    return None

# -----------------------------------------------------------------------------
# 2. DATA LOADERS (Original Logic preserved)
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
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400">
      <rect width="100%" height="100%" fill="#0b1120" rx="12"/>
      <circle cx="300" cy="170" r="60" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="6 6"/>
      <text x="50%" y="70%" dominant-baseline="middle" text-anchor="middle" fill="#64748b" font-family="sans-serif" font-size="18" font-weight="600">{basin_id_str}</text>
      <text x="50%" y="78%" dominant-baseline="middle" text-anchor="middle" fill="#475569" font-family="sans-serif" font-size="14">{name_clean}</text>
    </svg>"""
    return f"data:image/svg+xml;base64,{base64.b64encode(svg.encode('utf-8')).decode('utf-8')}"

def render_premium_image(title, b64_str, max_width_px=500):
    render_html(f"""
    <div class="premium-img-container" style="max-width: {max_width_px}px;">
        <div class="premium-img-title">{title}</div>
        <div class="img-wrapper">
            <img src="{b64_str}" alt="{title}"/>
        </div>
    </div>
    """)

# -----------------------------------------------------------------------------
# 3. HEADER & CONTROL PANEL
# -----------------------------------------------------------------------------
st.markdown("<div class='app-title'>🌊 HydroFoundation AI</div>", unsafe_allow_html=True)
st.markdown("<div class='app-subtitle'>Environmental Intelligence Profile</div>", unsafe_allow_html=True)

selected_display_id = st.selectbox("Selected Watershed", options=DISPLAY_BASINS, index=0, label_visibility="collapsed")

# -----------------------------------------------------------------------------
# SECTION 1: DIGITAL TWIN
# -----------------------------------------------------------------------------
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
st.markdown("<div class='section-header'>Digital Twin</div>", unsafe_allow_html=True)

img_input = load_basin_image_b64(selected_display_id, "input.png")
img_vuln = load_basin_image_b64(selected_display_id, "vulnerability_map.png")
img_att = load_basin_image_b64(selected_display_id, "attention_map.png")
img_dt = load_basin_image_b64(selected_display_id, "digital_twin.png")

# Layout: Input (Top) -> Vision (Att/Vuln side-by-side) -> Twin (Bottom)
render_premium_image("Input Environment", img_input, max_width_px=500)

c1, c2 = st.columns(2)
with c1: render_premium_image("AI Attention", img_att, max_width_px=450)
with c2: render_premium_image("Vulnerability", img_vuln, max_width_px=450)

render_premium_image("Reconstructed Digital Twin", img_dt, max_width_px=600)

# -----------------------------------------------------------------------------
# SECTION 2: ENVIRONMENTAL DNA
# -----------------------------------------------------------------------------
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
st.markdown("<div class='section-header'>Environmental DNA</div>", unsafe_allow_html=True)

dna_c1, dna_c2 = st.columns([1.2, 1])

env_b_col = find_col(df_env, ["basin_id", "basin", "target_basin", "id"]) or df_env.columns[0]
df_env["clean_id"] = df_env[env_b_col].astype(str).str.capitalize()
basin_env_data = df_env[df_env["clean_id"] == selected_display_id]

if basin_env_data.empty:
    num_id = selected_display_id.replace("Basin_", "")
    basin_env_data = df_env[df_env[env_b_col].astype(str).str.contains(num_id)]
if basin_env_data.empty:
    basin_env_data = df_env.iloc[0:1]

c_elev = find_col(df_env, ["elevation", "elev", "height"])
c_clay = find_col(df_env, ["clay", "clay_content", "clay_pct"])
c_bd   = find_col(df_env, ["bulk density", "bulk_density", "bd", "density"])
c_ksat = find_col(df_env, ["hydraulic conductivity", "hydraulic_conductivity", "ksat", "perm"])
c_agri = find_col(df_env, ["agriculture", "agri", "crop", "land_use"])

variable_map = {
    "Elevation": c_elev, "Clay": c_clay, "Bulk Density": c_bd, 
    "Conductivity": c_ksat, "Agriculture": c_agri
}

radar_vals, raw_vals = [], {}
for var_label, col_name in variable_map.items():
    if col_name and col_name in df_env.columns:
        v_min = pd.to_numeric(df_env[col_name], errors='coerce').min()
        v_max = pd.to_numeric(df_env[col_name], errors='coerce').max()
        val = float(pd.to_numeric(basin_env_data[col_name], errors='coerce').values[0])
        raw_vals[var_label] = val
        norm = ((val - v_min) / (v_max - v_min + 1e-6)) * 100
        radar_vals.append(max(5.0, min(100.0, norm)))
    else:
        radar_vals.append(50.0)
        raw_vals[var_label] = 0.0

with dna_c1:
    fig_radar = go.Figure(go.Scatterpolar(
        r=radar_vals + [radar_vals[0]], 
        theta=list(variable_map.keys()) + [list(variable_map.keys())[0]],
        fill='toself', 
        fillcolor='rgba(14, 165, 233, 0.2)',
        line=dict(color='#0ea5e9', width=3), 
        marker=dict(size=8, color='#38bdf8', symbol='circle')
    ))
    fig_radar.update_layout(
        template="plotly_dark",
        polar=dict(
            radialaxis=dict(visible=False, range=[0, 100]),
            angularaxis=dict(tickfont=dict(size=13, color='#cbd5e1', family='Space Grotesk'), rotation=90, gridcolor='rgba(255,255,255,0.1)'),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=25, b=25), height=320, showlegend=False
    )
    st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})

with dna_c2:
    elev = raw_vals.get("Elevation", 0)
    agri = raw_vals.get("Agriculture", 0)
    clay = raw_vals.get("Clay", 0)
    cond = raw_vals.get("Conductivity", 0)
    
    terrain_str = f"High Alpine ({elev:.0f}m)" if elev > 800 else f"Moderate ({elev:.0f}m)" if elev > 250 else f"Lowlands ({elev:.0f}m)"
    agri_str = f"Intensive ({agri:.1f}%)" if agri > 40 or agri > 0.4 else f"Moderate ({agri:.1f}%)" if agri > 15 or agri > 0.15 else f"Minimal ({agri:.1f}%)"
    soil_str = f"Clay Dominant" if clay > 25 or clay > 0.25 else f"Loam / Sand"
    perm_str = f"High Flow" if cond > 5.0 or cond > 0.5 else f"Low Flow"
    
    sens_score = int(radar_vals[1] * 0.5 + radar_vals[4] * 0.5) if len(radar_vals) >= 5 else 50
    sens_score = max(15, min(98, sens_score))

    render_html(f"""
    <div class="glass-panel dna-card-container">
        <div class="premium-img-title" style="margin-bottom: 1.5rem;">{selected_display_id} Identity</div>
        <div class="dna-row"><span>Terrain</span><span>{terrain_str}</span></div>
        <div class="dna-row"><span>Land Use</span><span>{agri_str}</span></div>
        <div class="dna-row"><span>Soil Base</span><span>{soil_str}</span></div>
        <div class="dna-row"><span>Hydrology</span><span>{perm_str}</span></div>
        <div class="dna-sensitivity">
            <div class="label">AI Sensitivity</div>
            <div class="val">{sens_score}%</div>
        </div>
    </div>
    """)

# -----------------------------------------------------------------------------
# SECTION 3: AI UNDERSTANDING
# -----------------------------------------------------------------------------
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
st.markdown("<div class='section-header'>AI Understanding</div>", unsafe_allow_html=True)

att_b_col = find_col(df_att, ["basin_id", "basin", "target_basin", "id"]) or df_att.columns[0]
df_att["clean_id"] = df_att[att_b_col].astype(str).str.capitalize()
att_data = df_att[df_att["clean_id"] == selected_display_id].copy()

if not att_data.empty:
    cols = [c for c in att_data.columns if c not in [att_b_col, "clean_id"]]
    feature_col = find_col(att_data, ["feature", "variable", "attribute", "name"]) or cols[0]
    val_col_name = [c for c in cols if c != feature_col][0] if len(cols) > 1 else cols[-1]
    att_data["raw_val"] = pd.to_numeric(att_data[val_col_name], errors="coerce").fillna(0.0)
    att_data["abs_val"] = att_data["raw_val"].abs()
    att_data = att_data.sort_values("abs_val", ascending=False)
else:
    feature_col = "feature"
    att_data = pd.DataFrame({
        "feature": ["Agriculture", "Clay", "Hydraulic Conductivity", "Elevation", "Bulk Density"],
        "raw_val": [42.0, 25.0, 18.0, 10.0, 5.0], "abs_val": [42.0, 25.0, 18.0, 10.0, 5.0]
    })

icon_map = {"Agriculture": "🌾", "Clay": "🪨", "Hydraulic": "💧", "Elevation": "⛰️", "Bulk": "🧱"}
max_val = max(att_data["abs_val"].max(), 1e-6)
bars_inner = ""

for _, row in att_data.iterrows():
    feat_name = str(row[feature_col])
    icon = next((v for k, v in icon_map.items() if k.lower() in feat_name.lower()), "🔹")
    val = float(row["raw_val"])
    abs_v = float(row["abs_val"])
    
    width_pct = (abs_v / max_val) * 100 if max_val > 1.0 else abs_v * 100
    width_pct = max(0.0, min(100.0, width_pct))
    display_pct = val * 100 if abs(val) <= 1.0 else val

    bars_inner += f"""
    <div class="ai-att-row">
        <div class="ai-att-label">
            <span class="feat"><span style="font-size:1.1rem;">{icon}</span> {feat_name}</span>
            <span class="pct">{display_pct:.1f}%</span>
        </div>
        <div class="ai-att-track">
            <div class="ai-att-fill" style="width: {width_pct:.1f}%;"></div>
        </div>
    </div>"""

render_html(f'<div class="glass-panel" style="max-width: 800px; margin: 0 auto;">{bars_inner}</div>')

# -----------------------------------------------------------------------------
# SECTION 4: BASIN INTELLIGENCE GALAXY
# -----------------------------------------------------------------------------
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
st.markdown("<div class='section-header'>Environmental Twin Network</div>", unsafe_allow_html=True)

emb_b_col = find_col(df_emb, ["basin_id", "basin", "target_basin", "id"]) or df_emb.columns[0]
num_cols = df_emb.select_dtypes(include=[np.number]).columns

if len(num_cols) >= 2:
    coords = df_emb[["dim1", "dim2"]].values if "dim1" in df_emb.columns else PCA(n_components=2).fit_transform(df_emb[num_cols].fillna(0))
else:
    coords = np.random.randn(len(df_emb), 2)

target_col = find_col(df_sim, ["target_basin", "basin_id", "basin"]) or df_sim.columns[0]
similar_col = find_col(df_sim, ["similar_basin", "twin_basin", "neighbor"]) or (df_sim.columns[1] if len(df_sim.columns)>1 else df_sim.columns[0])
score_col = find_col(df_sim, ["similarity_score", "similarity", "score"]) or df_sim.columns[-1]

df_sim["clean_target"] = df_sim[target_col].astype(str).str.capitalize()
sim_matches = df_sim[df_sim["clean_target"] == selected_display_id]
similar_ids = sim_matches[similar_col].astype(str).str.capitalize().tolist()[:3] if not sim_matches.empty else []

df_galaxy = pd.DataFrame({
    "basin_id": df_emb[emb_b_col].astype(str).str.capitalize(),
    "x": coords[:, 0], "y": coords[:, 1]
})

df_galaxy["Type"] = df_galaxy["basin_id"].apply(lambda b: "Selected Basin" if b == selected_display_id else ("Twin Network" if b in similar_ids else "Other Watersheds"))

fig_galaxy = px.scatter(
    df_galaxy, x="x", y="y", hover_name="basin_id", color="Type",
    color_discrete_map={"Selected Basin": "#fb7185", "Twin Network": "#0ea5e9", "Other Watersheds": "rgba(148, 163, 184, 0.2)"},
    size=df_galaxy["Type"].map({"Selected Basin": 18, "Twin Network": 12, "Other Watersheds": 5})
)
fig_galaxy.update_traces(marker=dict(line=dict(width=0)))
fig_galaxy.update_layout(
    template="plotly_dark",
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=""),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=""),
    margin=dict(l=0, r=0, t=0, b=0), height=450,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(color="#cbd5e1", size=12, family="Space Grotesk"))
)
st.plotly_chart(fig_galaxy, use_container_width=True, config={'displayModeBar': False})

# -----------------------------------------------------------------------------
# SECTION 5: RISK PROFILE
# -----------------------------------------------------------------------------
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
st.markdown("<div class='section-header'>Risk Profile</div>", unsafe_allow_html=True)

vuln_b_col = find_col(df_vuln, ["basin_id", "basin", "target_basin"]) or df_vuln.columns[0]
vuln_s_col = find_col(df_vuln, ["vulnerability", "score", "risk"]) or ([c for c in df_vuln.columns if c != vuln_b_col][0] if len(df_vuln.columns) > 1 else df_vuln.columns[-1])

df_vuln_sorted = df_vuln.copy()
df_vuln_sorted["clean_id"] = df_vuln_sorted[vuln_b_col].astype(str).str.capitalize()
df_vuln_sorted["raw_score"] = pd.to_numeric(df_vuln_sorted[vuln_s_col], errors="coerce").fillna(0)

max_raw = df_vuln_sorted["raw_score"].max()
if max_raw <= 1.0 and max_raw > 0:
    df_vuln_sorted["scaled_score"] = df_vuln_sorted["raw_score"] * 100.0
elif max_raw <= 10.0 and max_raw > 0:
    df_vuln_sorted["scaled_score"] = df_vuln_sorted["raw_score"] * 10.0
else:
    df_vuln_sorted["scaled_score"] = df_vuln_sorted["raw_score"]

df_vuln_sorted = df_vuln_sorted.sort_values("scaled_score", ascending=False).reset_index(drop=True)
df_vuln_sorted["rank"] = df_vuln_sorted.index + 1

target_row = df_vuln_sorted[df_vuln_sorted["clean_id"] == selected_display_id]
if target_row.empty:
    num_id = selected_display_id.replace("Basin_", "")
    target_row = df_vuln_sorted[df_vuln_sorted["clean_id"].str.contains(num_id)]

v_score = float(target_row["scaled_score"].values[0]) if not target_row.empty else 50.0
v_rank = int(target_row["rank"].values[0]) if not target_row.empty else 35
total_basins = len(df_vuln_sorted)

if v_score >= 70:
    risk_class = "risk-high"
    risk_text = "High Risk"
elif v_score >= 35:
    risk_class = "risk-med"
    risk_text = "Elevated Risk"
else:
    risk_class = "risk-low"
    risk_text = "Stable"

render_html(f"""
<div style="display: flex; justify-content: center; width: 100%;">
    <div class="risk-panel {risk_class}" style="width: 100%; max-width: 500px;">
        <div class="risk-label">Basin Risk Profile</div>
        <div class="risk-score">{v_score:.0f}<span style="font-size:2rem; opacity: 0.5;">%</span></div>
        <div class="risk-text">{risk_text}</div>
        <div class="risk-rank">Rank #{v_rank} of {total_basins}</div>
    </div>
</div>
""")
