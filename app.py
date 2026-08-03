/* style.css */

/* ============================================
   GLOBAL STYLES
   ============================================ */

[data-testid="stAppViewContainer"] {
    background: #0a0e1a;
}

[data-testid="stSidebar"] {
    background: rgba(10, 14, 26, 0.95);
    border-right: 1px solid rgba(255, 255, 255, 0.05);
    padding: 1rem 0;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 0;
}

/* ============================================
   SIDEBAR STYLES
   ============================================ */

.sidebar-header {
    text-align: center;
    padding: 0.5rem 1rem 1rem 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.sidebar-logo {
    font-size: 2.5rem;
    margin-bottom: 0.3rem;
}

.sidebar-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: #e2e8f0;
    letter-spacing: -0.5px;
}

.sidebar-subtitle {
    font-size: 0.75rem;
    color: #88c8e8;
    opacity: 0.7;
    font-weight: 300;
}

.sidebar-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #718096;
    margin-bottom: 0.5rem;
    font-weight: 500;
}

.sidebar-footer {
    padding: 1rem 0 0 0;
    text-align: center;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.footer-text {
    color: #4a5568;
    font-size: 0.75rem;
}

/* ============================================
   STATS CONTAINER
   ============================================ */

.stats-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
    padding: 0.5rem 0;
}

.stat-item {
    text-align: center;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 8px;
    padding: 0.5rem;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.stat-value {
    font-size: 1.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #48bb78, #38a169);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.stat-label {
    font-size: 0.6rem;
    color: #718096;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 0.2rem;
}

/* ============================================
   MAIN HEADER
   ============================================ */

.main-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0 1.5rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    margin-bottom: 1.5rem;
}

.header-title {
    font-size: 2rem;
    font-weight: 700;
    color: #e2e8f0;
    letter-spacing: -0.5px;
}

.header-subtitle {
    font-size: 0.85rem;
    color: #a0aec0;
    font-weight: 300;
    margin-top: 0.2rem;
}

.header-badge {
    display: flex;
    gap: 0.5rem;
}

.badge {
    background: rgba(45, 106, 143, 0.3);
    color: #88c8e8;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 500;
    border: 1px solid rgba(45, 106, 143, 0.3);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ============================================
   AI SUMMARY CARD
   ============================================ */

.ai-summary-card {
    background: linear-gradient(135deg, rgba(26, 54, 93, 0.4), rgba(15, 76, 117, 0.2));
    border: 1px solid rgba(45, 106, 143, 0.2);
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(10px);
}

.summary-title {
    font-size: 0.9rem;
    font-weight: 600;
    color: #88c8e8;
    margin-bottom: 0.8rem;
    letter-spacing: 0.5px;
}

.summary-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
}

.summary-item {
    text-align: center;
}

.summary-icon {
    font-size: 1.5rem;
    margin-bottom: 0.2rem;
}

.summary-label {
    font-size: 0.65rem;
    color: #718096;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.summary-value {
    font-size: 1rem;
    font-weight: 600;
    margin-top: 0.2rem;
}

/* ============================================
   GALLERY
   ============================================ */

.gallery-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #e2e8f0;
    margin: 1.5rem 0 1rem 0;
}

/* ============================================
   TABS
   ============================================ */

[data-testid="stTabs"] {
    margin-bottom: 1rem;
}

[data-testid="stTabs"] > div > div {
    gap: 0.5rem;
}

[data-testid="stTabs"] button {
    background: rgba(255, 255, 255, 0.03) !important;
    border-radius: 10px !important;
    padding: 0.5rem 1.2rem !important;
    color: #a0aec0 !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    transition: all 0.3s !important;
}

[data-testid="stTabs"] button:hover {
    background: rgba(45, 106, 143, 0.2) !important;
    border-color: rgba(45, 106, 143, 0.3) !important;
}

[data-testid="stTabs"] button[aria-selected="true"] {
    background: linear-gradient(135deg, rgba(26, 54, 93, 0.6), rgba(15, 76, 117, 0.4)) !important;
    color: #e2e8f0 !important;
    border-color: rgba(45, 106, 143, 0.4) !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
}

/* ============================================
   IMAGE CONTAINERS
   ============================================ */

[data-testid="stImage"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.05);
    background: rgba(0, 0, 0, 0.2);
}

[data-testid="stImage"] img {
    width: 100%;
    height: auto;
}

/* ============================================
   COMPARISON VIEW
   ============================================ */

.comparison-label {
    font-size: 0.85rem;
    font-weight: 500;
    color: #a0aec0;
    margin-bottom: 0.5rem;
    text-align: center;
}

/* ============================================
   MAP
   ============================================ */

[data-testid="stMap"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

/* ============================================
   FOOTER
   ============================================ */

.footer {
    margin-top: 2rem;
    padding: 1rem;
    text-align: center;
    color: #4a5568;
    font-size: 0.75rem;
    border-top: 1px solid rgba(255, 255, 255, 0.03);
}

.footer span {
    margin: 0 0.3rem;
}

/* ============================================
   STREAMLIT OVERRIDES
   ============================================ */

/* Hide default Streamlit elements */
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

/* ============================================
   RESPONSIVE DESIGN
   ============================================ */

@media (max-width: 768px) {
    .summary-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .main-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
    }
    
    .header-title {
        font-size: 1.5rem;
    }
}
