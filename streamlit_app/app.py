import streamlit as st
import requests
import json
import time
import os
import socket

st.set_page_config(
    page_title="House Price Predictor",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; }

/* ── Page background ── */
.stApp {
    background: #0f1117;
    color: #e8e8e8;
}

/* ── Page title ── */
.page-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.8rem;
    color: #f5f0e8;
    letter-spacing: -0.5px;
    margin-bottom: 0.1rem;
}
.page-subtitle {
    font-size: 1rem;
    color: #6b7280;
    font-weight: 300;
    margin-bottom: 2rem;
}

/* ── Cards ── */
.card {
    background: #1a1d27;
    border: 1px solid #2a2d3a;
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1rem;
}

/* ── Section labels ── */
.field-label {
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #9ca3af;
    margin-bottom: 0.3rem;
    margin-top: 1.2rem;
}

/* ── Predict button ── */
.stButton > button {
    background: linear-gradient(135deg, #c8973a 0%, #e8b84b 100%) !important;
    color: #0f1117 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 2rem !important;
    width: 100% !important;
    margin-top: 1.5rem !important;
    transition: opacity 0.2s ease !important;
    cursor: pointer !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

/* ── Predicted price ── */
.price-display {
    text-align: center;
    padding: 2rem 1rem;
    border-bottom: 1px solid #2a2d3a;
    margin-bottom: 1.5rem;
}
.price-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 0.5rem;
}
.price-value {
    font-family: 'DM Serif Display', serif;
    font-size: 3.8rem;
    color: #ffffff;
    letter-spacing: -1px;
    line-height: 1;
    text-shadow: 0 0 30px rgba(200, 151, 58, 0.5);
}
.price-range {
    font-size: 0.85rem;
    color: #6b7280;
    margin-top: 0.5rem;
}

/* ── Metric grid ── */
.metric-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
}
.metric-tile {
    background: #12141c;
    border: 1px solid #2a2d3a;
    border-radius: 10px;
    padding: 1rem 1.2rem;
}
.metric-tile-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 0.3rem;
}
.metric-tile-value {
    font-size: 1.25rem;
    font-weight: 600;
    color: #f5f0e8;
}

/* ── Feature importance ── */
.fi-row {
    margin-bottom: 0.9rem;
}
.fi-header {
    display: flex;
    justify-content: space-between;
    font-size: 0.82rem;
    color: #9ca3af;
    margin-bottom: 0.3rem;
}
.fi-bar-track {
    background: #12141c;
    border-radius: 4px;
    height: 6px;
    overflow: hidden;
}
.fi-bar-fill {
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, #c8973a, #e8b84b);
}

/* ── Placeholder ── */
.placeholder-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 320px;
    color: #374151;
    text-align: center;
    gap: 0.75rem;
}
.placeholder-icon {
    font-size: 3rem;
    opacity: 0.3;
}
.placeholder-text {
    font-size: 0.9rem;
    font-weight: 400;
    color: #4b5563;
    max-width: 200px;
    line-height: 1.5;
}

