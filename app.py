<<<<<<< HEAD
<<<<<<< Updated upstream
=======
# app.py
>>>>>>> Stashed changes
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
<<<<<<< Updated upstream
import base64
=======
# app.py
import streamlit as st
from PIL import Image
import os
import json
>>>>>>> ddd9d7a55759e9ba4b3e233cf4248ba196bcc625
import time
=======
import json
from PIL import Image
import base64
from io import BytesIO

# ============================================
# PAGE CONFIGURATION
# ============================================
>>>>>>> Stashed changes

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
<<<<<<< Updated upstream
    page_title="HydroFoundation Basin Explorer",
<<<<<<< HEAD
=======
    page_title="HydroFoundation - Basin Intelligence Explorer",
    page_icon="🌊",
>>>>>>> Stashed changes
=======
    page_icon="🌊",
>>>>>>> ddd9d7a55759e9ba4b3e233cf4248ba196bcc625
    layout="wide",
    initial_sidebar_state="collapsed"
)

<<<<<<< HEAD
<<<<<<< Updated upstream
# 2. Load Custom CSS
def load_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
=======
# ============================================
# LOAD CUSTOM CSS
# ============================================
>>>>>>> ddd9d7a55759e9ba4b3e233cf4248ba196bcc625

def load_css():
    try:
        with open('style.css', 'r') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.markdown("""
        <style>
            /* Reset and base */
            .main { padding: 0rem 2rem; }
            [data-testid="stAppViewContainer"] { 
                background: #f8fafc;
            }
            [data-testid="stHeader"] { background: transparent; }
            
            /* Hide default elements */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .stDeployButton {display: none;}
            
            /* Header */
            .header-container {
                text-align: center;
                padding: 2rem 0 1.5rem 0;
                border-bottom: 2px solid #e2e8f0;
                margin-bottom: 2rem;
            }
            .header-title {
                font-size: 2.5rem;
                font-weight: 700;
                color: #0a1628;
                letter-spacing: -0.5px;
            }
            .header-title span {
                background: linear-gradient(135deg, #1a365d, #2d6a8f);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            .header-subtitle {
                font-size: 0.9rem;
                color: #718096;
                margin-top: 0.3rem;
                font-weight: 300;
            }
            
            /* Selector */
            .selector-container {
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 1rem;
                padding: 1rem 0 2rem 0;
            }
            .selector-label {
                font-size: 0.9rem;
                font-weight: 500;
                color: #2d3748;
            }
            
            /* Image cards */
            .image-card {
                background: white;
                border-radius: 16px;
                padding: 1.2rem;
                box-shadow: 0 4px 20px rgba(0,0,0,0.06);
                transition: all 0.3s ease;
                border: 1px solid #e2e8f0;
                margin-bottom: 1.5rem;
            }
            .image-card:hover {
                box-shadow: 0 8px 40px rgba(0,0,0,0.1);
                transform: translateY(-2px);
            }
            .image-title {
                font-size: 0.85rem;
                font-weight: 600;
                color: #2d3748;
                text-align: center;
                margin-bottom: 0.8rem;
                letter-spacing: 0.3px;
                text-transform: uppercase;
                font-size: 0.75rem;
                color: #718096;
            }
            .image-wrapper {
                border-radius: 12px;
                overflow: hidden;
                background: #f7fafc;
                position: relative;
            }
            .image-wrapper img {
                width: 100%;
                height: auto;
                display: block;
                transition: transform 0.3s ease;
            }
            .image-wrapper:hover img {
                transform: scale(1.02);
            }
            
            /* Loading spinner */
            .loading-container {
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 3rem;
            }
            .spinner {
                border: 4px solid #e2e8f0;
                border-top: 4px solid #2d6a8f;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            /* Footer */
            .footer {
                text-align: center;
                padding: 2rem 0 1rem 0;
                color: #a0aec0;
                font-size: 0.75rem;
                border-top: 1px solid #e2e8f0;
                margin-top: 2rem;
            }
            
            /* Responsive */
            @media (max-width: 768px) {
                .main { padding: 0rem 1rem; }
                .header-title { font-size: 1.8rem; }
                .selector-container { flex-direction: column; gap: 0.5rem; }
                .image-card { padding: 0.8rem; }
            }
            
            /* Custom select box */
            .stSelectbox > div > div {
                border-radius: 10px !important;
                border: 2px solid #e2e8f0 !important;
                background: white !important;
                min-width: 200px;
            }
            .stSelectbox label {
                display: none !important;
            }
        </style>
        """, unsafe_allow_html=True)

