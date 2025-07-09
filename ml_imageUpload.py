import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import random
import datetime
import plotly.express as px

# Page config
st.set_page_config(page_title="EcoSat Monitor", layout="wide", page_icon="🛰️")

# Initialize session state for history
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar - Navigation
st.sidebar.title("🌍 EcoSat Monitor")
st.sidebar.markdown("AI-powered satellite land cover analysis")

st.sidebar.header("📂 Configuration")
region = st.sidebar.selectbox("Select Region", ["Global", "Americas", "Europe", "Asia", "Africa"])
time_range = st.sidebar.selectbox("Select Time Range", ["7 Days", "30 Days", "90 Days"])
view_mode = st.sidebar.radio("Select View", ["Analyzer", "Dashboard History", "Insights"])

# Simulated model prediction
def simulate_model():
    predictions = {
        "Green Area": random.uniform(0.2, 0.5),
        "Water": random.uniform(0.1, 0.3),
        "Desert": random.uniform(0.1, 0.3),
        "Cloudy": random.uniform(0.05, 0.3)
    }
    total = sum(predictions.values())
    return {k: round(v / total, 3) for k, v in predictions.items()}

# Analyzer Tab
if view_mode == "Analyzer":
    st.title("📱 EcoSat Monitor - Satellite Image Analysis")
    st.subheader("📷 Upload Satellite Image")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png", "tiff"])

    
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Satellite Image", use_container_width=True)

        if st.button("🔍 Analyze Image"):
            with st.spinner("Running AI Model Analysis..."):
                predictions = simulate_model()
                confidence = max(predictions.values())
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Save analysis in session history
                st.session_state.history.append({
                    "timestamp": timestamp,
                    "region": region,
                    "predictions": predictions,
                    "confidence": round(confidence * 100)
                })

                st.success("✅ Analysis Complete")

                # Classification results
                st.subheader("🚁 Land Cover Classification")
                for label, prob in predictions.items():
                    st.progress(int(prob * 100), text=f"{label}: {prob * 100:.1f}%")

                # Plotly Chart
                st.subheader("📈 Prediction Chart")
                df_chart = pd.DataFrame({
                    'Land Cover Type': list(predictions.keys()),
                    'Percentage': [p * 100 for p in predictions.values()]
                })
                fig = px.bar(df_chart, x='Land Cover Type', y='Percentage',
                             color='Land Cover Type',
                             title="Land Cover Classification Breakdown",
                             text_auto='.2f', height=400)
                st.plotly_chart(fig, use_container_width=True)

                # Environmental Metrics
                st.subheader("🌿 Environmental Impact")
                veg = int(predictions["Green Area"] * 100)
                water = int(predictions["Water"] * 100)
                deforest = round((0.3 - predictions["Green Area"]) * 10, 1)
                urban = round((1 - predictions["Green Area"] - predictions["Water"]) * 2, 1)

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Vegetation Health", f"{veg}%")
                col2.metric("Water Quality", f"{water}%")
                col3.metric("Deforestation Rate", f"{deforest}%")
                col4.metric("Urban Expansion", f"{urban}%")

                # Alerts
                st.subheader("🚨 Alerts")
                if veg < 50:
                    st.warning("⚠ Low vegetation coverage detected")
                if deforest > 5:
                    st.error("🌲 High deforestation rate detected")
                if water < 30:
                    st.warning("💧 Limited water coverage detected")

# Dashboard History Tab
elif view_mode == "Dashboard History":
    st.title("📊 Dashboard - Analysis History")
    if len(st.session_state.history) > 0:
        for item in reversed(st.session_state.history[-5:]):
            with st.expander(f"🕒 {item['timestamp']} | 🌐 {item['region']} | 🔮 {item['confidence']}% Confidence"):
                cols = st.columns(len(item['predictions']))
                for i, (label, prob) in enumerate(item['predictions'].items()):
                    cols[i].metric(label, f"{prob * 100:.1f}%")
    else:
        st.info("Upload and analyze images to populate dashboard.")

# Insights Tab
elif view_mode == "Insights":
    st.title("📊 Insights Summary")
    if len(st.session_state.history) > 0:
        st.info(f"Total analyses done: {len(st.session_state.history)}")

        avg_veg = np.mean([entry['predictions']['Green Area'] for entry in st.session_state.history])
        avg_water = np.mean([entry['predictions']['Water'] for entry in st.session_state.history])
        avg_deforest = np.mean([(0.3 - entry['predictions']['Green Area']) * 10 for entry in st.session_state.history])

        col1, col2, col3 = st.columns(3)
        col1.metric("Avg. Vegetation", f"{avg_veg * 100:.1f}%")
        col2.metric("Avg. Water", f"{avg_water * 100:.1f}%")
        col3.metric("Avg. Deforestation", f"{avg_deforest:.1f}%")
    else:
        st.warning("No data available. Please analyze images first.")



