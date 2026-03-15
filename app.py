import streamlit as st
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Smart Diet & Fitness Predictor",
    page_icon="🔥",
    layout="wide",
)

# Load trained model
model = pickle.load(open("model/calorie_model.pkl", "rb"))

def create_calorie_meter(calories, max_calories=3000):
    """Create a visual calorie meter using matplotlib with enhanced styling."""
    fig, ax = plt.subplots(figsize=(6, 2), facecolor='#f8f9fa')

    # Create gradient effect for the bar
    from matplotlib.patches import Rectangle
    import matplotlib.colors as mcolors

    # Background bar with subtle gradient
    bg_bar = Rectangle((0, -0.2), max_calories, 0.4, facecolor='#e9ecef',
                      edgecolor='#dee2e6', linewidth=1, alpha=0.8)
    ax.add_patch(bg_bar)

    # Main calorie bar with gradient
    if calories > 0:
        # Create gradient from orange to red
        gradient = mcolors.LinearSegmentedColormap.from_list("calorie_grad",
                                                            ['#FF8C42', '#FF6B35', '#FF4500'])
        bar = Rectangle((0, -0.2), calories, 0.4, facecolor=gradient(0.5),
                       edgecolor='#CC3333', linewidth=2, alpha=0.9)
        ax.add_patch(bar)

        # Add shine effect
        shine = Rectangle((calories * 0.1, -0.15), calories * 0.8, 0.1,
                         facecolor='white', alpha=0.3)
        ax.add_patch(shine)

    # Add text with better styling
    if calories > 200:  # Only show text if bar is wide enough
        ax.text(calories/2, 0, f'{calories:.0f} kcal', ha='center', va='center',
                fontsize=12, fontweight='bold', color='white',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#CC3333", alpha=0.8,
                         edgecolor="none"))

    # Styling
    ax.set_xlim(0, max_calories)
    ax.set_ylim(-0.5, 0.5)
    ax.set_xticks([0, max_calories/2, max_calories])
    ax.set_xticklabels(['0', f'{max_calories//2}', f'{max_calories}'], fontsize=8)
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(False)
    ax.set_facecolor('#f8f9fa')
    ax.grid(axis='x', alpha=0.3, linestyle='--')

    # Add title
    ax.set_title('Daily Calorie Burn', fontsize=11, fontweight='bold',
                color='#2c3e50', pad=10)

    return fig

def get_calorie_insights(calories, age, gender, bmi):
    """Generate personalized insights based on prediction."""
    insights = []

    # Age-based BMR estimates (rough)
    if gender == "Male":
        bmr_estimate = 88.362 + (13.397 * (70/2.20462)) + (4.799 * 170) - (5.677 * age)  # rough conversion
    else:
        bmr_estimate = 447.593 + (9.247 * (60/2.20462)) + (3.098 * 160) - (4.330 * age)

    activity_factor = calories / bmr_estimate if bmr_estimate > 0 else 1

    if activity_factor < 1.2:
        insights.append("⚠️ **Low Activity Level**: Consider increasing daily movement for better health.")
    elif activity_factor < 1.5:
        insights.append("✅ **Moderate Activity**: Good balance of rest and activity.")
    else:
        insights.append("🔥 **High Activity Level**: Excellent! You're burning significant calories.")

    # BMI-based suggestions
    if bmi < 18.5:
        insights.append("📈 **Underweight**: Focus on nutrient-dense foods to support your active lifestyle.")
    elif bmi < 25:
        insights.append("✅ **Healthy Weight**: Great job maintaining a healthy BMI!")
    elif bmi < 30:
        insights.append("⚖️ **Overweight**: Consider combining this activity with mindful eating.")
    else:
        insights.append("🏥 **Obese**: Consult healthcare professionals for personalized guidance.")

    # Calorie-based suggestions
    if calories < 1800:
        insights.append("🍎 **Low Calorie Burn**: Consider adding more activity to support metabolism.")
    elif calories > 2500:
        insights.append("💪 **High Calorie Burn**: Ensure adequate nutrition to fuel your active lifestyle.")

    return insights

