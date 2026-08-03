# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from PIL import Image
import os
import json
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import time

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="HydroFoundation - Watershed Intelligence Platform",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<style>
    /* Reset and base */
    .main { padding: 0rem 1.5rem; }
    [data-testid="stAppViewContainer"] { 
        background: linear-gradient(135deg, #0a0e1a 0%, #1a1a2e 50%, #16213e 100%);
    }
    [data-testid="stHeader"] { background: transparent; }
    
    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Glass cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.4);
        border-color: rgba(45, 106, 143, 0.3);
    }
    
    /* Header */
    .header-container {
        text-align: center;
        padding: 1.5rem 0 1rem 0;
        margin-bottom: 1rem;
    }
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #48bb78, #2d6a8f, #88c8e8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.5px;
    }
    .header-subtitle {
        font-size: 0.9rem;
        color: #88c8e8;
        opacity: 0.7;
        font-weight: 300;
        margin-top: 0.2rem;
    }
    
    /* Selector */
    .selector-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1.5rem;
        padding: 0.5rem 0 1.5rem 0;
    }
    .selector-label {
        font-size: 0.9rem;
        font-weight: 500;
        color: #a0aec0;
        letter-spacing: 0.5px;
    }
    
    /* Custom select */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: white !important;
        min-width: 200px;
    }
    .stSelectbox label { display: none !important; }
    
    /* Section headers */
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #88c8e8;
        padding: 0.5rem 0 0.8rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        margin-bottom: 1rem;
        letter-spacing: 0.5px;
    }
    
    /* Image containers */
    .image-wrapper {
        border-radius: 12px;
        overflow: hidden;
        background: rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
    }
    .image-wrapper:hover {
        border-color: rgba(45, 106, 143, 0.3);
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .image-wrapper img {
        width: 100%;
        height: auto;
        display: block;
    }
    
    /* DNA Card */
    .dna-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .dna-item {
        display: flex;
        justify-content: space-between;
        padding: 0.4rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.03);
    }
    .dna-label {
        color: #a0aec0;
        font-size: 0.8rem;
    }
    .dna-value {
        color: #e2e8f0;
        font-weight: 500;
        font-size: 0.85rem;
    }
    
    /* Risk indicators */
    .risk-low { color: #48bb78; }
    .risk-medium { color: #f6ad55; }
    .risk-high { color: #fc8181; }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
        color: #4a5568;
        font-size: 0.7rem;
        border-top: 1px solid rgba(255,255,255,0.03);
        margin-top: 1.5rem;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main { padding: 0rem 0.5rem; }
        .header-title { font-size: 1.8rem; }
        .selector-container { flex-direction: column; gap: 0.5rem; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE
# ============================================

if 'basin_id' not in st.session_state:
    st.session_state.basin_id = 1

# ============================================
# DATA LOADING
# ============================================

@st.cache_data
def load_csv(filename):
    """Load CSV from assets/tables/"""
    path = f"assets/tables/{filename}"
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

@st.cache_data
def load_basin_image(basin_id, image_type):
    """Load basin image"""
    image_map = {
        'input': 'input.png',
        'vulnerability': 'vulnerability_map.png',
        'attention': 'attention_map.png',
        'digital_twin': 'digital_twin.png'
    }
    filename = image_map.get(image_type)
    if not filename:
        return None
    
    path = f"assets/basin_outputs/basin_{basin_id:03d}/{filename}"
    if os.path.exists(path):
        return Image.open(path)
    return None

# ============================================
# PLOT FUNCTIONS
# ============================================

def create_radar_chart(values, categories, title):
    """Create radar chart for environmental DNA"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Basin Profile',
        line=dict(color='#2d6a8f', width=2),
        fillcolor='rgba(45, 106, 143, 0.3)'
    ))
    
    fig.update_layout(
        template='plotly_dark',
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                showticklabels=False,
                gridcolor='rgba(255,255,255,0.1)'
            ),
            angularaxis=dict(
                tickfont=dict(color='#a0aec0', size=9),
                gridcolor='rgba(255,255,255,0.05)'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=False,
        height=350,
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_similarity_map(embeddings, highlight_idx):
    """Create UMAP/PCA similarity map"""
    if embeddings is None or len(embeddings) < 2:
        return None
    
    # Use PCA for simplicity
    pca = PCA(n_components=2, random_state=42)
    coords = pca.fit_transform(embeddings)
    
    fig = go.Figure()
    
    # All points
    fig.add_trace(go.Scatter(
        x=coords[:, 0],
        y=coords[:, 1],
        mode='markers',
        marker=dict(
            size=10,
            color='#2d6a8f',
            opacity=0.5,
            line=dict(color='white', width=0.5)
        ),
        text=[f'Basin {i+1:03d}' for i in range(len(embeddings))],
        hovertemplate='%{text}<extra></extra>',
        name='Basins'
    ))
    
    # Highlight selected
    if highlight_idx is not None and highlight_idx < len(embeddings):
        fig.add_trace(go.Scatter(
            x=[coords[highlight_idx, 0]],
            y=[coords[highlight_idx, 1]],
            mode='markers',
            marker=dict(
                size=20,
                color='#fc8181',
                symbol='star',
                line=dict(color='white', width=2)
            ),
            text=f'Basin {highlight_idx+1:03d} (Selected)',
            hovertemplate='%{text}<extra></extra>',
            name='Selected'
        ))
    
    fig.update_layout(
        template='plotly_dark',
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        showlegend=False
    )
    
    return fig

def create_risk_bar(vulnerability_scores, basin_id):
    """Create risk visualization"""
    if vulnerability_scores is None:
        return None
    
    # Get selected basin risk
    basin_row = vulnerability_scores[vulnerability_scores['basin_id'] == basin_id]
    if len(basin_row) == 0:
        return None
    
    risk_score = basin_row['vulnerability_score'].values[0]
    
    # Determine risk level
    if risk_score < 0.33:
        level = "Low"
        color = "#48bb78"
        emoji = "🟢"
    elif risk_score < 0.66:
        level = "Medium"
        color = "#f6ad55"
        emoji = "🟡"
    else:
        level = "High"
        color = "#fc8181"
        emoji = "🔴"
    
    # Create gauge
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = risk_score * 100,
        title = {'text': f"Risk Level: {level}", 'font': {'color': '#a0aec0', 'size': 14}},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#4a5568"},
            'bar': {'color': color},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 33], 'color': 'rgba(72, 187, 120, 0.2)'},
                {'range': [33, 66], 'color': 'rgba(246, 173, 85, 0.2)'},
                {'range': [66, 100], 'color': 'rgba(252, 129, 129, 0.2)'}
            ]
        }
    ))
    
    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#e2e8f0'}
    )
    
    return fig

# ============================================
# MAIN APPLICATION
# ============================================

# Load data
env_profile = load_csv('basin_environment_profile.csv')
vulnerability_scores = load_csv('basin_vulnerability_scores.csv')
embeddings_df = load_csv('basin_embeddings.csv')
similar_basins = load_csv('similar_basins.csv')
attention_features = load_csv('attention_features.csv')

# Get basin count
total_basins = 71
if env_profile is not None:
    total_basins = len(env_profile)

# ============================================
# HEADER
# ============================================

st.markdown("""
<div class="header-container">
    <div class="header-title">🌊 HydroFoundation</div>
    <div class="header-subtitle">AI-Powered Watershed Intelligence Platform</div>
</div>
""", unsafe_allow_html=True)

# ============================================
# BASIN SELECTOR
# ============================================

st.markdown('<div class="selector-container">', unsafe_allow_html=True)
st.markdown('<span class="selector-label">Select Basin</span>', unsafe_allow_html=True)

basin_id = st.selectbox(
    "Basin",
    options=list(range(1, total_basins + 1)),
    format_func=lambda x: f"Basin {x:03d}",
    index=st.session_state.basin_id - 1,
    label_visibility="collapsed"
)

if basin_id != st.session_state.basin_id:
    st.session_state.basin_id = basin_id
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# SECTION 1: DIGITAL TWIN
# ============================================

st.markdown('<div class="section-header">🏔 Basin Digital Twin</div>', unsafe_allow_html=True)

# Load images
input_img = load_basin_image(basin_id, 'input')
vuln_img = load_basin_image(basin_id, 'vulnerability')
attn_img = load_basin_image(basin_id, 'attention')
twin_img = load_basin_image(basin_id, 'digital_twin')

col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p style="color:#a0aec0;font-size:0.75rem;text-align:center;margin-bottom:0.5rem;">Input Environment</p>', unsafe_allow_html=True)
        if input_img:
            st.image(input_img, use_container_width=True)
        else:
            st.info("No input image")
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p style="color:#a0aec0;font-size:0.75rem;text-align:center;margin-bottom:0.5rem;">AI Vulnerability</p>', unsafe_allow_html=True)
        if vuln_img:
            st.image(vuln_img, use_container_width=True)
        else:
            st.info("No vulnerability map")
        st.markdown('</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p style="color:#a0aec0;font-size:0.75rem;text-align:center;margin-bottom:0.5rem;">AI Attention</p>', unsafe_allow_html=True)
        if attn_img:
            st.image(attn_img, use_container_width=True)
        else:
            st.info("No attention map")
        st.markdown('</div>', unsafe_allow_html=True)

with col4:
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p style="color:#a0aec0;font-size:0.75rem;text-align:center;margin-bottom:0.5rem;">Digital Twin</p>', unsafe_allow_html=True)
        if twin_img:
            st.image(twin_img, use_container_width=True)
        else:
            st.info("No digital twin")
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# SECTION 2: ENVIRONMENTAL DNA
# ============================================

st.markdown('<div class="section-header">🧬 Environmental DNA</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])

with col1:
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        if env_profile is not None:
            # Get basin profile
            basin_row = env_profile[env_profile['basin_id'] == basin_id]
            if len(basin_row) > 0:
                # Create radar chart
                categories = ['Elevation', 'Clay', 'Bulk Density', 'Hydraulic Conductivity', 'Agriculture']
                values = [
                    basin_row['elevation'].values[0],
                    basin_row['clay'].values[0],
                    basin_row['bulk_density'].values[0],
                    basin_row['hydraulic_conductivity'].values[0],
                    basin_row['agriculture'].values[0]
                ]
                # Normalize values to 0-1 range
                values = np.clip(values, 0, 1)
                
                fig = create_radar_chart(values, categories, "Environmental Signature")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No environmental profile available")
        else:
            st.info("Environmental profile not loaded")
        
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p style="color:#88c8e8;font-size:0.85rem;font-weight:500;margin-bottom:0.8rem;">Basin DNA Profile</p>', unsafe_allow_html=True)
        
        if env_profile is not None:
            basin_row = env_profile[env_profile['basin_id'] == basin_id]
            if len(basin_row) > 0:
                row = basin_row.iloc[0]
                
                # Map values to descriptive text
                terrain = "High" if row['elevation'] > 0.6 else "Medium" if row['elevation'] > 0.3 else "Low"
                land_use = "High" if row['agriculture'] > 0.6 else "Medium" if row['agriculture'] > 0.3 else "Low"
                soil = "Clay dominated" if row['clay'] > 0.5 else "Mixed" if row['clay'] > 0.3 else "Sandy"
                water = "High" if row['hydraulic_conductivity'] > 0.6 else "Medium" if row['hydraulic_conductivity'] > 0.3 else "Low"
                
                risk_level = "High" if row['vulnerability'] > 0.6 else "Medium" if row['vulnerability'] > 0.3 else "Low"
                risk_color = "#fc8181" if risk_level == "High" else "#f6ad55" if risk_level == "Medium" else "#48bb78"
                
                st.markdown(f"""
                <div class="dna-card">
                    <div class="dna-item">
                        <span class="dna-label">🌄 Terrain</span>
                        <span class="dna-value">{terrain} elevation</span>
                    </div>
                    <div class="dna-item">
                        <span class="dna-label">🌱 Land Use</span>
                        <span class="dna-value">{land_use} agriculture</span>
                    </div>
                    <div class="dna-item">
                        <span class="dna-label">🟫 Soil</span>
                        <span class="dna-value">{soil}</span>
                    </div>
                    <div class="dna-item">
                        <span class="dna-label">💧 Water Movement</span>
                        <span class="dna-value">{water} permeability</span>
                    </div>
                    <div class="dna-item">
                        <span class="dna-label">🔥 AI Risk</span>
                        <span class="dna-value" style="color:{risk_color}">{risk_level} ({int(row['vulnerability']*100)}%)</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Profile data not available")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# SECTION 3: ATTENTION FINGERPRINT
# ============================================

st.markdown('<div class="section-header">🧠 AI Attention Fingerprint</div>', unsafe_allow_html=True)

if attention_features is not None:
    basin_attn = attention_features[attention_features['basin_id'] == basin_id]
    
    if len(basin_attn) > 0:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p style="color:#a0aec0;font-size:0.75rem;text-align:center;margin-bottom:0.8rem;">What does AI consider important?</p>', unsafe_allow_html=True)
        
        # Get attention scores
        attn_cols = ['agriculture', 'clay', 'hydraulic_conductivity', 'elevation', 'bulk_density']
        attn_values = []
        attn_labels = ['Agriculture', 'Clay', 'Hydraulic Conductivity', 'Elevation', 'Bulk Density']
        
        for col in attn_cols:
            if col in basin_attn.columns:
                attn_values.append(basin_attn[col].values[0])
            else:
                attn_values.append(0.2)
        
        # Normalize
        attn_values = np.array(attn_values)
        attn_values = attn_values / attn_values.sum() if attn_values.sum() > 0 else np.ones(len(attn_values)) / len(attn_values)
        
        # Create custom progress bars
        colors = ['#48bb78', '#63b3ed', '#f6ad55', '#fc8181', '#b794f4']
        
        for label, value, color in zip(attn_labels, attn_values, colors):
            pct = int(value * 100)
            st.markdown(f"""
            <div style="margin:0.3rem 0;">
                <div style="display:flex;justify-content:space-between;font-size:0.75rem;color:#a0aec0;">
                    <span>{label}</span>
                    <span>{pct}%</span>
                </div>
                <div style="background:rgba(255,255,255,0.05);border-radius:4px;height:6px;overflow:hidden;">
                    <div style="background:{color};width:{pct}%;height:100%;border-radius:4px;transition:width 1s ease;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Attention features not available for this basin")
else:
    st.info("Attention data not loaded")

# ============================================
# SECTION 4: SIMILARITY GALAXY
# ============================================

st.markdown('<div class="section-header">🌐 Watershed Similarity Galaxy</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])

with col1:
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        if embeddings_df is not None:
            # Prepare embeddings
            emb_cols = [col for col in embeddings_df.columns if col != 'basin_id']
            embeddings = embeddings_df[emb_cols].values
            
            fig = create_similarity_map(embeddings, basin_id - 1)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Embeddings not loaded")
        
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p style="color:#88c8e8;font-size:0.85rem;font-weight:500;margin-bottom:0.8rem;">Closest Environmental Twins</p>', unsafe_allow_html=True)
        
        if similar_basins is not None:
            basin_sim = similar_basins[similar_basins['basin_id'] == basin_id]
            if len(basin_sim) > 0:
                # Get top 5 similar basins
                sim_cols = [col for col in basin_sim.columns if col != 'basin_id']
                top_sim = basin_sim[sim_cols].iloc[0].sort_values(ascending=False).head(5)
                
                for idx, (basin, score) in enumerate(top_sim.items()):
                    basin_num = int(basin.split('_')[1]) if '_' in basin else int(basin)
                    color = '#48bb78' if score > 0.8 else '#f6ad55' if score > 0.6 else '#a0aec0'
                    st.markdown(f"""
                    <div style="display:flex;justify-content:space-between;padding:0.3rem 0;border-bottom:1px solid rgba(255,255,255,0.03);">
                        <span style="color:#e2e8f0;font-size:0.85rem;">Basin {basin_num:03d}</span>
                        <span style="color:{color};font-weight:500;font-size:0.85rem;">{score*100:.0f}%</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No similarity data available")
        else:
            st.info("Similarity data not loaded")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# SECTION 5: RISK ASSESSMENT
# ============================================

st.markdown('<div class="section-header">🔥 Watershed Risk Assessment</div>', unsafe_allow_html=True)

if vulnerability_scores is not None:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.container():
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            
            # Create risk gauge
            fig = create_risk_bar(vulnerability_scores, basin_id)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            # Show risk ranking
            all_risks = vulnerability_scores.sort_values('vulnerability_score', ascending=False)
            rank = all_risks[all_risks['basin_id'] == basin_id].index[0] + 1 if len(all_risks) > 0 else 0
            
            st.markdown(f"""
            <div style="text-align:center;padding:0.5rem 0;">
                <span style="color:#a0aec0;font-size:0.8rem;">Risk Ranking: </span>
                <span style="color:#e2e8f0;font-weight:600;font-size:1rem;">#{rank} of {len(all_risks)}</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Vulnerability data not loaded")

# ============================================
# FOOTER
# ============================================

st.markdown(f"""
<div class="footer">
    Basin {basin_id:03d} of {total_basins} • Powered by HydroFoundation AI • PhD Research Prototype
</div>
""", unsafe_allow_html=True)
