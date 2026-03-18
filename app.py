import streamlit as st
import pickle
import numpy as np
import pandas as pd
import altair as alt
import time

# Page configuration
st.set_page_config(
    page_title="Smart Diet & Fitness",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for glassmorphism and premium feel
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.5);
    }
    
    /* Metrics / Cards */
    [data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid rgba(255, 255, 255, 0.5);
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.05);
        backdrop-filter: blur(8px);
        transition: transform 0.2s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-5px);
    }

    /* Primary Button */
    .stButton > button {
        background: linear-gradient(135deg, #ff0844 0%, #ffb199 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 8, 68, 0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255, 8, 68, 0.4) !important;
    }

    /* Headers */
    h1, h2, h3 {
        color: #2D3748 !important;
        font-weight: 700 !important;
    }

    /* Custom progress bar container */
    .meter-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.05);
        margin: 20px 0;
    }

    .meter-bar-bg {
        background: #EDF2F7;
        border-radius: 20px;
        height: 30px;
        width: 100%;
        overflow: hidden;
        position: relative;
    }
    
    .meter-bar-fill {
        background: linear-gradient(90deg, #f6d365 0%, #fda085 100%);
        height: 100%;
        border-radius: 20px;
        transition: width 1s ease-in-out;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-right: 15px;
        color: white;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }

    /* Insight Cards */
    .insight-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #ff0844;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        margin-bottom: 15px;
        transition: all 0.2s ease;
    }
    .insight-card:hover {
        transform: translateX(5px);
    }
</style>
""", unsafe_allow_html=True)

# Load trained model
@st.cache_resource
def load_model():
    return pickle.load(open("model/calorie_model.pkl", "rb"))

try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

def get_calorie_insights(calories, age, gender, bmi):
    """Generate personalized insights based on prediction."""
    insights = []
    
    # Age-based BMR estimates (rough)
    if gender == "Male":
        bmr_estimate = 88.362 + (13.397 * (70/2.20462)) + (4.799 * 170) - (5.677 * age)
    else:
        bmr_estimate = 447.593 + (9.247 * (60/2.20462)) + (3.098 * 160) - (4.330 * age)
        
    activity_factor = calories / bmr_estimate if bmr_estimate > 0 else 1

    if activity_factor < 1.2:
        insights.append({"icon": "⚠️", "title": "Low Activity Level", "text": "Consider increasing daily movement for better health."})
    elif activity_factor < 1.5:
        insights.append({"icon": "✅", "title": "Moderate Activity", "text": "Good balance of rest and activity."})
    else:
        insights.append({"icon": "🔥", "title": "High Activity Level", "text": "Excellent! You're burning significant calories."})

    if bmi < 18.5:
        insights.append({"icon": "📈", "title": "Underweight", "text": "Focus on nutrient-dense foods to support your active lifestyle."})
    elif bmi < 25:
        insights.append({"icon": "⭐", "title": "Healthy Weight", "text": "Great job maintaining a healthy BMI!"})
    elif bmi < 30:
        insights.append({"icon": "⚖️", "title": "Overweight", "text": "Consider combining this activity with mindful eating."})
    else:
        insights.append({"icon": "🏥", "title": "Obese", "text": "Consult healthcare professionals for personalized guidance."})

    return insights

# App title and description
st.title("⚡ Smart Diet & Fitness")
st.markdown("<p style='font-size: 1.2rem; color: #4A5568;'>AI-powered daily caloric expenditure prediction with a beautiful, dynamic interface.</p>", unsafe_allow_html=True)

# Sidebar inputs
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>🔥 Data Entry</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.header("👤 Your Profile")
    
    age = st.slider("Age (years)", 10, 100, 25)
    bmi = st.slider("BMI", 10.0, 50.0, 22.0, 0.1)
    gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
    
    st.markdown("---")
    st.header("🏃‍♂️ Activity Log")
    
    active_hours = st.slider("Active Hours / Day", 0.0, 24.0, 8.0, 0.5)
    workout_hours = st.slider("Workout Hours / Day", 0.0, 12.0, 1.0, 0.25)
    workout_type = st.selectbox("Workout Type", ["None", "Cardio", "Strength", "Mixed"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("Predict Calories 🔥", use_container_width=True)

# Main prediction area
if predict_btn or 'prediction' not in st.session_state:
    if predict_btn:
        gender_encoded = 1 if gender == "Male" else 0
        workout_mixed = 1 if workout_type == "Mixed" else 0
        workout_none = 1 if workout_type == "None" else 0
        workout_strength = 1 if workout_type == "Strength" else 0
        
        feature_names = ['age', 'bmi', 'active_hours', 'workout_hours', 'gender_Male',
                         'workout_type_Mixed', 'workout_type_None', 'workout_type_Strength']
                         
        features_df = pd.DataFrame([[
            age, bmi, active_hours, workout_hours, gender_encoded, 
            workout_mixed, workout_none, workout_strength
        ]], columns=feature_names)
        
        with st.spinner("Analyzing your profile..."):
            time.sleep(0.5)
            prediction = model.predict(features_df)[0]
            st.session_state.prediction = prediction
    else:
        st.info("👈 Enter your details in the sidebar and click 'Predict Calories' to see your results!")
        st.stop()

prediction = st.session_state.prediction

# Dashboard Layout
col1, col2, col3 = st.columns(3)

daily_needs = 2000 if gender == "Female" else 2500
surplus_deficit = prediction - daily_needs
activity_level = "Low" if prediction < 2000 else "Moderate" if prediction < 2500 else "High"

with col1:
    st.metric("Estimated Burn", f"{prediction:.0f} kcal", delta="Total Daily Energy")
with col2:
    st.metric("Activity Level", activity_level, delta="Based on burn rate", delta_color="off")
with col3:
    st.metric("vs Daily Intake Needs", f"{surplus_deficit:+.0f} kcal", delta=f"{daily_needs} kcal Base", delta_color="inverse")

# Beautiful HTML Meter
max_cal = 4000
width_pct = min(100, (prediction / max_cal) * 100)

st.markdown(f"""
<div class="meter-container">
    <h3 style="margin-top:0; color: #2D3748;">🔥 Calorie Burn Intensity</h3>
    <div class="meter-bar-bg">
        <div class="meter-bar-fill" style="width: {width_pct}%;">
            {prediction:.0f} kcal
        </div>
    </div>
    <div style="display: flex; justify-content: space-between; margin-top: 10px; color: #A0AEC0; font-size: 0.9rem;">
        <span>0</span>
        <span>2000</span>
        <span>4000+</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Charts and Insights side-by-side
