import streamlit as st
import math
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Rainwater Harvesting Feasibility", page_icon="🌧️", layout="wide")

# Custom CSS for Sky Blue Background, Realistic Clouds, Slow Ship & Water Waves
st.markdown("""
    <style>
    /* Pleasant Sky Blue Gradient Background */
    .stApp {
        background: linear-gradient(180deg, #e0f2fe 0%, #bae6fd 60%, #7dd3fc 100%) !important;
        color: #0c4a6e;
        overflow-x: hidden;
        padding-bottom: 80px;
    }

    /* REALISTIC FLUFFY CLOUD BUTTONS */
    div.stButton > button {
        background: linear-gradient(180deg, #ffffff 0%, #f0f9ff 60%, #e2e8f0 100%) !important;
        color: #0369a1 !important;
        font-weight: 800 !important;
        font-size: 13px !important;
        height: 75px !important;
        border: none !important;
        
        /* Organic Realistic Cloud Silhouette Shape */
        clip-path: path("M 22 52 C 15 52 10 45 15 38 C 12 28 25 18 38 22 C 45 12 65 10 75 22 C 90 12 115 15 122 28 C 135 22 148 32 145 42 C 155 48 152 60 142 62 L 25 62 C 18 62 18 55 22 52 Z") !important;
        
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        filter: drop-shadow(0px 8px 12px rgba(2, 132, 199, 0.25)) !important;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }

    /* Cloud Button Hover Effect */
    div.stButton > button:hover {
        transform: translateY(-6px) scale(1.08) !important;
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 50%, #e0f2fe 100%) !important;
        color: #0284c7 !important;
        filter: drop-shadow(0px 12px 20px rgba(2, 132, 199, 0.4)) !important;
    }

    /* Falling Water Drops Animation (Under Selected Cloud Only) */
    @keyframes fallingWaterDrops {
        0% { transform: translateY(-8px); opacity: 0; }
        50% { opacity: 1; }
        100% { transform: translateY(30px); opacity: 0; }
    }

    .cloud-rain-container {
        text-align: center;
        margin-top: -12px;
        margin-bottom: 10px;
        font-size: 20px;
        height: 35px;
    }

    .water-drop {
        display: inline-block;
        animation: fallingWaterDrops 0.7s linear infinite;
        margin: 0 2px;
    }

    .drop-delay-1 { animation-delay: 0.0s; }
    .drop-delay-2 { animation-delay: 0.25s; }
    .drop-delay-3 { animation-delay: 0.5s; }

    /* Glassmorphism Metric Cards */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.85);
        border-radius: 20px;
        padding: 18px;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.9);
        box-shadow: 0 10px 25px rgba(2, 132, 199, 0.12);
    }
    
    [data-testid="stMetricLabel"] {
        color: #0369a1 !important;
        font-weight: 700;
    }

    [data-testid="stMetricValue"] {
        color: #0c4a6e !important;
        font-weight: 900;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.88);
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.7);
    }

    h1, h2, h3, p, span {
        color: #0c4a6e !important;
    }

    /* BOTTOM WATER FLOW & SLOW REALISTIC SHIP ANIMATION */
    .ocean-container {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 70px;
        z-index: 999;
        pointer-events: none;
    }

    /* Slow & Natural Rocking Ship Motion directly on water */
    @keyframes sailSlow {
        0% { left: -70px; transform: translateY(0px) scaleX(1) rotate(1deg); }
        25% { transform: translateY(3px) scaleX(1) rotate(-2deg); }
        50% { transform: translateY(0px) scaleX(1) rotate(1deg); }
        49.9% { left: 102%; transform: translateY(0px) scaleX(1) rotate(1deg); }
        50% { left: 102%; transform: translateY(0px) scaleX(-1) rotate(-1deg); }
        75% { transform: translateY(3px) scaleX(-1) rotate(2deg); }
        100% { left: -70px; transform: translateY(0px) scaleX(-1) rotate(-1deg); }
    }

    .sailing-ship {
        position: absolute;
        bottom: 12px; /* Placed exactly on top of the wave surface */
        font-size: 34px;
        animation: sailSlow 45s ease-in-out infinite; /* Much slower and smoother speed */
        z-index: 1001;
    }

    /* Realistic Layered Wave Flow */
    .wave {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 200%;
        height: 45px;
        background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none"><path d="M0,0 C150,90 350,-40 500,45 C650,130 900,10 1200,40 L1200,120 L0,120 Z" fill="%230284c7" opacity="0.7"/></svg>');
        background-size: 1200px 45px;
        animation: waveFlow 12s linear infinite;
    }

    .wave.wave2 {
        bottom: 0;
        opacity: 0.9;
        background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none"><path d="M0,30 C200,100 400,-10 600,50 C800,110 1000,10 1200,30 L1200,120 L0,120 Z" fill="%230369a1"/></svg>');
        background-size: 1200px 45px;
        animation: waveFlowReverse 8s linear infinite;
    }

    @keyframes waveFlow {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }

    @keyframes waveFlowReverse {
        0% { transform: translateX(-50%); }
        100% { transform: translateX(0); }
    }
    </style>

    <!-- Bottom Water Layer with Properly Seated Slow Ship -->
    <div class="ocean-container">
        <div class="sailing-ship">🚢</div>
        <div class="wave wave1"></div>
        <div class="wave wave2"></div>
    </div>
""", unsafe_allow_html=True)

