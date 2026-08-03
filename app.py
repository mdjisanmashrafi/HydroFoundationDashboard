# app.py
import streamlit as st
from PIL import Image
import os
import json
import time

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="HydroFoundation Basin Explorer",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# LOAD CUSTOM CSS
# ============================================

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
        st.image(images['digital_twin'], use_container_width=True)
else:
    st.info("No digital twin available")

st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================

st.markdown(f"""
<div class="footer">
    Basin {basin_id:03d} of {total_basins} • Powered by HydroFoundation AI
</div>
""", unsafe_allow_html=True)
