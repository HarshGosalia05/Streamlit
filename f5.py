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

# Custom CSS
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
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'energy_data' not in st.session_state:
    st.session_state.energy_data = []
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}

# Main Header
st.markdown("""
<div class="main-header">
    <h1 style="color: white; text-align: center;">\u26a1 Smart Energy Consumption Tracker</h1>
    <p style="color: white; text-align: center;">Track, analyze, and optimize your daily energy usage</p>
</div>
""", unsafe_allow_html=True)

# Sidebar - User Profile
with st.sidebar:
    # st.markdown("### \ud83d\udc64 User Profile")
    st.markdown("### 👤 User Profile")

    name = st.text_input("Your Name", value=st.session_state.user_profile.get('name', ''))
    age = st.number_input("Age", 18, 100, value=st.session_state.user_profile.get('age', 25))
    city = st.text_input("City", value=st.session_state.user_profile.get('city', ''))
    area = st.text_input("Area", value=st.session_state.user_profile.get('area', ''))
    # st.markdown("### \ud83c\udfe0 Housing Details")
    st.markdown("### 🏠 Housing Details")

    flat_tenement = st.selectbox("Housing Type", ["Flat", "Tenement"],
                                  index=0 if st.session_state.user_profile.get('flat_tenement', 'Flat') == 'Flat' else 1)
    facility = st.selectbox("Home Size", ["1BHK", "2BHK", "3BHK"],
                             index=["1BHK", "2BHK", "3BHK"].index(st.session_state.user_profile.get('facility', '1BHK')))
    st.session_state.user_profile.update({
        'name': name, 'age': age, 'city': city, 'area': area,
        'flat_tenement': flat_tenement, 'facility': facility
    })

# Main Content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### \ud83d\udcca Daily Energy Consumption Entry")
    selected_date = st.date_input("Select Date", value=date.today())
    st.markdown("#### \ud83c\udfe0 Appliance Usage")
    col_ac, col_fridge, col_wm = st.columns(3)

    with col_ac:
        ac_usage = st.selectbox("Air Conditioner", ["No", "Yes"], key="ac")
        ac_hours = st.slider("Hours of AC usage", 0, 24, 8, key="ac_hours") if ac_usage == "Yes" else 0

    with col_fridge:
        fridge_usage = st.selectbox("Refrigerator", ["No", "Yes"], key="fridge")
        fridge_efficiency = st.slider("Fridge Efficiency (1-5)", 1, 5, 3, key="fridge_eff") if fridge_usage == "Yes" else 0

    with col_wm:
        wm_usage = st.selectbox("Washing Machine", ["No", "Yes"], key="wm")
        wm_cycles = st.slider("Number of wash cycles", 0, 5, 1, key="wm_cycles") if wm_usage == "Yes" else 0

    st.markdown("#### \ud83d\udca1 Additional Appliances")
    col_lights, col_fans, col_tv = st.columns(3)
    lights_hours = st.slider("Lights usage (hours)", 0, 24, 6, key="lights")
    fans_hours = st.slider("Fans usage (hours)", 0, 24, 8, key="fans")
    tv_hours = st.slider("TV usage (hours)", 0, 24, 4, key="tv")

with col2:
    st.markdown("### \u26a1 Energy Calculation")
    base_energy = {"1BHK": 2*0.4+2*0.8, "2BHK": 3*0.4+3*0.8, "3BHK": 4*0.4+4*0.8}[facility]
    fridge_factor = {1: 0.2, 2: 0.18, 3: 0.15, 4: 0.12, 5: 0.1}

    appliance_breakdown = {
        "AC": ac_hours * 1.5,
        "Fridge": 24 * fridge_factor.get(fridge_efficiency, 0.15) if fridge_usage == "Yes" else 0,
        "Washing Machine": wm_cycles * 2,
        "Lights": lights_hours * 0.06,
        "Fans": fans_hours * 0.075,
        "TV": tv_hours * 0.15
    }

    appliance_energy = sum(appliance_breakdown.values())
    total_energy = base_energy + appliance_energy
    energy_cost = total_energy * 5
    carbon_footprint = total_energy * 0.82

    st.markdown(f"""
    <div class='energy-card'>
        <h3>Daily Energy Consumption</h3>
        <h2>{total_energy:.2f} kWh</h2>
        <p>Estimated Cost: ₹{energy_cost:.2f}</p>
    </div>
    """, unsafe_allow_html=True)

    if total_energy > 20:
        st.warning("\u26a0\ufe0f High energy consumption detected! Consider reducing usage.")

    max_appliance = max(appliance_breakdown, key=appliance_breakdown.get)
    st.info(f"\ud83d\udd0d Most consuming appliance today: **{max_appliance}**")

    if total_energy < 10:
        score = "\U0001F7E2 Efficient"
    elif total_energy < 15:
        score = "\U0001F7E1 Moderate"
    else:
        score = "\U0001F534 High Consumption"
    st.metric("Efficiency Score", score)

    st.metric("Base Consumption", f"{base_energy:.2f} kWh")
    st.metric("Appliances", f"{appliance_energy:.2f} kWh")
    st.metric("Carbon Footprint", f"{carbon_footprint:.2f} kg CO₂")