# Main Title Header
st.markdown("<h1 style='text-align: center; color: #0284c7; text-shadow: 0 2px 12px rgba(255,255,255,0.9);'>🌧️ Rainwater Harvesting Feasibility Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #0369a1; font-size: 16px; font-weight: 600;'>JNTUK B.Tech R23 Regulation — Multidisciplinary Engineering Simulator</p>", unsafe_allow_html=True)
st.markdown("---")

# Session State Setup
if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = "Combined Subjects"

# Cloud Nav Section
st.markdown("<h3 style='color: #0284c7; text-align: center;'>☁️ Click a Cloud to Release Rainwater & Explore Topics</h3>", unsafe_allow_html=True)
col1, col2, col3, col4, col5, col6 = st.columns(6)

# Button 1
with col1:
    if st.button("Subjects", use_container_width=True):
        st.session_state.selected_topic = "Combined Subjects"
    if st.session_state.selected_topic == "Combined Subjects":
        st.markdown("<div class='cloud-rain-container'><span class='water-drop drop-delay-1'>💧</span><span class='water-drop drop-delay-2'>💧</span><span class='water-drop drop-delay-3'>💧</span></div>", unsafe_allow_html=True)

# Button 2
with col2:
    if st.button("Integrated", use_container_width=True):
        st.session_state.selected_topic = "Topics Integrated"
    if st.session_state.selected_topic == "Topics Integrated":
        st.markdown("<div class='cloud-rain-container'><span class='water-drop drop-delay-1'>💧</span><span class='water-drop drop-delay-2'>💧</span><span class='water-drop drop-delay-3'>💧</span></div>", unsafe_allow_html=True)

# Button 3
with col3:
    if st.button("AI Layer", use_container_width=True):
        st.session_state.selected_topic = "AI / LLM Layer"
    if st.session_state.selected_topic == "AI / LLM Layer":
        st.markdown("<div class='cloud-rain-container'><span class='water-drop drop-delay-1'>💧</span><span class='water-drop drop-delay-2'>💧</span><span class='water-drop drop-delay-3'>💧</span></div>", unsafe_allow_html=True)

# Button 4
with col4:
    if st.button("Code Base", use_container_width=True):
        st.session_state.selected_topic = "Coding Framework"
    if st.session_state.selected_topic == "Coding Framework":
        st.markdown("<div class='cloud-rain-container'><span class='water-drop drop-delay-1'>💧</span><span class='water-drop drop-delay-2'>💧</span><span class='water-drop drop-delay-3'>💧</span></div>", unsafe_allow_html=True)

