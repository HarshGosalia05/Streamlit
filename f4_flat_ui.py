import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Energy Consumption Tracker",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .energy-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .stSelectbox > div > div {
        background-color: #f0f2f6;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for data persistence
if 'energy_data' not in st.session_state:
    st.session_state.energy_data = []

if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}

# Main header
st.markdown("""
<div class="main-header">
    <h1 style="color: white; text-align: center; margin: 0;">
        ⚡ Smart Energy Consumption Tracker
    </h1>
    <p style="color: white; text-align: center; margin: 0.5rem 0 0 0;">
        Track, analyze, and optimize your daily energy usage
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar for user profile
with st.sidebar:
    st.markdown("### 👤 User Profile")
    
    name = st.text_input("Your Name", value=st.session_state.user_profile.get('name', ''))
    age = st.number_input("Age", min_value=18, max_value=100, value=st.session_state.user_profile.get('age', 25))
    city = st.text_input("City", value=st.session_state.user_profile.get('city', ''))
    area = st.text_input("Area", value=st.session_state.user_profile.get('area', ''))
    
    st.markdown("### 🏠 Housing Details")
    flat_tenement = st.selectbox("Housing Type", ["Flat", "Tenement"], 
                                index=0 if st.session_state.user_profile.get('flat_tenement', 'Flat') == 'Flat' else 1)
    facility = st.selectbox("Home Size", ["1BHK", "2BHK", "3BHK"], 
                           index=["1BHK", "2BHK", "3BHK"].index(st.session_state.user_profile.get('facility', '1BHK')))
    
    # Update session state
    st.session_state.user_profile.update({
        'name': name,
        'age': age,
        'city': city,
        'area': area,
        'flat_tenement': flat_tenement,
        'facility': facility
    })

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📊 Daily Energy Consumption Entry")
    
    # Date selection
    selected_date = st.date_input("Select Date", value=date.today())
    
    # Appliance usage section
    st.markdown("#### 🏠 Appliance Usage")
    
    col_ac, col_fridge, col_wm = st.columns(3)
    
    with col_ac:
        ac_usage = st.selectbox("Air Conditioner", ["No", "Yes"], key="ac")
        if ac_usage == "Yes":
            ac_hours = st.slider("Hours of AC usage", 0, 24, 8, key="ac_hours")
        else:
            ac_hours = 0
    
    with col_fridge:
        fridge_usage = st.selectbox("Refrigerator", ["No", "Yes"], key="fridge")
        # Fridge typically runs 24/7, so we'll use efficiency factor
        fridge_efficiency = st.slider("Fridge Efficiency (1-5)", 1, 5, 3, key="fridge_eff") if fridge_usage == "Yes" else 0
    
    with col_wm:
        wm_usage = st.selectbox("Washing Machine", ["No", "Yes"], key="wm")
        if wm_usage == "Yes":
            wm_cycles = st.slider("Number of wash cycles", 0, 5, 1, key="wm_cycles")
        else:
            wm_cycles = 0
    
    # Additional appliances
    st.markdown("#### 💡 Additional Appliances")
    col_lights, col_fans, col_tv = st.columns(3)
    
    with col_lights:
        lights_hours = st.slider("Lights usage (hours)", 0, 24, 6, key="lights")
    
    with col_fans:
        fans_hours = st.slider("Fans usage (hours)", 0, 24, 8, key="fans")
    
    with col_tv:
        tv_hours = st.slider("TV usage (hours)", 0, 24, 4, key="tv")

with col2:
    st.markdown("### ⚡ Energy Calculation")
    
    # Calculate base energy consumption based on home size
    base_energy = 0
    if facility == "1BHK":
        base_energy = 2 * 0.4 + 2 * 0.8  # 2 lights + 2 fans base
    elif facility == "2BHK":
        base_energy = 3 * 0.4 + 3 * 0.8  # 3 lights + 3 fans base
    elif facility == "3BHK":
        base_energy = 4 * 0.4 + 4 * 0.8  # 4 lights + 4 fans base
    
    # Calculate appliance energy consumption (kWh)
    appliance_energy = 0
    
    # AC consumption (assuming 1.5kW per hour)
    if ac_usage == "Yes":
        appliance_energy += ac_hours * 1.5
    
    # Fridge consumption (assuming 0.15kW per hour, adjusted by efficiency)
    if fridge_usage == "Yes":
        fridge_factor = {1: 0.2, 2: 0.18, 3: 0.15, 4: 0.12, 5: 0.1}
        appliance_energy += 24 * fridge_factor.get(fridge_efficiency, 0.15)
    
    # Washing machine (assuming 2kW per cycle)
    appliance_energy += wm_cycles * 2
    
    # Additional appliances
    appliance_energy += lights_hours * 0.06  # LED lights
    appliance_energy += fans_hours * 0.075   # Ceiling fans
    appliance_energy += tv_hours * 0.15      # LED TV
    
    total_energy = base_energy + appliance_energy
    
    # Energy cost calculation (assuming ₹5 per kWh)
    energy_cost = total_energy * 5
    
    # Display energy metrics
    st.markdown(f"""
    <div class="energy-card">
        <h3>Daily Energy Consumption</h3>
        <h2>{total_energy:.2f} kWh</h2>
        <p>Estimated Cost: ₹{energy_cost:.2f}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### 📈 Energy Breakdown")
    st.metric("Base Consumption", f"{base_energy:.2f} kWh")
    st.metric("Appliances", f"{appliance_energy:.2f} kWh")
    
    # Carbon footprint (assuming 0.82 kg CO2 per kWh)
    carbon_footprint = total_energy * 0.82
    st.metric("Carbon Footprint", f"{carbon_footprint:.2f} kg CO₂")

# Save data button
if st.button("💾 Save Daily Consumption", type="primary"):
    if name:
        entry = {
            'date': selected_date,
            'name': name,
            'city': city,
            'area': area,
            'facility': facility,
            'total_energy': total_energy,
            'base_energy': base_energy,
            'appliance_energy': appliance_energy,
            'cost': energy_cost,
            'carbon_footprint': carbon_footprint,
            'ac_hours': ac_hours,
            'fridge_efficiency': fridge_efficiency,
            'wm_cycles': wm_cycles,
            'lights_hours': lights_hours,
            'fans_hours': fans_hours,
            'tv_hours': tv_hours
        }
        
        # Check if entry for this date already exists
        existing_entry = next((i for i, item in enumerate(st.session_state.energy_data) 
                             if item['date'] == selected_date), None)
        
        if existing_entry is not None:
            st.session_state.energy_data[existing_entry] = entry
            st.success(f"Updated energy data for {selected_date}")
        else:
            st.session_state.energy_data.append(entry)
            st.success(f"Saved energy data for {selected_date}")
    else:
        st.error("Please enter your name in the sidebar first!")

# Display historical data
if st.session_state.energy_data:
    st.markdown("### 📊 Historical Energy Consumption")
    
    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(st.session_state.energy_data)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # Display recent entries
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📅 Recent Entries")
        recent_df = df.tail(5)[['date', 'total_energy', 'cost']].copy()
        recent_df['date'] = recent_df['date'].dt.strftime('%Y-%m-%d')
        st.dataframe(recent_df, use_container_width=True)
    
    with col2:
        st.markdown("#### 📈 Energy Trends")
        if len(df) > 1:
            fig = px.line(df, x='date', y='total_energy', 
                         title='Daily Energy Consumption Trend',
                         labels={'total_energy': 'Energy (kWh)', 'date': 'Date'})
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    # Summary statistics
    st.markdown("#### 📊 Summary Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Average Daily", f"{df['total_energy'].mean():.2f} kWh")
    
    with col2:
        st.metric("Total This Month", f"{df['total_energy'].sum():.2f} kWh")
    
    with col3:
        st.metric("Average Cost", f"₹{df['cost'].mean():.2f}")
    
    with col4:
        st.metric("Total CO₂", f"{df['carbon_footprint'].sum():.2f} kg")
    
    # Detailed analytics
    if len(df) >= 7:
        st.markdown("#### 🔍 Weekly Analysis")
        
        # Energy breakdown pie chart
        col1, col2 = st.columns(2)
        
        with col1:
            latest_entry = df.iloc[-1]
            breakdown_data = {
                'Base Consumption': latest_entry['base_energy'],
                'Appliances': latest_entry['appliance_energy']
            }
            
            fig = px.pie(values=list(breakdown_data.values()), 
                        names=list(breakdown_data.keys()),
                        title='Energy Consumption Breakdown')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Monthly cost trend
            df['month'] = df['date'].dt.to_period('M')
            monthly_cost = df.groupby('month')['cost'].sum().reset_index()
            monthly_cost['month'] = monthly_cost['month'].astype(str)
            
            fig = px.bar(monthly_cost, x='month', y='cost',
                        title='Monthly Energy Cost',
                        labels={'cost': 'Cost (₹)', 'month': 'Month'})
            st.plotly_chart(fig, use_container_width=True)

# Tips section
st.markdown("### 💡 Energy Saving Tips")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **🌡️ Cooling Tips**
    - Set AC to 24-26°C
    - Use fans with AC
    - Close curtains during day
    - Regular AC maintenance
    """)

with col2:
    st.markdown("""
    **💡 Lighting Tips**
    - Use LED bulbs
    - Natural light during day
    - Motion sensors
    - Turn off unused lights
    """)

with col3:
    st.markdown("""
    **🏠 General Tips**
    - Unplug devices when not in use
    - Use energy-efficient appliances
    - Regular maintenance
    - Monitor usage patterns
    """)

# Footer
st.markdown("---")
st.markdown("*💚 Track your energy consumption and contribute to a greener planet!*")