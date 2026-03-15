# Smart Diet & Fitness Predictor

A Streamlit app that predicts daily calorie burn from lifestyle and workout habits.

## 🚀 Features

- **Calorie Prediction** – Estimate daily calories burned using age, BMI, activity, and workout data.
- **Interactive Dashboard** – Clean UI built with Streamlit.
- **Personalized Insights** – Practical tips based on your activity level.
- **Visual Analytics** – Charts and breakdowns to help you understand the results.

## 📁 Project Structure

```
smart-diet-fitness-predictor
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── calories.csv
├── model/
│   └── calorie_model.pkl
└── notebooks/
    └── exploration.ipynb
```

## 🛠️ Setup

### 1) Clone the repository

```bash
git clone https://github.com/darkacer211/smart-diet-fitness-predictor.git
cd smart-diet-fitness-predictor
```

### 2) Create a virtual environment

```bash
python -m venv venv
```

Activate it:

- **Windows:** `venv\Scripts\activate`
- **macOS / Linux:** `source venv/bin/activate`

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Run the App

```bash
streamlit run app.py
```

Then open:

```
http://localhost:8501
```

## 🧠 Model Details

- **Algorithm:** Random Forest Regressor
- **Inputs:** Age, BMI, Active Hours, Workout Hours, Gender, Workout Type
- **Output:** Estimated daily calories burned

## ⚠️ Disclaimer

This tool is for educational purposes only and should not replace professional medical advice.