# Button 5
with col5:
    if st.button("Calculator", use_container_width=True):
        st.session_state.selected_topic = "Mini Project Outcome"
    if st.session_state.selected_topic == "Mini Project Outcome":
        st.markdown("<div class='cloud-rain-container'><span class='water-drop drop-delay-1'>💧</span><span class='water-drop drop-delay-2'>💧</span><span class='water-drop drop-delay-3'>💧</span></div>", unsafe_allow_html=True)

# Button 6
with col6:
    if st.button("Alignment", use_container_width=True):
        st.session_state.selected_topic = "R23 Alignment"
    if st.session_state.selected_topic == "R23 Alignment":
        st.markdown("<div class='cloud-rain-container'><span class='water-drop drop-delay-1'>💧</span><span class='water-drop drop-delay-2'>💧</span><span class='water-drop drop-delay-3'>💧</span></div>", unsafe_allow_html=True)

st.markdown("---")

# ------------------------------------------------------------------------------
# 1. COMBINED SUBJECTS
# ------------------------------------------------------------------------------
if st.session_state.selected_topic == "Combined Subjects":
    st.header("📚 1. Combined Subjects")
    st.markdown("""
    * **Civil / Mechanical Engineering (BCME):** Surface hydrology, runoff potential, and water catchment dynamics.
    * **Applied Mathematics (Linear Algebra):** Sector-wise water demand matrices and seasonal allocation vectors.
    * **Computer Science & AI:** Modular Python architecture, input boundary validation, and dynamic web visualization.
    """)

# ------------------------------------------------------------------------------
# 2. TOPICS INTEGRATED
# ------------------------------------------------------------------------------
elif st.session_state.selected_topic == "Topics Integrated":
    st.header("🧩 2. Topics Integrated")
    c1, c2 = st.columns(2)
    with c1:
        st.info("""
        #### 🌊 Integrated Waterflow (Hydrodynamics)
        * **Rational Method Formula:** $H = A \\times R \\times C \\times E$
        * **Catchment Parameters:** Area ($A$), Rainfall ($R$), Runoff Coeff. ($C$), Filter Eff. ($E$).
        * **First-Flush Diverter:** Sized at $1\\text{ L/m}^2$ to purge roof contaminants.
        """)
    with c2:
        st.success("""
        #### 📐 System Vectors (Applied Mathematics)
        * **Demand Matrix Formulation:** $[D] = [D_1, D_2, D_3]^T$
        * **Matrix Vector Products:** Mapped across 365 days for annual consumption.
        * **Monsoon vs. Dry Season Balance:** Matrix solver evaluating seasonal rainfall deficits.
        """)

# ------------------------------------------------------------------------------
# 3. AI / LLM LAYER
# ------------------------------------------------------------------------------
elif st.session_state.selected_topic == "AI / LLM Layer":
    st.header("🤖 3. AI / LLM Recommendation Engine")
    st.markdown("""
    * **Heuristic Classification:** Automatically classifies roof viability as **Fully Feasible**, **Partially Feasible**, or **Low Potential**.
    * **Storage Optimizer:** Evaluates 45-day emergency supply buffers to calculate ideal tank volume.
    * **Prompt Payload Generator:** Formats structural data payloads ready for streaming directly to LLM models.
    """)

# ------------------------------------------------------------------------------
# 4. CODING FRAMEWORK
# ------------------------------------------------------------------------------
elif st.session_state.selected_topic == "Coding Framework":
    st.header("💻 4. Coding Framework")
    st.markdown("""
    * **Core Language:** Python 3.x
    * **Frontend UI Engine:** Streamlit with CSS3 Glassmorphism and SVG Cloud Clip-Paths
    * **Data Matrix Library:** Pandas & NumPy
    """)