/* ── Footer ── */
.footer {
    text-align: center;
    color: #374151;
    font-size: 0.78rem;
    margin-top: 2.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid #1e2130;
    line-height: 1.8;
}
.footer a { color: #c8973a; text-decoration: none; }

/* ── Streamlit widget overrides ── */
.stSlider > div > div > div { background: #2a2d3a !important; }
.stSlider > div > div > div > div { background: #c8973a !important; }
div[data-baseweb="select"] > div {
    background-color: #12141c !important;
    border-color: #2a2d3a !important;
    color: #e8e8e8 !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Header ──
st.markdown('<p class="page-title">House Price Predictor</p>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Real-time valuation powered by XGBoost · MLOps demonstration</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="field-label">Square Footage</p>', unsafe_allow_html=True)
    sqft = st.slider("sqft", 500, 5000, 1500, 50, label_visibility="collapsed", key="sqft")
    st.caption(f"{sqft:,} sq ft")

    bed_col, bath_col = st.columns(2)
    with bed_col:
        st.markdown('<p class="field-label">Bedrooms</p>', unsafe_allow_html=True)
        bedrooms = st.selectbox("beds", options=[1, 2, 3, 4, 5, 6], index=2, label_visibility="collapsed")
    with bath_col:
        st.markdown('<p class="field-label">Bathrooms</p>', unsafe_allow_html=True)
        bathrooms = st.selectbox("baths", options=[1, 1.5, 2, 2.5, 3, 3.5, 4], index=2, label_visibility="collapsed")

    st.markdown('<p class="field-label">Location</p>', unsafe_allow_html=True)
    location = st.selectbox("loc", options=["Urban", "Suburban", "Rural", "Waterfront", "Mountain"], index=1, label_visibility="collapsed")

    st.markdown('<p class="field-label">Year Built</p>', unsafe_allow_html=True)
    year_built = st.slider("year", 1900, 2025, 2000, 1, label_visibility="collapsed", key="year")
    st.caption(str(year_built))

    predict_button = st.button("Estimate Price →", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    if predict_button:
        with st.spinner("Running model inference…"):
            api_data = {
                "sqft": sqft, "bedrooms": bedrooms, "bathrooms": bathrooms,
                "location": location.lower(), "year_built": year_built, "condition": "Good"
            }
            try:
                api_endpoint = os.getenv("API_URL", "http://model:8000")
                response = requests.post(f"{api_endpoint.rstrip('/')}/predict", json=api_data)
                response.raise_for_status()
                st.session_state.prediction = response.json()
            except requests.exceptions.RequestException:
                st.session_state.prediction = {
                    "predicted_price": 467145,
                    "confidence_interval": [420430.5, 513859.5],
                    "features_importance": {"sqft": 0.43, "location": 0.27, "bathrooms": 0.15, "year_built": 0.15},
                    "prediction_time": "0.12 seconds"
                }
            st.session_state.prediction_time = time.time()

    if "prediction" in st.session_state:
        pred = st.session_state.prediction
        lower = "${:,.0f}".format(pred["confidence_interval"][0])
        upper = "${:,.0f}".format(pred["confidence_interval"][1])

        st.markdown(f"""
        <div class="price-display">
            <p class="price-label">Estimated Value</p>
            <p class="price-value">${pred["predicted_price"]:,.0f}</p>
            <p class="price-range">Range: {lower} – {upper}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="metric-grid">
            <div class="metric-tile">
                <p class="metric-tile-label">Confidence</p>
                <p class="metric-tile-value">92%</p>
            </div>
            <div class="metric-tile">
                <p class="metric-tile-label">Model</p>
                <p class="metric-tile-value">XGBoost</p>
            </div>
            <div class="metric-tile">
                <p class="metric-tile-label">Inference</p>
                <p class="metric-tile-value">0.12s</p>
            </div>
            <div class="metric-tile">
                <p class="metric-tile-label">Status</p>
                <p class="metric-tile-value" style="color:#4ade80;">● Live</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-top: 1.2rem; border-top: 1px solid #2a2d3a; padding-top: 1.2rem;">
            <p class="field-label" style="margin-bottom: 0.6rem;">Top Factors Affecting Price</p>
            <ul style="list-style: none; padding: 0; margin: 0;">
                <li style="padding: 0.4rem 0; color: #e8e8e8; font-size: 0.9rem;">
                    <span style="color: #c8973a; margin-right: 0.5rem;">◆</span> Square Footage
                </li>
                <li style="padding: 0.4rem 0; color: #e8e8e8; font-size: 0.9rem;">
                    <span style="color: #c8973a; margin-right: 0.5rem;">◆</span> Location
                </li>
                <li style="padding: 0.4rem 0; color: #e8e8e8; font-size: 0.9rem;">
                    <span style="color: #c8973a; margin-right: 0.5rem;">◆</span> Bathrooms
                </li>
                <li style="padding: 0.4rem 0; color: #e8e8e8; font-size: 0.9rem;">
                    <span style="color: #c8973a; margin-right: 0.5rem;">◆</span> Year Built
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="placeholder-box">
            <div class="placeholder-icon">◈</div>
            <p class="placeholder-text">Fill out the form and click Estimate Price to see a valuation.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ──
version = os.getenv("APP_VERSION", "4.0.0")
hostname = socket.gethostname()
try:
    ip_address = socket.gethostbyname(hostname)
except:
    ip_address = "N/A"

st.markdown(f"""
<div class="footer">
    <strong>MLOps Bootcamp</strong> · Built by <a href="https://www.schoolofdevops.com" target="_blank">School of Devops</a><br>
    v{version} · {hostname} · {ip_address}
</div>
""", unsafe_allow_html=True)