# App title and description
st.title("🔥 Smart Diet & Fitness Predictor")
st.markdown("""
Predict the calories you'll burn based on your lifestyle and workout habits.
This AI-powered tool helps you understand your daily caloric expenditure to optimize your diet and fitness goals.
""")

# Create two columns for better layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📊 Personal Information")

    # Age input
    age = st.number_input(
        "Age (years)",
        min_value=10,
        max_value=100,
        value=25,
        step=1,
        help="Enter your age in years"
    )

    # BMI input
    bmi = st.number_input(
        "BMI",
        min_value=10.0,
        max_value=50.0,
        value=22.0,
        step=0.1,
        format="%.1f",
        help="Body Mass Index (weight in kg / height in m²)"
    )

    # Gender selection
    gender = st.selectbox(
        "Gender",
        options=["Male", "Female"],
        help="Select your gender"
    )

with col2:
    st.header("💪 Activity Information")

    # Active hours per day
    active_hours = st.number_input(
        "Active Hours per Day",
        min_value=0.0,
        max_value=24.0,
        value=8.0,
        step=0.5,
        format="%.1f",
        help="Hours spent in daily activities (walking, standing, etc.)"
    )

    # Workout hours per day
    workout_hours = st.number_input(
        "Workout Hours per Day",
        min_value=0.0,
        max_value=12.0,
        value=1.0,
        step=0.25,
        format="%.1f",
        help="Hours spent exercising per day"
    )

    # Workout type selection
    workout_type = st.selectbox(
        "Workout Type",
        options=["None", "Cardio", "Strength", "Mixed"],
        help="Primary type of workout you do"
    )

# Prediction section
st.header("🔮 Prediction")