load_css()

# ============================================
# SESSION STATE
# ============================================

if 'basin_id' not in st.session_state:
    st.session_state.basin_id = 1

if 'loading' not in st.session_state:
    st.session_state.loading = False

# ============================================
# DATA LOADING
# ============================================

@st.cache_data
def load_metadata():
    """Load metadata to get basin count"""
    try:
        with open('assets/metadata.json', 'r') as f:
            return json.load(f)
    except:
        return {"basins": 71}

@st.cache_data
def load_basin_image(basin_id, image_type):
    """Load specific image for a basin"""
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
    
    # Fallback to global figures
    fallback_path = f"assets/figures/{filename}"
    if os.path.exists(fallback_path):
        return Image.open(fallback_path)
    
    return None

@st.cache_data
def load_all_images(basin_id):
    """Load all four images for a basin"""
    images = {}
    for img_type in ['input', 'vulnerability', 'attention', 'digital_twin']:
        images[img_type] = load_basin_image(basin_id, img_type)
    return images

# ============================================
# MAIN APPLICATION
# ============================================

# Load metadata
metadata = load_metadata()
total_basins = metadata.get('basins', 71)

# ============================================
# HEADER
# ============================================

st.markdown("""
<div class="header-container">
    <div class="header-title">🌊 HydroFoundation <span>Basin Explorer</span></div>
    <div class="header-subtitle">Interactive AI-powered watershed visualization</div>
</div>
""", unsafe_allow_html=True)

# ============================================
# BASIN SELECTOR
# ============================================

st.markdown('<div class="selector-container">', unsafe_allow_html=True)
st.markdown('<span class="selector-label">Select Basin</span>', unsafe_allow_html=True)

basin_id = st.selectbox(
    "Select Basin",
    options=list(range(1, total_basins + 1)),
    format_func=lambda x: f"Basin {x:03d}",
    index=st.session_state.basin_id - 1,
    label_visibility="collapsed"
)

if basin_id != st.session_state.basin_id:
    st.session_state.basin_id = basin_id
    st.session_state.loading = True
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# LOAD IMAGES
# ============================================

images = load_all_images(basin_id)

# ============================================
# ROW 1: INPUT IMAGE
# ============================================

st.markdown('<div class="image-card">', unsafe_allow_html=True)
st.markdown('<div class="image-title">Input Basin</div>', unsafe_allow_html=True)

if images.get('input'):
    st.image(images['input'], use_container_width=True)
else:
    st.info("No input image available")

st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# ROW 2: ATTENTION + VULNERABILITY
# ============================================

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="image-card">', unsafe_allow_html=True)
    st.markdown('<div class="image-title">Attention Map</div>', unsafe_allow_html=True)
    
    if images.get('attention'):
        st.image(images['attention'], use_container_width=True)
    else:
        st.info("No attention map available")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="image-card">', unsafe_allow_html=True)
    st.markdown('<div class="image-title">Vulnerability Map</div>', unsafe_allow_html=True)
    
    if images.get('vulnerability'):
        st.image(images['vulnerability'], use_container_width=True)
    else:
        st.info("No vulnerability map available")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# ROW 3: DIGITAL TWIN
# ============================================

st.markdown('<div class="image-card">', unsafe_allow_html=True)
st.markdown('<div class="image-title">Digital Twin</div>', unsafe_allow_html=True)

if images.get('digital_twin'):
    # Center the image with constrained width
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
<<<<<<< HEAD
        render_card("Vulnerability Map", img_vuln, "width-100")
        
    # --- ROW 3: Digital Twin (~70% width, centered) ---
    render_card("Digital Twin", img_dt, "width-70")
