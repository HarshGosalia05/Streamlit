import streamlit as st
import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np
from io import BytesIO
import base64

# Configure page
st.set_page_config(
    page_title="Energy Consumption Tracker",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .energy-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .tip-card {
        background: #e8f5e8;
        border: 1px solid #4caf50;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .warning-card {
        background: #fff3cd;
        border: 1px solid #ffc107;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .stSelectbox > div > div {
        border-radius: 8px;
    }
    
    .stTextInput > div > div {
        border-radius: 8px;
    }
    
    .stNumberInput > div > div {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize MongoDB connection
@st.cache_resource
def init_connection():
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["Workshop"]
        collection = db["profile"]
        return collection
    except Exception as e:
        st.error(f"MongoDB connection failed: {e}")
        return None

# Energy calculation function
def calculate_energy(appliances):
    energy_rates = {
        'light': 0.2,
        'fans': 0.2,
        'tv': 0.3,
        'ac': 3.0,
        'fridge': 3.1,
        'washing_machine': 2.8
    }
    
    total_energy = 0
    for appliance, count in appliances.items():
        if count > 0:
            total_energy += count * energy_rates[appliance]
    
    return round(total_energy, 2)

# Energy saving tips
def get_energy_tips(energy_consumption):
    tips = []
    if energy_consumption > 15:
        tips.extend([
            "💡 Replace traditional bulbs with LED lights to save up to 75% energy",
            "❄️ Use inverter AC for better efficiency",
            "🌡️ Set AC temperature to 24°C for optimal energy saving",
            "🔌 Unplug electronics when not in use",
            "🌙 Use timer settings for appliances",
            "🪟 Improve home insulation to reduce AC usage"
        ])
    elif energy_consumption > 10:
        tips.extend([
            "✅ Good energy management! Consider solar panels for further savings",
            "🌱 Use natural light during daytime",
            "💨 Use fans along with AC to circulate air better"
        ])
    else:
        tips.extend([
            "🏆 Excellent energy management!",
            "🌟 You're an eco-friendly household",
            "🌱 Consider sharing your energy-saving tips with neighbors"
        ])
    
    return tips

# Data visualization function
def create_energy_chart(data):
    if len(data) < 2:
        return None
    
    # Prepare data for plotting
    dates = [item['date'] for item in data[-7:]]  # Last 7 entries
    energy_values = [item['energy_kwh_per_day'] for item in data[-7:]]
    day_names = [datetime.strptime(date, '%Y-%m-%d').strftime('%a\n%m-%d') for date in dates]
    
    # Create matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot line chart
    colors = ['red' if energy > 15 else 'green' for energy in energy_values]
    ax.plot(day_names, energy_values, marker='o', linewidth=2, markersize=8, color='#667eea')
    
    # Color markers based on energy consumption
    for i, (day, energy) in enumerate(zip(day_names, energy_values)):
        color = '#ff4444' if energy > 15 else '#44ff44'
        ax.scatter(day, energy, color=color, s=100, zorder=5)
        ax.annotate(f'{energy:.1f}', (day, energy), textcoords="offset points", 
                   xytext=(0,10), ha='center', fontweight='bold')
    
    ax.set_title('Daily Energy Usage Trend', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Day', fontsize=12)
    ax.set_ylabel('Energy (kWh)', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.set_facecolor('#f8f9fa')
    
    # Style the plot
    plt.xticks(rotation=0)
    plt.tight_layout()
    
    return fig

# Main app function
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>⚡ Energy Consumption Tracker</h1>
        <p>Monitor, Analyze, and Optimize Your Energy Usage</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize database connection
    collection = init_connection()
    
    # Sidebar for theme toggle and navigation
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <h3>🎛️ Dashboard Controls</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Theme toggle (placeholder - Streamlit doesn't support dynamic theme switching)
        theme = st.selectbox("🎨 Theme", ["Light Mode", "Dark Mode"], help="Theme selection")
        
        # Navigation
        page = st.selectbox("📋 Navigate", ["Energy Calculator", "View History", "Export Data"])
    
    if page == "Energy Calculator":
        show_energy_calculator(collection)
    elif page == "View History":
        show_history(collection)
    elif page == "Export Data":
        show_export_data(collection)

def show_energy_calculator(collection):
    st.header("📊 Energy Consumption Calculator")
    
    # User Profile Section
    with st.expander("👤 User Profile", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("📝 Full Name", placeholder="Enter your full name", help="Your full name for the record")
            age = st.number_input("🎂 Age", min_value=1, max_value=120, value=25, help="Your age in years")
        
        with col2:
            city = st.text_input("🏙️ City", placeholder="Enter your city", help="City where you live")
            area = st.text_input("📍 Area/Locality", placeholder="Enter your area", help="Your locality or area")
    
    # Appliance Entry Section
    st.header("🔌 Appliance Information")
    
    # Basic appliances
    with st.expander("💡 Basic Appliances", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            lights = st.number_input("💡 Lights", min_value=0, value=0, help="Number of lights in your home")
        
        with col2:
            fans = st.number_input("🌀 Fans", min_value=0, value=0, help="Number of fans in your home")
        
        with col3:
            tv = st.number_input("📺 TVs", min_value=0, value=0, help="Number of televisions")
    
    # Major appliances
    with st.expander("🏠 Major Appliances", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            has_ac = st.selectbox("❄️ Air Conditioner", ["No", "Yes"], help="Do you have an AC?")
            ac = st.number_input("Number of ACs", min_value=0, value=0, disabled=(has_ac == "No"))
        
        with col2:
            has_fridge = st.selectbox("🧊 Refrigerator", ["No", "Yes"], help="Do you have a refrigerator?")
            fridge = st.number_input("Number of Fridges", min_value=0, value=0, disabled=(has_fridge == "No"))
        
        with col3:
            has_wm = st.selectbox("🌊 Washing Machine", ["No", "Yes"], help="Do you have a washing machine?")
            washing_machine = st.number_input("Number of Washing Machines", min_value=0, value=0, disabled=(has_wm == "No"))
    
    # Calculate and display results
    if st.button("🔍 Calculate Energy Consumption", type="primary"):
        if not all([name, age, city, area]):
            st.error("❌ Please fill in all profile information!")
            return
        
        appliances = {
            'light': lights,
            'fans': fans,
            'tv': tv,
            'ac': ac if has_ac == "Yes" else 0,
            'fridge': fridge if has_fridge == "Yes" else 0,
            'washing_machine': washing_machine if has_wm == "Yes" else 0
        }
        
        # Calculate energy consumption
        total_energy = calculate_energy(appliances)
        rate_per_unit = 8  # ₹ per kWh
        daily_cost = round(total_energy * rate_per_unit, 2)
        monthly_cost = round(daily_cost * 30, 2)
        yearly_cost = round(daily_cost * 365, 2)
        
        # Display results
        st.success("✅ Calculation Complete!")
        
        # Metrics display
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("⚡ Daily Energy", f"{total_energy:.2f} kWh")
        
        with col2:
            st.metric("💰 Daily Cost", f"₹{daily_cost}")
        
        with col3:
            st.metric("📅 Monthly Cost", f"₹{monthly_cost}")
        
        with col4:
            st.metric("📈 Yearly Cost", f"₹{yearly_cost}")
        
        # Energy breakdown chart
        if total_energy > 0:
            appliance_names = ['Lights', 'Fans', 'TVs', 'AC', 'Refrigerator', 'Washing Machine']
            appliance_counts = [lights, fans, tv, ac, fridge, washing_machine]
            appliance_energy = [
                lights * 0.2, fans * 0.2, tv * 0.3, 
                ac * 3.0, fridge * 3.1, washing_machine * 2.8
            ]
            
            # Filter out zero values
            non_zero_indices = [i for i, energy in enumerate(appliance_energy) if energy > 0]
            filtered_names = [appliance_names[i] for i in non_zero_indices]
            filtered_energy = [appliance_energy[i] for i in non_zero_indices]
            
            if filtered_energy:
                fig, ax = plt.subplots(figsize=(10, 6))
                colors = plt.cm.Set3(np.linspace(0, 1, len(filtered_names)))
                bars = ax.bar(filtered_names, filtered_energy, color=colors)
                
                # Add value labels on bars
                for bar, energy in zip(bars, filtered_energy):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{energy:.1f}', ha='center', va='bottom', fontweight='bold')
                
                ax.set_title('Energy Consumption by Appliance', fontsize=14, fontweight='bold')
                ax.set_ylabel('Energy (kWh/day)')
                ax.set_facecolor('#f8f9fa')
                plt.xticks(rotation=45)
                plt.tight_layout()
                
                st.pyplot(fig)
        
        # Energy tips
        tips = get_energy_tips(total_energy)
        if total_energy > 15:
            st.markdown(f"""
            <div class="warning-card">
                <h4>⚠️ High Energy Usage Alert!</h4>
                <p>Your daily consumption is {total_energy:.2f} kWh. Consider these energy-saving tips:</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="tip-card">
                <h4>💡 Energy Saving Tips</h4>
                <p>Your daily consumption is {total_energy:.2f} kWh. Here are some tips:</p>
            </div>
            """, unsafe_allow_html=True)
        
        for tip in tips:
            st.write(f"• {tip}")
        
        # Save to database
        if collection is not None:
            try:
                data = {
                    "name": name,
                    "age": age,
                    "city": city,
                    "area": area,
                    "appliances": appliances,
                    "energy_kwh_per_day": total_energy,
                    "estimated_daily_cost": daily_cost,
                    "estimated_monthly_cost": monthly_cost,
                    "estimated_yearly_cost": yearly_cost,
                    "date": datetime.now().strftime('%Y-%m-%d'),
                    "day_of_week": datetime.now().strftime('%A'),
                    "timestamp": datetime.now()
                }
                
                collection.insert_one(data)
                st.success("✅ Data saved successfully to database!")
                
            except Exception as e:
                st.error(f"❌ Error saving to database: {e}")

def show_history(collection):
    st.header("📊 Energy Usage History")
    
    if collection is None:
        st.error("❌ Database connection not available")
        return
    
    try:
        # Fetch all records
        records = list(collection.find().sort("timestamp", -1))
        
        if not records:
            st.info("📝 No records found. Add some energy consumption data first!")
            return
        
        # Display summary statistics
        total_records = len(records)
        avg_energy = sum(record.get('energy_kwh_per_day', 0) for record in records) / total_records
        max_energy = max(record.get('energy_kwh_per_day', 0) for record in records)
        min_energy = min(record.get('energy_kwh_per_day', 0) for record in records)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📈 Total Records", total_records)
        
        with col2:
            st.metric("📊 Average Energy", f"{avg_energy:.2f} kWh")
        
        with col3:
            st.metric("🔝 Maximum Energy", f"{max_energy:.2f} kWh")
        
        with col4:
            st.metric("🔽 Minimum Energy", f"{min_energy:.2f} kWh")
        
        # Create and display chart
        fig = create_energy_chart(records)
        if fig:
            st.pyplot(fig)
            
            # Option to download chart
            buf = BytesIO()
            fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
            buf.seek(0)
            
            st.download_button(
                label="📥 Download Chart as PNG",
                data=buf.getvalue(),
                file_name=f"energy_usage_chart_{datetime.now().strftime('%Y%m%d')}.png",
                mime="image/png"
            )
        
        # Display records table
        st.subheader("📋 All Records")
        
        # Prepare data for display
        display_data = []
        for record in records:
            display_data.append({
                'Name': record.get('name', ''),
                'Date': record.get('date', ''),
                'Day': record.get('day_of_week', ''),
                'City': record.get('city', ''),
                'Energy (kWh)': record.get('energy_kwh_per_day', 0),
                'Daily Cost (₹)': record.get('estimated_daily_cost', 0),
                'Monthly Cost (₹)': record.get('estimated_monthly_cost', 0)
            })
        
        df = pd.DataFrame(display_data)
        st.dataframe(df, use_container_width=True)
        
    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")

def show_export_data(collection):
    st.header("📁 Export Data")
    
    if collection is None:
        st.error("❌ Database connection not available")
        return
    
    try:
        records = list(collection.find())
        
        if not records:
            st.info("📝 No data to export. Add some records first!")
            return
        
        # Prepare data for export
        export_data = []
        for record in records:
            # Flatten the appliances data
            appliances = record.get('appliances', {})
            export_row = {
                'Name': record.get('name', ''),
                'Age': record.get('age', ''),
                'City': record.get('city', ''),
                'Area': record.get('area', ''),
                'Date': record.get('date', ''),
                'Day_of_Week': record.get('day_of_week', ''),
                'Lights': appliances.get('light', 0),
                'Fans': appliances.get('fans', 0),
                'TVs': appliances.get('tv', 0),
                'Air_Conditioners': appliances.get('ac', 0),
                'Refrigerators': appliances.get('fridge', 0),
                'Washing_Machines': appliances.get('washing_machine', 0),
                'Energy_kWh_per_day': record.get('energy_kwh_per_day', 0),
                'Daily_Cost_INR': record.get('estimated_daily_cost', 0),
                'Monthly_Cost_INR': record.get('estimated_monthly_cost', 0),
                'Yearly_Cost_INR': record.get('estimated_yearly_cost', 0)
            }
            export_data.append(export_row)
        
        df = pd.DataFrame(export_data)
        
        # Display preview
        st.subheader("📊 Data Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Export options
        st.subheader("📥 Export Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # CSV export
            csv = df.to_csv(index=False)
            st.download_button(
                label="📄 Download as CSV",
                data=csv,
                file_name=f"energy_consumption_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with col2:
            # Excel export
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Energy Data')
            
            st.download_button(
                label="📊 Download as Excel",
                data=excel_buffer.getvalue(),
                file_name=f"energy_consumption_data_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        # Statistics
        st.subheader("📈 Quick Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📊 Total Records", len(df))
            st.metric("👥 Unique Users", df['Name'].nunique())
        
        with col2:
            st.metric("🏙️ Cities Covered", df['City'].nunique())
            st.metric("📅 Date Range", f"{df['Date'].min()} to {df['Date'].max()}")
        
        with col3:
            st.metric("⚡ Total Energy", f"{df['Energy_kWh_per_day'].sum():.2f} kWh")
            st.metric("💰 Total Cost", f"₹{df['Daily_Cost_INR'].sum():.2f}")
        
    except Exception as e:
        st.error(f"❌ Error exporting data: {e}")

if __name__ == "__main__":
    main()