if st.button("\ud83d\udcc2 Save Daily Consumption", type="primary"):
    if name:
        entry = {
            'date': selected_date, 'name': name, 'city': city, 'area': area,
            'facility': facility, 'total_energy': total_energy,
            'base_energy': base_energy, 'appliance_energy': appliance_energy,
            'cost': energy_cost, 'carbon_footprint': carbon_footprint,
            'ac_hours': ac_hours, 'fridge_efficiency': fridge_efficiency,
            'wm_cycles': wm_cycles, 'lights_hours': lights_hours,
            'fans_hours': fans_hours, 'tv_hours': tv_hours
        }
        existing_entry = next((i for i, item in enumerate(st.session_state.energy_data) if item['date'] == selected_date), None)
        if existing_entry is not None:
            st.session_state.energy_data[existing_entry] = entry
            st.success(f"Updated energy data for {selected_date}")
        else:
            st.session_state.energy_data.append(entry)
            st.success(f"Saved energy data for {selected_date}")
    else:
        st.error("Please enter your name in the sidebar first!")

if st.session_state.energy_data:
    st.markdown("### \ud83d\udcca Historical Energy Consumption")
    df = pd.DataFrame(st.session_state.energy_data)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### \ud83d\uddd3\ufe0f Recent Entries")
        recent_df = df.tail(5)[['date', 'total_energy', 'cost']].copy()
        recent_df['date'] = recent_df['date'].dt.strftime('%Y-%m-%d')
        st.dataframe(recent_df, use_container_width=True)
    with col2:
        if len(df) > 1:
            fig = px.line(df, x='date', y='total_energy', title='Daily Energy Consumption Trend')
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### \ud83d\udcca Summary Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Average Daily", f"{df['total_energy'].mean():.2f} kWh")
    with col2:
        st.metric("Total This Month", f"{df['total_energy'].sum():.2f} kWh")
    with col3:
        st.metric("Average Cost", f"₹{df['cost'].mean():.2f}")
    with col4:
        st.metric("Total CO₂", f"{df['carbon_footprint'].sum():.2f} kg")

    current_month = pd.Timestamp.today().to_period('M')
    month_df = df[df['date'].dt.to_period('M') == current_month]
    if not month_df.empty:
        avg_daily_cost = month_df['cost'].mean()
        projected_bill = avg_daily_cost * 30
        
        st.metric("\ud83d\udcc5 Projected Monthly Bill", f"₹{projected_bill:.2f}")

    if len(df) >= 7:
        st.markdown("#### \ud83d\udd0d Weekly Analysis")
        col1, col2 = st.columns(2)
        with col1:
            latest_entry = df.iloc[-1]
            fig = px.pie(values=[latest_entry['base_energy'], latest_entry['appliance_energy']],
                         names=['Base Consumption', 'Appliances'], title='Energy Consumption Breakdown')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            df['month'] = df['date'].dt.to_period('M')
            monthly_cost = df.groupby('month')['cost'].sum().reset_index()
            monthly_cost['month'] = monthly_cost['month'].astype(str)
            fig = px.bar(monthly_cost, x='month', y='cost', title='Monthly Energy Cost')
            st.plotly_chart(fig, use_container_width=True)

    if st.button("\u2b07\ufe0f Download Data as CSV"):
        csv = df.to_csv(index=False)
        st.download_button("Download CSV", data=csv, file_name="energy_data.csv", mime="text/csv")

# Tips Section
st.markdown("### \ud83d\udca1 Energy Saving Tips")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""**\ud83c\udf21\ufe0f Cooling Tips**\n- Set AC to 24-26°C\n- Use fans with AC\n- Close curtains\n- Maintain AC regularly""")
with col2:
    st.markdown("""**\ud83d\udca1 Lighting Tips**\n- Use LED bulbs\n- Use daylight\n- Use motion sensors\n- Turn off unused lights""")
with col3:
    st.markdown("""**\ud83c\udfe0 General Tips**\n- Unplug unused devices\n- Buy efficient appliances\n- Regular servicing\n- Monitor your usage""")

st.markdown("---")