=======
# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<style>
    /* Main container */
    .main {
        padding: 0rem 1rem;
        background: #0a0e1a;
    }
    
    /* Header */
    .header-container {
        background: linear-gradient(135deg, #0a1628 0%, #1a365d 50%, #0f4c75 100%);
        padding: 1.2rem 2rem;
        border-radius: 14px;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    }
    
    .header-title {
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 0.1rem;
    }
    
    .header-subtitle {
        color: #88c8e8;
        font-size: 0.9rem;
        font-weight: 300;
        opacity: 0.8;
    }
    
    /* Section containers */
    .section-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    
    .section-title {
        color: #88c8e8;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.8rem;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Basin selector card */
    .selector-card {
        background: linear-gradient(135deg, rgba(26, 54, 93, 0.4), rgba(15, 76, 117, 0.2));
        border: 1px solid rgba(45, 106, 143, 0.3);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 2rem;
    }
    
    .selector-label {
        color: #a0aec0;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Image cards */
    .image-card {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 10px;
        padding: 0.5rem;
        overflow: hidden;
    }
    
    .image-card img {
        width: 100%;
        border-radius: 8px;
    }
    
    .image-label {
        color: #a0aec0;
        font-size: 0.8rem;
        text-align: center;
        padding: 0.3rem 0;
        font-weight: 400;
    }
    
    /* Info panel */
    .info-panel {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 1rem;
    }
    
    .info-row {
        display: flex;
        justify-content: space-between;
        padding: 0.3rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.03);
    }
    
    .info-label {
        color: #718096;
        font-size: 0.8rem;
    }
    
    .info-value {
        color: #e2e8f0;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    /* Comparison slider */
    .comparison-container {
        position: relative;
        overflow: hidden;
        border-radius: 10px;
    }
    
    /* Footer */
    .footer {
        background: rgba(255, 255, 255, 0.02);
        padding: 0.8rem 1.5rem;
        border-radius: 10px;
        margin-top: 1.5rem;
        text-align: center;
        color: #4a5568;
        font-size: 0.75rem;
        border: 1px solid rgba(255, 255, 255, 0.03);
    }
    
    /* Custom select box */
    .stSelectbox > div > div {
        background: rgba(26, 54, 93, 0.4) !important;
        border: 1px solid rgba(45, 106, 143, 0.3) !important;
        border-radius: 8px !important;
        color: white !important;
    }
    
    .stSelectbox label {
        color: #a0aec0 !important;
        font-weight: 500 !important;
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0a0e1a;
    }
    ::-webkit-scrollbar-thumb {
        background: #1a365d;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #2d6a8f;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# DATA LOADING FUNCTIONS
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
def load_basin_image(basin_id):
    """Load basin input image"""
    image_path = f"assets/basin_images/basin_{basin_id:03d}.png"
    if os.path.exists(image_path):
        return Image.open(image_path)
    return None

@st.cache_data
def load_figure(name):
    """Load pre-generated figure"""
    path = f"assets/figures/{name}"
    if os.path.exists(path):
        return Image.open(path)
    return None

@st.cache_data
def load_dem():
    """Load DEM data"""
    path = "assets/large_dem.npy"
    if os.path.exists(path):
        return np.load(path)
    return None

@st.cache_data
def load_tensor():
    """Load tensor data"""
    path = "assets/large_basin_tensor.npy"
    if os.path.exists(path):
        return np.load(path)
    return None

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_basin_range(metadata):
    """Get range of basin IDs"""
    return list(range(metadata.get('basins', 71)))

def format_basin_name(basin_id):
    """Format basin name for display"""
    return f"Basin {basin_id:03d}"

# ============================================
# MAIN APPLICATION
# ============================================

# Load data
metadata = load_metadata()
dem = load_dem()
X = load_tensor()

# Initialize session state
if 'basin_id' not in st.session_state:
    st.session_state.basin_id = 0

# ============================================
# HEADER
# ============================================

st.markdown("""
<div class="header-container">
    <div class="header-title">🌊 HydroFoundation Basin Intelligence Explorer</div>
    <div class="header-subtitle">Interactive watershed digital twin — Select a basin to visualize environmental and AI insights</div>
</div>
""", unsafe_allow_html=True)

# ============================================
# BASIN SELECTOR
# ============================================

basin_range = get_basin_range(metadata)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    basin_id = st.selectbox(
        "Select Basin",
        options=basin_range,
        format_func=format_basin_name,
        index=st.session_state.basin_id,
        label_visibility="collapsed"
    )
    st.session_state.basin_id = basin_id

st.markdown("---")

# ============================================
# MAIN CONTENT
# ============================================

# Load basin image
basin_img = load_basin_image(basin_id)

# Load AI outputs (these are global for now, but in production would be basin-specific)
vuln_map = load_figure("watershed_vulnerability_map.png")
attn_map = load_figure("attention_map.png")
digital_twin = load_figure("basin_digital_twin.png")

# ============================================
# ROW 1: INPUT ENVIRONMENT
# ============================================

st.markdown('<div class="section-title">📍 Environmental Input</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    if basin_img:
        st.image(basin_img, use_container_width=True)
    else:
        st.warning(f"No image found for {format_basin_name(basin_id)}")

with col2:
    st.markdown("""
    <div class="info-panel">
        <div style="font-size: 0.85rem; font-weight: 600; color: #88c8e8; margin-bottom: 0.5rem;">Basin Information</div>
    """, unsafe_allow_html=True)
    
    # Display basin info
    st.markdown(f"""
    <div class="info-row">
        <span class="info-label">Basin ID</span>
        <span class="info-value">{basin_id:03d}</span>
    </div>
    <div class="info-row">
        <span class="info-label">Spatial Resolution</span>
        <span class="info-value">{metadata.get('height', 64)} × {metadata.get('width', 64)}</span>
    </div>
    <div class="info-row">
        <span class="info-label">Channels</span>
        <span class="info-value">{metadata.get('channels', 15)}</span>
    </div>
    <div class="info-row">
        <span class="info-label">Embedding Dim</span>
        <span class="info-value">128</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ============================================
# ROW 2: AI INTERPRETATION
# ============================================

st.markdown('<div class="section-title">🧠 AI Watershed Intelligence</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div style="font-size: 0.8rem; color: #a0aec0; text-align: center; margin-bottom: 0.3rem;">Vulnerability Map</div>', unsafe_allow_html=True)
    if vuln_map:
        st.image(vuln_map, use_container_width=True)
    else:
        st.info("Vulnerability map not available")

with col2:
    st.markdown('<div style="font-size: 0.8rem; color: #a0aec0; text-align: center; margin-bottom: 0.3rem;">Attention Map</div>', unsafe_allow_html=True)
    if attn_map:
        st.image(attn_map, use_container_width=True)
    else:
        st.info("Attention map not available")

st.markdown("---")

# ============================================
# ROW 3: DIGITAL TWIN
# ============================================

st.markdown('<div class="section-title">🛰 Environmental Digital Twin</div>', unsafe_allow_html=True)

if digital_twin:
    st.image(digital_twin, use_container_width=True)
else:
    st.info("Digital twin visualization not available")

# ============================================
# ROW 4: COMPARISON (Optional)
# ============================================

st.markdown("---")
st.markdown('<div class="section-title">📊 Input vs AI Interpretation</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div style="font-size: 0.8rem; color: #a0aec0; text-align: center; margin-bottom: 0.3rem;">Original Basin</div>', unsafe_allow_html=True)
    if basin_img:
        st.image(basin_img, use_container_width=True)

with col2:
    st.markdown('<div style="font-size: 0.8rem; color: #a0aec0; text-align: center; margin-bottom: 0.3rem;">AI Interpretation</div>', unsafe_allow_html=True)
    if vuln_map:
        st.image(vuln_map, use_container_width=True)
=======
        st.image(images['digital_twin'], use_container_width=True)
else:
    st.info("No digital twin available")

st.markdown('</div>', unsafe_allow_html=True)
>>>>>>> ddd9d7a55759e9ba4b3e233cf4248ba196bcc625

# ============================================
# FOOTER
# ============================================

<<<<<<< HEAD
st.markdown("""
<div class="footer">
    HydroFoundation v2.0 — PhD Research Prototype | Powered by BASINGRID Dataset
</div>
""", unsafe_allow_html=True)
>>>>>>> Stashed changes
=======
st.markdown(f"""
<div class="footer">
    Basin {basin_id:03d} of {total_basins} • Powered by HydroFoundation AI
</div>
""", unsafe_allow_html=True)
>>>>>>> ddd9d7a55759e9ba4b3e233cf4248ba196bcc625
