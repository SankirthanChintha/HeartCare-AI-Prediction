# Heart Disease Prediction Using Machine Learning

## Abstract
Heart disease is one of the leading causes of mortality worldwide, and early detection plays a crucial role in reducing complications and improving survival rates. This project aims to develop an intelligent system that predicts the likelihood of heart disease based on patient medical data. This system utilizes machine learning algorithms to analyze various health parameters such as age, gender, chest pain type, blood pressure, cholesterol levels, fasting blood sugar, electrocardiogram (ECG) results, maximum heart rate, and other clinical attributes.

## Features
- **Data Preprocessing**: Handles missing values, normalizes data, and selects important features.
- **Multiple Models**: Implements and compares Logistic Regression, Decision Tree, Random Forest, SVM, and KNN.
- **Advanced UI**: Premium medical dashboard for risk assessment.
- **Risk Analysis**: Categorizes risk into High, Medium, and Low levels.

## Tech Stack
- **Backend**: Python (Flask)
- **Machine Learning**: Scikit-Learn, Pandas, Numpy
- **Frontend**: HTML5, CSS3 (Premium UI), JavaScript (ES6+)

## Project Structure
- `backend/`: API and Model Training scripts.
- `frontend/`: Dashboard interface.
- `data/`: UCI Heart Disease Dataset.
- `models/`: Saved ML models and scalers.

## How to Run
1. Install dependencies:
   ```bash
   pip install flask flask-cors pandas scikit-learn numpy
   ```
2. Train the models (already done, but can be rerun):
   ```bash
   python backend/train_model.py
   ```
3. Start the server:
   ```bash
   python run.py
   ```
4. Open `frontend/index.html` in your browser.

## Keywords
Heart Disease Prediction, Machine Learning, Healthcare Analytics, Classification Algorithms, Early Diagnosis.
