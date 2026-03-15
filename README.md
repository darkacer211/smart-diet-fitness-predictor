# Smart Diet & Fitness Predictor

A Streamlit web application that predicts daily calorie burn based on lifestyle and activity patterns using machine learning.

## Features

- **Calorie Prediction**: Estimate daily calories burned based on age, BMI, gender, and activity levels
- **Interactive Dashboard**: Clean, professional interface with visual charts and insights
- **Personalized Insights**: Get tailored recommendations based on your activity level
- **Visual Analytics**: View your results with interactive charts and breakdowns

## Project Structure

```
├── app.py                 # Main Streamlit application
├── data/                  # Dataset files
│   └── calories.csv      # Training data
├── model/                 # Trained machine learning models
│   └── calorie_model.pkl # Random Forest model for predictions
├── notebooks/            # Jupyter notebooks for analysis
│   └── exploration.ipynb # Data exploration and model development
├── src/                  # Source code (currently empty)
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd "Health prediction proj"
```

2. Create a virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`.

## Input Features

The model predicts calories burned based on:
- **Age**: User's age in years
- **BMI**: Body Mass Index
- **Active Hours**: Daily hours spent in physical activities
- **Workout Hours**: Structured exercise time per day
- **Gender**: Male or Female
- **Workout Type**: None, Cardio, Strength, or Mixed

## Model Details

- **Algorithm**: Random Forest Regressor
- **Features**: 8 input features with proper encoding
- **Training Data**: Historical calorie burn data
- **Performance**: Trained to predict daily energy expenditure

## Development

### Prerequisites
- Python 3.8+
- Streamlit
- scikit-learn
- pandas
- matplotlib

### Adding New Features
1. Update the input form in `app.py`
2. Modify feature encoding if needed
3. Retrain the model if new features are added
4. Update the visualization components

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes. Please check local regulations for health-related applications.

## Disclaimer

This tool provides estimates only and should not replace professional medical advice. Consult healthcare professionals for personalized nutrition and fitness guidance.
