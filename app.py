# app.py
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
from PIL import Image
import os
import json
import base64
from io import BytesIO
import time

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="HydroFoundation AI - Watershed Intelligence Platform",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# LOAD CUSTOM CSS
# ============================================

def load_css():
    """Load custom CSS from file or use inline"""
    try:
        with open('style.css', 'r') as f:
            css = f.read()
            st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        # Inline CSS if file doesn't exist
        st.markdown("""
        <style>
            /* Global styles */
            .main { padding: 0rem 1rem; }
            [data-testid="stAppViewContainer"] { background: #0a0e1a; }
            [data-testid="stSidebar"] { 
                background: rgba(10, 14, 26, 0.95); 
                border-right: 1px solid rgba(255, 255, 255, 0.05);
                padding: 1rem 0;
            }
            
            .sidebar-header { text-align: center; padding: 0.5rem 1rem 1rem 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); }
            .sidebar-logo { font-size: 2.5rem; margin-bottom: 0.3rem; }
            .sidebar-title { font-size: 1.2rem; font-weight: 600; color: #e2e8f0; letter-spacing: -0.5px; }
            .sidebar-subtitle { font-size: 0.75rem; color: #88c8e8; opacity: 0.7; font-weight: 300; }
            .sidebar-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; color: #718096; margin-bottom: 0.5rem; font-weight: 500; }
            .sidebar-footer { padding: 1rem 0 0 0; text-align: center; border-top: 1px solid rgba(255,255,255,0.05); }
            .footer-text { color: #4a5568; font-size: 0.75rem; }
            
            .stats-container { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem; padding: 0.5rem 0; }
            .stat-item { text-align: center; background: rgba(255,255,255,0.03); border-radius: 8px; padding: 0.5rem; border: 1px solid rgba(255,255,255,0.05); }
            .stat-value { font-size: 1.5rem; font-weight: 700; background: linear-gradient(135deg, #48bb78, #38a169); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
            .stat-label { font-size: 0.6rem; color: #718096; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 0.2rem; }
            
            .main-header { display: flex; justify-content: space-between; align-items: center; padding: 1rem 0 1.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 1.5rem; }
            .header-title { font-size: 2rem; font-weight: 700; color: #e2e8f0; letter-spacing: -0.5px; }
            .header-subtitle { font-size: 0.85rem; color: #a0aec0; font-weight: 300; margin-top: 0.2rem; }
            .header-badge { display: flex; gap: 0.5rem; }
            .badge { background: rgba(45,106,143,0.3); color: #88c8e8; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.7rem; font-weight: 500; border: 1px solid rgba(45,106,143,0.3); text-transform: uppercase; letter-spacing: 0.5px; }
            
            .ai-summary-card { background: linear-gradient(135deg, rgba(26,54,93,0.4), rgba(15,76,117,0.2)); border: 1px solid rgba(45,106,143,0.2); border-radius: 16px; padding: 1.2rem 1.5rem; margin-bottom: 1.5rem; backdrop-filter: blur(10px); }
            .summary-title { font-size: 0.9rem; font-weight: 600; color: #88c8e8; margin-bottom: 0.8rem; letter-spacing: 0.5px; }
            .summary-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }
            .summary-item { text-align: center; }
            .summary-icon { font-size: 1.5rem; margin-bottom: 0.2rem; }
            .summary-label { font-size: 0.65rem; color: #718096; text-transform: uppercase; letter-spacing: 0.5px; }
            .summary-value { font-size: 1rem; font-weight: 600; margin-top: 0.2rem; }
            
            .gallery-title { font-size: 1.1rem; font-weight: 600; color: #e2e8f0; margin: 1.5rem 0 1rem 0; }
            
            [data-testid="stTabs"] { margin-bottom: 1rem; }
            [data-testid="stTabs"] > div > div { gap: 0.5rem; }
            [data-testid="stTabs"] button { background: rgba(255,255,255,0.03) !important; border-radius: 10px !important; padding: 0.5rem 1.2rem !important; color: #a0aec0 !important; border: 1px solid rgba(255,255,255,0.05) !important; transition: all 0.3s !important; }
            [data-testid="stTabs"] button:hover { background: rgba(45,106,143,0.2) !important; border-color: rgba(45,106,143,0.3) !important; }
            [data-testid="stTabs"] button[aria-selected="true"] { background: linear-gradient(135deg, rgba(26,54,93,0.6), rgba(15,76,117,0.4)) !important; color: #e2e8f0 !important; border-color: rgba(45,106,143,0.4) !important; box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important; }
            
            [data-testid="stImage"] { border-radius: 12px; overflow: hidden; border: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.2); }
            [data-testid="stImage"] img { width: 100%; height: auto; }
            
            .comparison-label { font-size: 0.85rem; font-weight: 500; color: #a0aec0; margin-bottom: 0.5rem; text-align: center; }
            
            [data-testid="stMap"] { border-radius: 12px; overflow: hidden; border: 1px solid rgba(255,255,255,0.05); }
            
            .footer { margin-top: 2rem; padding: 1rem; text-align: center; color: #4a5568; font-size: 0.75rem; border-top: 1px solid rgba(255,255,255,0.03); }
            .footer span { margin: 0 0.3rem; }
            
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .stDeployButton {display: none;}
            
            ::-webkit-scrollbar { width: 8px; height: 8px; }
            ::-webkit-scrollbar-track { background: #0a0e1a; }
            ::-webkit-scrollbar-thumb { background: #1a365d; border-radius: 4px; }
            ::-webkit-scrollbar-thumb:hover { background: #2d6a8f; }
            
            @media (max-width: 768px) {
                .summary-grid { grid-template-columns: repeat(2, 1fr); }
                .main-header { flex-direction: column; align-items: flex-start; gap: 0.5rem; }
                .header-title { font-size: 1.5rem; }
            }
        </style>
        """, unsafe_allow_html=True)

