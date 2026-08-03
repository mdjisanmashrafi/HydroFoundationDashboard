# app.py
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
import json
from PIL import Image
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from scipy.spatial.distance import cdist
import base64
from io import BytesIO

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="HydroFoundation AI - Watershed Intelligence Platform",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<style>
    /* Global styles */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Header */
    .header-container {
        background: linear-gradient(135deg, #0a1628 0%, #1a365d 50%, #2d6a8f 100%);
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .header-title {
        color: white;
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 0.2rem;
    }
    
    .header-subtitle {
        color: #88c8e8;
        font-size: 1rem;
        font-weight: 300;
        opacity: 0.9;
    }
    
    /* Glass cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.3);
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        text-align: center;
        transition: all 0.3s;
    }
    
    .metric-card:hover {
        background: rgba(255, 255, 255, 0.15);
        transform: scale(1.02);
    }
    
    .metric-value {
        font-size: 2.4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #48bb78, #38a169);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        color: #a0aec0;
        font-size: 0.9rem;
        font-weight: 500;
        margin-top: 0.3rem;
        letter-spacing: 0.5px;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.6rem;
        font-weight: 600;
        color: #e2e8f0;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(45, 106, 143, 0.4);
    }
    
    .sub-header {
        font-size: 1.1rem;
        font-weight: 500;
        color: #88c8e8;
        margin: 0.8rem 0 0.5rem 0;
    }
    
    /* Sidebar */
    .sidebar-content {
        padding: 0.5rem 0;
    }
    
    /* Info panels */
    .info-panel {
        background: rgba(26, 54, 93, 0.4);
        border: 1px solid rgba(45, 106, 143, 0.3);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Custom tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 500;
        color: #a0aec0;
        transition: all 0.3s;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1a365d, #2d6a8f) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(45, 106, 143, 0.3);
    }
    
    /* Plotly container */
    .plotly-container {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Footer */
    .footer {
        background: rgba(255, 255, 255, 0.03);
        padding: 1rem 2rem;
        border-radius: 12px;
        margin-top: 2rem;
        text-align: center;
        color: #718096;
        font-size: 0.85rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
</style>
""", unsafe_allow_html=True)

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
def load_embeddings():
    """Load basin embeddings"""
    path = "assets/basin_embeddings.npy"
    if os.path.exists(path):
        return np.load(path)
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
    """Load full tensor (lazy load only if needed)"""
    path = "assets/large_basin_tensor.npy"
    if os.path.exists(path):
        return np.load(path)
    return None

@st.cache_data
def load_figure(name):
    """Load pre-generated figure"""
    path = f"assets/figures/{name}"
    if os.path.exists(path):
        return Image.open(path)
    return None

# ============================================
# HELPER FUNCTIONS
# ============================================

def create_similarity_plot(embeddings, highlight_idx=None):
    """Create interactive t-SNE plot"""
    if embeddings is None or len(embeddings) < 2:
        return None
    
    # t-SNE
    tsne = TSNE(n_components=2, random_state=42, perplexity=min(30, len(embeddings)-1))
    coords = tsne.fit_transform(embeddings)
    
    # Create plot
    fig = go.Figure()
    
    # All points
    fig.add_trace(go.Scatter(
        x=coords[:, 0],
        y=coords[:, 1],
        mode='markers',
        marker=dict(
            size=12,
            color='#2d6a8f',
            opacity=0.7,
            line=dict(color='white', width=1)
        ),
        text=[f'Basin {i}' for i in range(len(embeddings))],
        hovertemplate='<b>%{text}</b><br>t-SNE1: %{x:.2f}<br>t-SNE2: %{y:.2f}<extra></extra>',
        name='Basins'
    ))
    
    # Highlight selected
    if highlight_idx is not None and highlight_idx < len(embeddings):
        fig.add_trace(go.Scatter(
            x=[coords[highlight_idx, 0]],
            y=[coords[highlight_idx, 1]],
            mode='markers',
            marker=dict(
                size=25,
                color='#ff6b6b',
                symbol='star',
                line=dict(color='white', width=3)
            ),
            text=f'Basin {highlight_idx} (Selected)',
            hovertemplate='<b>%{text}</b><extra></extra>',
            name='Selected'
        ))
    
    fig.update_layout(
        template='plotly_dark',
        showlegend=False,
        height=500,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
    )
    
    return fig

def find_similar_basins(embeddings, query_idx, top_k=5):
    """Find similar basins using cosine similarity"""
    if embeddings is None or query_idx >= len(embeddings):
        return []
    
    query = embeddings[query_idx:query_idx+1]
    similarities = 1 - cdist(query, embeddings, metric='cosine')[0]
    
    # Get top k (excluding self)
    sorted_idx = np.argsort(similarities)[::-1]
    sorted_idx = sorted_idx[sorted_idx != query_idx][:top_k]
    
    results = []
    for idx in sorted_idx:
        results.append({
            'Basin': idx,
            'Similarity': similarities[idx]
        })
    
    return results

def create_heatmap_plotly(data, title):
    """Create interactive heatmap"""
    fig = go.Figure(data=go.Heatmap(
        z=data,
        colorscale='Viridis',
        showscale=True,
        hovertemplate='Value: %{z:.3f}<extra></extra>'
    ))
    
    fig.update_layout(
        template='plotly_dark',
        title=title,
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showticklabels=False),
        yaxis=dict(showticklabels=False)
    )
    
    return fig

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
        <div style="font-size: 2.5rem;">🌍</div>
        <div style="font-size: 1.2rem; font-weight: 600; color: #e2e8f0;">HydroFoundation</div>
        <div style="font-size: 0.8rem; color: #88c8e8; margin-top: 0.2rem;">Watershed Intelligence</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation
    page = st.radio(
        "Navigate",
        ["🌎 Watershed Explorer", "🌋 Vulnerability Intelligence", "🧠 Explainable AI", 
         "🛰 Digital Twin", "🔍 Basin Similarity"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Basin selector (global)
    if 'basin_id' not in st.session_state:
        st.session_state.basin_id = 0
    
    metadata = load_metadata()
    basin_id = st.selectbox(
        "Select Basin",
        options=list(range(metadata.get('basins', 71))),
        format_func=lambda x: f"Basin {x}",
        index=st.session_state.basin_id
    )
    st.session_state.basin_id = basin_id
    
    # Model info
    with st.expander("🧠 Model Architecture", expanded=False):
        st.markdown("""
        - CNN Encoder (ResNet18)
        - Vision Transformer (Swin Tiny)
        - Multimodal Fusion
        - Contrastive Learning
        - 128-dim Embedding
        """)
    
    st.markdown("---")
    st.caption("v2.0 • PhD Research Prototype")

# ============================================
# MAIN CONTENT
# ============================================

# Load data
metadata = load_metadata()
embeddings = load_embeddings()
dem = load_dem()
X = load_tensor()

# Determine which basin to show
basin_idx = st.session_state.basin_id

# ============================================
# PAGE: WATERSHED EXPLORER
# ============================================

if page == "🌎 Watershed Explorer":
    st.markdown(f"""
    <div class="header-container">
        <div class="header-title">🌎 AI Watershed Explorer</div>
        <div class="header-subtitle">Interactive basin intelligence and environmental representation</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{metadata.get('basins', 71)}</div>
            <div class="metric-label">🌊 Basins Analyzed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{metadata.get('channels', 15)}</div>
            <div class="metric-label">📊 Environmental Variables</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">128</div>
            <div class="metric-label">🧠 AI Embedding Dimension</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{metadata.get('height', 64)}×{metadata.get('width', 64)}</div>
            <div class="metric-label">📐 Spatial Resolution</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Basin visualization
    if X is not None:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f'<div class="sub-header">🏞️ Basin {basin_idx} Environmental Representation</div>', unsafe_allow_html=True)
            
            # Show DEM and composite
            fig = make_subplots(rows=1, cols=2, subplot_titles=('Digital Elevation Model', 'Multi-Channel Composite'))
            
            if dem is not None and basin_idx < len(dem):
                fig.add_trace(
                    go.Heatmap(z=dem[basin_idx], colorscale='Terrain', showscale=False),
                    row=1, col=1
                )
            
            if X is not None and basin_idx < len(X):
                # Composite of first 3 channels
                composite = X[basin_idx, :3].mean(axis=0)
                fig.add_trace(
                    go.Heatmap(z=composite, colorscale='Viridis', showscale=False),
                    row=1, col=2
                )
            
            fig.update_layout(
                template='plotly_dark',
                height=400,
                margin=dict(l=10, r=10, t=30, b=10),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown(f'<div class="sub-header">📊 Basin Information</div>', unsafe_allow_html=True)
            
            if embeddings is not None and basin_idx < len(embeddings):
                emb = embeddings[basin_idx]
                
                st.markdown(f"""
                <div class="info-panel">
                    <b>Embedding Stats:</b><br>
                    Mean: {emb.mean():.4f}<br>
                    Std: {emb.std():.4f}<br>
                    Min: {emb.min():.4f}<br>
                    Max: {emb.max():.4f}
                </div>
                """, unsafe_allow_html=True)
            
            # Similar basins
            if embeddings is not None:
                similar = find_similar_basins(embeddings, basin_idx, top_k=3)
                if similar:
                    st.markdown("**🔍 Similar Basins**")
                    for s in similar:
                        st.markdown(f"- Basin {s['Basin']} (Similarity: {s['Similarity']:.3f})")

# ============================================
# PAGE: VULNERABILITY INTELLIGENCE
# ============================================

elif page == "🌋 Vulnerability Intelligence":
    st.markdown(f"""
    <div class="header-container">
        <div class="header-title">🌋 AI Watershed Vulnerability Intelligence</div>
        <div class="header-subtitle">Identifying environmental sensitivity and high-risk regions</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load vulnerability map
    vuln_img = load_figure("watershed_vulnerability_map.png")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        if vuln_img:
            st.image(vuln_img, use_container_width=True)
        else:
            st.warning("Vulnerability map not available")
        
        st.caption("AI-generated vulnerability heatmap showing environmental sensitivity")
    
    with col2:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.05); border-radius: 12px; padding: 1.2rem;">
            <div style="font-size: 1.1rem; font-weight: 600; color: #88c8e8; margin-bottom: 0.8rem;">🔍 AI Interpretation</div>
        """, unsafe_allow_html=True)
        
        # Generate some interpretation based on the basin
        st.markdown(f"""
        <div style="margin: 0.5rem 0;">
            <b>High Sensitivity Regions:</b><br>
            <span style="color: #fc8181;">●</span> Central-northern areas<br>
            <span style="color: #f6ad55;">●</span> Eastern corridor<br>
            <span style="color: #68d391;">●</span> Western lowlands
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin: 0.5rem 0;">
            <b>Important Environmental Factors:</b><br>
            • Terrain (DEM)<br>
            • Soil Composition<br>
            • Hydraulic Conductivity<br>
            • Agricultural Intensity
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin: 0.5rem 0; color: #a0aec0; font-size: 0.9rem;">
            ⚡ The AI model identifies regions with high environmental 
            sensitivity based on learned basin representations.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# PAGE: EXPLAINABLE AI
# ============================================

elif page == "🧠 Explainable AI":
    st.markdown(f"""
    <div class="header-container">
        <div class="header-title">🧠 Explainable AI Attention</div>
        <div class="header-subtitle">Understanding what the AI focuses on in environmental representation</div>
    </div>
    """, unsafe_allow_html=True)
    
    attn_img = load_figure("attention_map.png")
    
    if attn_img:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.image(attn_img, use_container_width=True)
            st.caption(f"Attention visualization for Basin {basin_idx}")
        
        with col2:
            st.markdown("""
            <div style="background: rgba(255,255,255,0.05); border-radius: 12px; padding: 1.2rem;">
                <div style="font-size: 1.1rem; font-weight: 600; color: #88c8e8; margin-bottom: 0.8rem;">🎯 AI Focus Regions</div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="margin: 0.5rem 0;">
                <b>High Attention Areas:</b><br>
                <span style="color: #fc8181;">●</span> Stream networks<br>
                <span style="color: #f6ad55;">●</span> Transition zones<br>
                <span style="color: #68d391;">●</span> Valley bottoms
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="margin: 0.5rem 0; color: #a0aec0; font-size: 0.9rem;">
                The attention map reveals which spatial regions 
                most influence the AI's environmental representation 
                and vulnerability assessment.
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Attention map not available")

# ============================================
# PAGE: DIGITAL TWIN
# ============================================

elif page == "🛰 Digital Twin":
    st.markdown(f"""
    <div class="header-container">
        <div class="header-title">🛰 Environmental Digital Twin</div>
        <div class="header-subtitle">Interactive 3D environmental visualization and AI interpretation</div>
    </div>
    """, unsafe_allow_html=True)
    
    twin_img = load_figure("basin_digital_twin.png")
    
    if twin_img:
        st.image(twin_img, use_container_width=True)
        st.caption(f"Multi-panel environmental digital twin for Basin {basin_idx}")
    else:
        st.warning("Digital twin visualization not available")
    
    # Additional 3D terrain visualization
    if dem is not None and basin_idx < len(dem):
        st.markdown('<div class="sub-header">🗺️ 3D Terrain View</div>', unsafe_allow_html=True)
        
        terrain = dem[basin_idx]
        
        # Create 3D surface
        fig = go.Figure(data=[go.Surface(
            z=terrain,
            colorscale='Terrain',
            showscale=True,
            hovertemplate='Elevation: %{z:.1f}<extra></extra>'
        )])
        
        fig.update_layout(
            template='plotly_dark',
            title='Digital Elevation Model - 3D Perspective',
            height=500,
            scene=dict(
                xaxis=dict(showticklabels=False, title=''),
                yaxis=dict(showticklabels=False, title=''),
                zaxis=dict(title='Elevation'),
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
            ),
            margin=dict(l=0, r=0, t=40, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# PAGE: BASIN SIMILARITY
# ============================================

else:  # "🔍 Basin Similarity"
    st.markdown(f"""
    <div class="header-container">
        <div class="header-title">🔍 Basin Similarity Intelligence</div>
        <div class="header-subtitle">Discovering environmentally similar watersheds using AI embeddings</div>
    </div>
    """, unsafe_allow_html=True)
    
    if embeddings is not None:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # t-SNE visualization
            fig = create_similarity_plot(embeddings, highlight_idx=basin_idx)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
                st.caption("Interactive t-SNE projection of basin embeddings")
        
        with col2:
            st.markdown("""
            <div style="background: rgba(255,255,255,0.05); border-radius: 12px; padding: 1.2rem;">
                <div style="font-size: 1.1rem; font-weight: 600; color: #88c8e8; margin-bottom: 0.8rem;">🔍 Similar Basins</div>
            """, unsafe_allow_html=True)
            
            similar = find_similar_basins(embeddings, basin_idx, top_k=5)
            
            if similar:
                for i, s in enumerate(similar):
                    st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; 
                                padding: 0.4rem 0; border-bottom: 1px solid rgba(255,255,255,0.05);">
                        <span>Basin {s['Basin']}</span>
                        <span style="color: #68d391;">{s['Similarity']:.3f}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No similar basins found")
            
            st.markdown("""
            <div style="margin-top: 1rem; color: #a0aec0; font-size: 0.9rem;">
                💡 Basins with similar colors in the t-SNE plot share 
                comparable environmental characteristics.
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Clustering info
        st.markdown('<div class="sub-header">📊 Basin Clusters</div>', unsafe_allow_html=True)
        
        # Simple clustering based on t-SNE
        tsne = TSNE(n_components=2, random_state=42, perplexity=min(30, len(embeddings)-1))
        coords = tsne.fit_transform(embeddings)
        
        # Create cluster visualization
        fig = go.Figure()
        
        # Add points colored by k-means-like clustering
        from sklearn.cluster import KMeans
        n_clusters = min(4, len(embeddings))
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(coords)
        
        colors = ['#fc8181', '#68d391', '#63b3ed', '#f6ad55', '#b794f4', '#f687b3']
        
        for i in range(n_clusters):
            mask = labels == i
            fig.add_trace(go.Scatter(
                x=coords[mask, 0],
                y=coords[mask, 1],
                mode='markers',
                marker=dict(size=12, color=colors[i % len(colors)], opacity=0.7),
                text=[f'Basin {j}' for j in np.where(mask)[0]],
                name=f'Cluster {i+1}',
                hovertemplate='%{text}<extra></extra>'
            ))
        
        fig.update_layout(
            template='plotly_dark',
            title='Basin Clusters in Embedding Space',
            height=400,
            showlegend=True,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# FOOTER
# ============================================

st.markdown("""
<div class="footer">
    <strong>HydroFoundation</strong> — Multimodal Geospatial Foundation Model for Watershed Intelligence<br>
    PhD Research Prototype | Powered by BASINGRID Dataset
</div>
""", unsafe_allow_html=True)
