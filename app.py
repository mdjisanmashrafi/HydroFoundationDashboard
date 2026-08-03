import streamlit as st
import os
import base64
import time

# 1. Page Configuration (Must be the first command)
st.set_page_config(
    page_title="HydroFoundation Basin Explorer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Load Custom CSS
def load_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("style.css")

# 3. Setup Paths and Data
BASE_DIR = os.path.join("HydroFoundation_Output", "basin_outputs")
BASINS = [f"basin_{str(i).zfill(3)}" for i in range(1, 72)]

# 4. Lazy-loading Base64 Image Converter with Caching
@st.cache_data(show_spinner=False)
def get_image_base64(basin_name, image_name):
    img_path = os.path.join(BASE_DIR, basin_name, image_name)
    if not os.path.exists(img_path):
        return None
    
    with open(img_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string

# 5. UI: Header and Selector
st.markdown("<h1 class='main-title'>HydroFoundation Basin Explorer</h1>", unsafe_allow_html=True)

# Selectbox natively supports searching
selected_basin = st.selectbox(
    "Select Basin", 
    options=BASINS, 
    format_func=lambda x: x.replace("_", " ").title()
)

st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

# 6. Render Helper Function
def render_card(title, base64_str, width_class):
    if base64_str:
        html = f"""
        <div class="card-container">
            <div class="img-card {width_class}">
                <div class="card-title">{title}</div>
                <div class="img-wrapper">
                    <img src="data:image/png;base64,{base64_str}" alt="{title}"/>
                </div>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.error(f"Image not found: {title}")

# 7. Dashboard Layout Engine
with st.spinner("Loading basin data..."):
    # Brief pause to ensure the UI spinner renders smoothly during transitions
    time.sleep(0.2)
    
    # Load assets just-in-time
    img_input = get_image_base64(selected_basin, "input.png")
    img_att = get_image_base64(selected_basin, "attention_map.png")
    img_vuln = get_image_base64(selected_basin, "vulnerability_map.png")
    img_dt = get_image_base64(selected_basin, "digital_twin.png")
    
    # --- ROW 1: Input Image (~75% width, centered) ---
    render_card("Input Basin", img_input, "width-80")
    
    # --- ROW 2: Attention & Vulnerability Maps (Side-by-side, equal width) ---
    # We use Streamlit columns here to handle side-by-side spacing responsively
    col1, col2 = st.columns(2)
    with col1:
        render_card("Attention Map", img_att, "width-100")
    with col2:
        render_card("Vulnerability Map", img_vuln, "width-100")
        
    # --- ROW 3: Digital Twin (~70% width, centered) ---
    render_card("Digital Twin", img_dt, "width-70")