load_css()

# ============================================
# SESSION STATE
# ============================================

if 'basin_id' not in st.session_state:
    st.session_state.basin_id = 1
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'
if 'fullscreen' not in st.session_state:
    st.session_state.fullscreen = False
if 'fullscreen_image' not in st.session_state:
    st.session_state.fullscreen_image = None

# ============================================
# DATA LOADING
# ============================================

@st.cache_data
def load_metadata():
    """Load project metadata"""
    metadata_path = "assets/metadata.json"
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            return json.load(f)
    return {
        "basins": 71,
        "channels": 15,
        "height": 64,
        "width": 64,
        "variables": ["dem", "clay", "bdod", "hydraulic_conductivity", "agriculture"]
    }

@st.cache_data
def load_basin_image(basin_id, image_type):
    """Load basin image from outputs folder"""
    image_map = {
        'input': 'input.png',
        'vulnerability': 'vulnerability_map.png',
        'attention': 'attention_map.png',
        'digital_twin': 'digital_twin.png'
    }
    
    filename = image_map.get(image_type)
    if not filename:
        return None
    
    basin_path = f"assets/basin_outputs/basin_{basin_id:03d}/{filename}"
    if os.path.exists(basin_path):
        return Image.open(basin_path)
    
    global_path = f"assets/figures/{filename}"
    if os.path.exists(global_path):
        return Image.open(global_path)
    
    return None

@st.cache_data
def load_all_basin_images(basin_id):
    """Load all images for a basin"""
    images = {}
    for img_type in ['input', 'vulnerability', 'attention', 'digital_twin']:
        images[img_type] = load_basin_image(basin_id, img_type)
    return images

# ============================================
# HELPER FUNCTIONS
# ============================================

def create_similarity_summary(basin_id):
    """Generate AI summary card based on basin characteristics"""
    summaries = {
        1: {"terrain": "High", "soil": "Medium", "hydraulic": "High", "agriculture": "Low"},
        2: {"terrain": "Medium", "soil": "High", "hydraulic": "Medium", "agriculture": "High"},
        3: {"terrain": "Low", "soil": "Medium", "hydraulic": "Low", "agriculture": "High"},
        4: {"terrain": "High", "soil": "High", "hydraulic": "High", "agriculture": "Medium"},
        5: {"terrain": "Medium", "soil": "Low", "hydraulic": "Medium", "agriculture": "Low"},
    }
    
    default = {"terrain": "Medium", "soil": "Medium", "hydraulic": "Medium", "agriculture": "Medium"}
    summary = summaries.get(basin_id, default)
    
    icons = {"terrain": "⛰️", "soil": "🌱", "hydraulic": "💧", "agriculture": "🌾"}
    colors = {"High": "#48bb78", "Medium": "#f6ad55", "Low": "#fc8181"}
    
    html = """
    <div class="ai-summary-card">
        <div class="summary-title">🧠 AI Environmental Summary</div>
        <div class="summary-grid">
    """
    
    for key, value in summary.items():
        html += f"""
        <div class="summary-item">
            <div class="summary-icon">{icons.get(key, '📊')}</div>
            <div class="summary-label">{key.capitalize()}</div>
            <div class="summary-value" style="color: {colors.get(value, '#a0aec0')}">{value}</div>
        </div>
        """
    
    html += """
        </div>
    </div>
    """
    
    return html