# Predict button
if st.button("Predict Calories Burned", type="primary", use_container_width=True):
    # Encode gender: Male = 1, Female = 0 (based on model feature 'gender_Male')
    gender_encoded = 1 if gender == "Male" else 0

    # Encode workout type: one-hot encoding
    # Model features: workout_type_Mixed, workout_type_None, workout_type_Strength
    workout_mixed = 1 if workout_type == "Mixed" else 0
    workout_none = 1 if workout_type == "None" else 0
    workout_strength = 1 if workout_type == "Strength" else 0
    # Note: Cardio is not in the model, so all zeros for Cardio

    # Create feature DataFrame with correct column names
    feature_names = ['age', 'bmi', 'active_hours', 'workout_hours', 'gender_Male',
                     'workout_type_Mixed', 'workout_type_None', 'workout_type_Strength']

    features_df = pd.DataFrame([[
        age,                    # age
        bmi,                    # bmi
        active_hours,           # active_hours
        workout_hours,          # workout_hours
        gender_encoded,         # gender_Male
        workout_mixed,          # workout_type_Mixed
        workout_none,           # workout_type_None
        workout_strength        # workout_type_Strength
    ]], columns=feature_names)

    # Make prediction
    prediction = model.predict(features_df)[0]

    # Enhanced Results Display
    st.header("📊 Your Calorie Burn Analysis")

    # Main metric display
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.metric(
            "Estimated Daily Calories Burned",
            f"{prediction:.0f} kcal",
            help="Total energy expenditure including BMR, daily activities, and exercise"
        )

    with col2:
        # Calculate activity level
        activity_level = "Low" if prediction < 2000 else "Moderate" if prediction < 2500 else "High"
        st.metric("Activity Level", activity_level)

    with col3:
        # Rough daily calorie needs estimate
        daily_needs = 2000 if gender == "Female" else 2500
        surplus_deficit = prediction - daily_needs
        st.metric(
            "vs Daily Needs",
            f"{surplus_deficit:+.0f} kcal",
            help=f"Compared to estimated {daily_needs} kcal daily needs"
        )

    # Calorie Meter and Comparison Chart side by side
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("🔥 Calorie Burn Meter")
        fig = create_calorie_meter(prediction)
        st.pyplot(fig, width='stretch')

    with col_chart2:
        st.subheader("📈 Activity Comparison")

        # Create comparison data with smaller chart
        categories = ['Sedentary', 'Light', 'Moderate', 'Very Active']
        values = [1800, 2200, 2500, 2800]
        colors = ['#E0E0E0'] * len(values)

        # Determine user's position first
        user_x_pos = None
        if prediction >= 1800 and prediction < 2200:
            user_x_pos = 0
            colors[0] = '#FF4B4B'
        elif prediction >= 2200 and prediction < 2500:
            user_x_pos = 1
            colors[1] = '#FF4B4B'
        elif prediction >= 2500 and prediction < 2800:
            user_x_pos = 2
            colors[2] = '#FF4B4B'
        else:
            user_x_pos = 3
            colors[3] = '#FF4B4B'

        fig2, ax2 = plt.subplots(figsize=(5, 4), facecolor='#f8f9fa')

        # Create bars with gradient effects
        bars = []
        for i, (value, color) in enumerate(zip(values, colors)):
            # Create gradient bars
            bar_color = color if color != '#E0E0E0' else '#bdc3c7'
            bar = ax2.bar(i, value, width=0.7, color=bar_color, alpha=0.9,
                         edgecolor='#34495e' if color != '#E0E0E0' else '#95a5a6',
                         linewidth=1.5, zorder=3)

            # Add subtle shadow effect
            ax2.bar(i, value, width=0.7, color='black', alpha=0.1,
                   bottom=-value*0.02, zorder=2)

            bars.append(bar)

        # Enhanced horizontal line for user's burn
        ax2.axhline(y=prediction, color='#e74c3c', linestyle='-', linewidth=2,
                   alpha=0.8, zorder=4, label=f'Your Burn: {prediction:.0f} kcal')

        # Add glow effect around the line
        for offset in [-0.5, 0.5]:
            ax2.axhline(y=prediction + offset, color='#e74c3c', linestyle='-',
                       linewidth=1, alpha=0.3, zorder=3)

        # Enhanced marker point
        ax2.scatter(user_x_pos, prediction, color='#e74c3c', s=100, zorder=6,
                   edgecolor='white', linewidth=3, marker='o',
                   label=f'Your Position')

        # Add inner highlight to marker
        ax2.scatter(user_x_pos, prediction, color='white', s=30, zorder=7,
                   marker='o', alpha=0.8)

        # Enhanced annotation
        bbox_props = dict(boxstyle="round,pad=0.4", facecolor='#e74c3c',
                         edgecolor='white', alpha=0.95, linewidth=2)
        ax2.annotate(f'You: {prediction:.0f} kcal',
                    xy=(user_x_pos, prediction),
                    xytext=(user_x_pos + 0.4, prediction + 80),
                    fontsize=9, fontweight='bold', color='white',
                    bbox=bbox_props,
                    arrowprops=dict(arrowstyle='->', color='#e74c3c',
                                  alpha=0.8, linewidth=2, shrinkA=5, shrinkB=5))

        # Enhanced styling
        ax2.set_xticks(range(len(categories)))
        ax2.set_xticklabels(categories, rotation=45, ha='right', fontsize=9,
                           fontweight='medium', color='#2c3e50')
        ax2.set_ylabel('Calories Burned', fontsize=10, fontweight='medium',
                      color='#2c3e50')
        ax2.set_title('Activity Level Comparison', fontsize=12, fontweight='bold',
                     color='#2c3e50', pad=15)
        ax2.legend(fontsize=8, loc='upper left', framealpha=0.9,
                  facecolor='white', edgecolor='#bdc3c7')
        ax2.grid(axis='y', alpha=0.4, linestyle='--', color='#bdc3c7', zorder=1)
        ax2.set_facecolor('#f8f9fa')

        # Enhanced y-axis scaling
        y_max = max(max(values) + 150, prediction + 150)
        ax2.set_ylim(0, y_max)

        # Add subtle background pattern
        ax2.axhspan(0, y_max, facecolor='#ffffff', alpha=0.5, zorder=0)

        # Enhanced value labels with better positioning
        for i, (bar, value) in enumerate(zip(bars, values)):
            height = bar[0].get_height()
            ax2.text(i, height + 25, f'{value}', ha='center', va='bottom',
                    fontsize=8, fontweight='bold', color='#2c3e50',
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                             edgecolor="none", alpha=0.8))

        st.pyplot(fig2, width='stretch')

    # Personalized Insights
    st.subheader("💡 Personalized Insights")
    insights = get_calorie_insights(prediction, age, gender, bmi)

    for insight in insights:
        st.info(insight)

    # Calorie Breakdown (estimated)
    st.subheader("🔍 Estimated Calorie Breakdown")

    # Rough estimates
    bmr_estimate = prediction * 0.6  # ~60% of total calories
    activity_calories = prediction * 0.25  # ~25% from daily activity
    exercise_calories = prediction * 0.15  # ~15% from structured exercise

    breakdown_data = pd.DataFrame({
        'Source': ['Basal Metabolic Rate', 'Daily Activities', 'Exercise/Workout', 'Other'],
        'Calories': [bmr_estimate, activity_calories, exercise_calories, prediction - bmr_estimate - activity_calories - exercise_calories],
        'Percentage': [60, 25, 15, 0]
    })

    col_break1, col_break2 = st.columns([1.2, 1])

    with col_break1:
        st.dataframe(breakdown_data.style.format({'Calories': '{:.0f}', 'Percentage': '{:.0f}%'}))

    with col_break2:
        # Pie chart - smaller and more readable
        fig3, ax3 = plt.subplots(figsize=(3.5, 3.5), facecolor='#f8f9fa')

        # Enhanced color palette
        colors_pie = ['#FF6B35', '#00BFA5', '#2196F3', '#FFC107']
        explode = [0.03 if i == breakdown_data['Calories'].idxmax() else 0 for i in range(len(breakdown_data))]

        wedges, texts, autotexts = ax3.pie(breakdown_data['Calories'],
                                          labels=breakdown_data['Source'],
                                          autopct='%1.0f%%', startangle=90,
                                          pctdistance=0.80, labeldistance=1.05,
                                          colors=colors_pie, explode=explode,
                                          shadow=True, wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})

        ax3.axis('equal')
        ax3.set_title('Calorie Sources', fontsize=12, fontweight='bold',
                     color='#2c3e50', pad=15)

        # Enhanced text styling - smaller for better readability
        plt.setp(autotexts, size=9, weight="bold", color="white")
        plt.setp(texts, size=8, weight="medium", color="#2c3e50")

        # Hide legend - labels are now placed around the chart
        ax3.legend([], [], frameon=False)

        # Add center circle for donut effect - slightly smaller
        centre_circle = plt.Circle((0,0), 0.65, fc='white', edgecolor='#bdc3c7', linewidth=1.5)
        ax3.add_artist(centre_circle)

        # Add center text - smaller font
        ax3.text(0, 0, f'Total\n{prediction:.0f}\nkcal', ha='center', va='center',
                fontsize=10, fontweight='bold', color='#2c3e50')

        st.pyplot(fig3, width='stretch')

    # Actionable Recommendations
    st.subheader("🎯 Recommendations")

    recommendations = []

    if prediction < 2000:
        recommendations.extend([
            "🚶 **Increase Daily Movement**: Aim for 8,000+ steps per day",
            "🏋️ **Add Strength Training**: Build muscle to boost metabolism",
            "🥗 **Focus on Protein**: Support muscle maintenance and recovery"
        ])
    elif prediction < 2500:
        recommendations.extend([
            "✅ **Maintain Current Activity**: You're at a healthy level",
            "🏃 **Add Variety**: Mix cardio and strength training",
            "📊 **Track Progress**: Monitor changes in energy levels"
        ])
    else:
        recommendations.extend([
            "🔥 **High Performer**: Ensure adequate recovery time",
            "🍽️ **Fuel Properly**: High activity requires quality nutrition",
            "💧 **Stay Hydrated**: Important for high activity levels"
        ])

    for rec in recommendations:
        st.success(rec)

# Footer
st.markdown("---")