c1, c2 = st.columns([1.5, 1])

with c1:
    st.subheader("📊 Breakdown & Sources")
    
    # Altair Chart
    bmr_est = prediction * 0.6
    act_est = prediction * 0.25
    exc_est = prediction * 0.15
    
    df_breakdown = pd.DataFrame({
        "Category": ["Basal Metabolic Rate", "Daily Activity", "Exercise"],
        "Calories": [bmr_est, act_est, exc_est]
    })
    
    chart = alt.Chart(df_breakdown).mark_arc(innerRadius=70, cornerRadius=10).encode(
        theta=alt.Theta(field="Calories", type="quantitative"),
        color=alt.Color(field="Category", type="nominal", scale=alt.Scale(range=["#ff0844", "#4FACFE", "#00F2FE"])),
        tooltip=["Category", alt.Tooltip("Calories", format=",.0f")]
    ).properties(
        width=400,
        height=350
    ).configure_view(strokeWidth=0).configure_legend(
        labelFontSize=14,
        titleFontSize=16,
        orient='bottom'
    )
    
    st.altair_chart(chart, use_container_width=True)

with c2:
    st.subheader("💡 Smart Insights")
    insights = get_calorie_insights(prediction, age, gender, bmi)
    for ins in insights:
        st.markdown(f"""
        <div class="insight-card">
            <h4 style="margin:0; color:#2D3748; display:flex; align-items:center; gap:8px;">
                <span>{ins['icon']}</span> 
                <span>{ins['title']}</span>
            </h4>
            <p style="margin:8px 0 0 0; color:#4A5568; font-size: 0.95rem; line-height:1.4;">{ins['text']}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='text-align: center; color: #A0AEC0; margin-top: 50px; font-size: 0.8rem;'>Smart Diet & Fitness Predictor • Built with Streamlit</div>", unsafe_allow_html=True)