# ============================================
# MAIN APPLICATION
# ============================================

# Load metadata
metadata = load_metadata()
total_basins = metadata.get('basins', 71)

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-logo">🌊</div>
        <div class="sidebar-title">HydroFoundation</div>
        <div class="sidebar-subtitle">Watershed Intelligence</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<div class="sidebar-label">Select Basin</div>', unsafe_allow_html=True)
    
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
    
    st.markdown("---")
    
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-item">
            <div class="stat-value">{total_basins}</div>
            <div class="stat-label">Basins</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">15</div>
            <div class="stat-label">Layers</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">128</div>
            <div class="stat-label">Embedding</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    theme = st.toggle("🌙 Dark Mode", value=st.session_state.theme == 'dark')
    if theme != (st.session_state.theme == 'dark'):
        st.session_state.theme = 'dark' if theme else 'light'
        st.rerun()
    
    st.markdown('<div class="sidebar-label">Export</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Images", use_container_width=True):
            st.info("Download functionality coming soon")
    with col2:
        if st.button("📊 Report", use_container_width=True):
            st.info("Report generation coming soon")
    
    st.markdown("---")
    
    st.markdown("""
    <div class="sidebar-footer">
        <div class="footer-text">v2.0 • PhD Research</div>
        <div class="footer-text" style="font-size: 0.65rem; opacity: 0.5;">Powered by BASINGRID</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# MAIN CONTENT
# ============================================

# Load images for current basin
images = load_all_basin_images(basin_id)

# ============================================
# HEADER
# ============================================

st.markdown(f"""
<div class="main-header">
    <div>
        <div class="header-title">🌊 Basin {basin_id:03d}</div>
        <div class="header-subtitle">Interactive watershed intelligence and environmental analysis</div>
    </div>
    <div class="header-badge">
        <span class="badge">AI Generated</span>
        <span class="badge">Real-time</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# AI SUMMARY CARD
# ============================================

st.markdown(create_similarity_summary(basin_id), unsafe_allow_html=True)

# ============================================
# IMAGE GALLERY
# ============================================

st.markdown('<div class="gallery-title">Environmental Intelligence</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🖼️ Overview", "🌋 Vulnerability", "🧠 Attention", "🛰️ Digital Twin"])

with tab1:
    if images.get('input'):
        st.image(images['input'], use_container_width=True)
    else:
        st.info("Input image not available")

with tab2:
    if images.get('vulnerability'):
        st.image(images['vulnerability'], use_container_width=True)
    else:
        st.info("Vulnerability map not available")

with tab3:
    if images.get('attention'):
        st.image(images['attention'], use_container_width=True)
    else:
        st.info("Attention map not available")

with tab4:
    if images.get('digital_twin'):
        st.image(images['digital_twin'], use_container_width=True)
    else:
        st.info("Digital twin not available")

# ============================================
# COMPARISON VIEW
# ============================================

st.markdown('<div class="gallery-title">Input vs AI Interpretation</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="comparison-label">Original Basin</div>', unsafe_allow_html=True)
    if images.get('input'):
        st.image(images['input'], use_container_width=True)
    else:
        st.info("No input image")

with col2:
    st.markdown('<div class="comparison-label">AI Interpretation</div>', unsafe_allow_html=True)
    if images.get('vulnerability'):
        st.image(images['vulnerability'], use_container_width=True)
    else:
        st.info("No AI interpretation")

# ============================================
# INTERACTIVE MAP - Fixed Version
# ============================================

st.markdown('<div class="gallery-title">Interactive Basin Explorer</div>', unsafe_allow_html=True)

np.random.seed(42)
map_data = pd.DataFrame({
    'lat': np.random.uniform(25, 45, total_basins),
    'lon': np.random.uniform(-125, -65, total_basins),
    'basin': [f"Basin {i:03d}" for i in range(1, total_basins + 1)]
})

# Create size column with highlighted basin
map_data['size'] = 10
map_data.loc[basin_id - 1, 'size'] = 25

# Use st.map without color parameter (uses default coloring)
st.map(map_data[['lat', 'lon']], size=map_data['size'])

# Add a note about the highlighted basin
st.caption(f"📍 Basin {basin_id:03d} highlighted in the map above")

# ============================================
# FOOTER
# ============================================

st.markdown("""
<div class="footer">
    <span>HydroFoundation v2.0</span>
    <span>•</span>
    <span>PhD Research Prototype</span>
    <span>•</span>
    <span>Powered by BASINGRID Dataset</span>
</div>
""", unsafe_allow_html=True)