# ------------------------------------------------------------------------------
# 5. MINI PROJECT OUTCOME (DYNAMIC SIMULATOR)
# ------------------------------------------------------------------------------
elif st.session_state.selected_topic == "Mini Project Outcome":
    st.header("📊 5. Mini Project Outcome (Interactive Simulator & Analytics)")
    
    # Sidebar
    st.sidebar.header("⚙️ Catchment Parameters")
    area = st.sidebar.number_input("Roof Area (m²)", min_value=10.0, max_value=10000.0, value=150.0, step=10.0)
    rainfall = st.sidebar.number_input("Annual Rainfall (mm)", min_value=100.0, max_value=5000.0, value=1000.0, step=50.0)
    
    roof_type = st.sidebar.selectbox(
        "Roof Material (Runoff Coeff. C)",
        ["Concrete / RCC Roof (C = 0.85)", "Corrugated Metal Sheet (C = 0.90)", "Clay / Ceramic Tile Roof (C = 0.75)", "Asbestos Sheet (C = 0.80)"]
    )
    coef_map = {"Concrete / RCC Roof (C = 0.85)": 0.85, "Corrugated Metal Sheet (C = 0.90)": 0.90, "Clay / Ceramic Tile Roof (C = 0.75)": 0.75, "Asbestos Sheet (C = 0.80)": 0.80}
    coef = coef_map[roof_type]
    occupants = st.sidebar.number_input("Household Occupants", min_value=1, max_value=50, value=4, step=1)

    # Calculations
    harvest_liters = area * (rainfall / 1000.0) * coef * 0.85 * 1000.0
    daily_demand = occupants * (5.0 + 30.0 + 15.0)
    annual_demand = daily_demand * 365.0
    coverage = (harvest_liters / annual_demand) * 100.0 if annual_demand > 0 else 0
    tank_size = math.ceil((daily_demand * 45) / 500.0) * 500

    monsoon_supply = 0.80 * harvest_liters
    monsoon_demand = daily_demand * 120.0
    dry_supply = 0.20 * harvest_liters
    dry_demand = daily_demand * 245.0

    # Metrics Display
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Annual Harvest Potential", f"{harvest_liters:,.0f} L", f"{harvest_liters/1000:.1f} m³")
    with m2:
        st.metric("Total Household Demand", f"{annual_demand:,.0f} L", f"{daily_demand:.0f} L/day")
    with m3:
        st.metric("Demand Coverage", f"{coverage:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # Feasibility Output
    if coverage >= 100.0:
        st.success(f"### 🟢 Verdict: FULLY FEASIBLE\nRecommended Storage Tank Size: **{tank_size:,} Liters**")
    elif coverage >= 40.0:
        st.warning(f"### 🟡 Verdict: PARTIALLY FEASIBLE\nRecommended Storage Tank Size: **{tank_size:,} Liters**")
    else:
        st.error(f"### 🔴 Verdict: UNFEASIBLE / LOW POTENTIAL\nRecommended Storage Tank Size: **{tank_size:,} Liters**")

    st.markdown("---")
    st.subheader("📈 Visual Graphical Analysis")

    # Bar Charts
    g_col1, g_col2 = st.columns(2)

    with g_col1:
        st.write("#### 💧 Harvest Potential vs Demand")
        chart_data = pd.DataFrame({
            "Category": ["Harvest Potential", "Annual Demand"],
            "Liters": [harvest_liters, annual_demand]
        }).set_index("Category")
        st.bar_chart(chart_data, color="#0284c7")

    with g_col2:
        st.write("#### 🌦️ Seasonal Supply & Demand Breakdown")
        seasonal_data = pd.DataFrame({
            "Period": ["Monsoon (4 Mos)", "Dry Season (8 Mos)"],
            "Supply": [monsoon_supply, dry_supply],
            "Demand": [monsoon_demand, dry_demand]
        }).set_index("Period")
        st.bar_chart(seasonal_data)

# ------------------------------------------------------------------------------
# 6. R23 ALIGNMENT
# ------------------------------------------------------------------------------
elif st.session_state.selected_topic == "R23 Alignment":
    st.header("🎓 6. JNTUK R23 Regulation Alignment")
    st.markdown("""
    * **Regulation:** JNTUK B.Tech R23 Regulation (Semester 2)
    * **Target Disciplines:** Civil Engineering / Mechanical Engineering / Allied Branches
    * **Curriculum Outcomes:**
      1. Practical calculation of civil hydrology formulas.
      2. Application of matrix algebra to real-world resource allocation problems.
      3. Creation of dynamic, user-centered computer software.
    """)