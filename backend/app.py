from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import os

app = Flask(__name__)
# Explicitly allow all origins for mobile/Vercel compatibility
CORS(app, resources={r"/*": {"origins": "*"}})

# Get absolute path of the current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Models are now inside the backend folder for safer deployment
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# Load the best model and scaler
with open(os.path.join(MODELS_DIR, 'heart_model.pkl'), 'rb') as f:
    model = pickle.load(f)

with open(os.path.join(MODELS_DIR, 'scaler.pkl'), 'rb') as f:
    scaler = pickle.load(f)

with open(os.path.join(MODELS_DIR, 'model_results.pkl'), 'rb') as f:
    model_results = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Features in order: age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal
        features = [
            float(data['age']),
            float(data['sex']),
            float(data['cp']),
            float(data['trestbps']),
            float(data['chol']),
            float(data['fbs']),
            float(data['restecg']),
            float(data['thalach']),
            float(data['exang']),
            float(data['oldpeak']),
            float(data['slope']),
            float(data['ca']),
            float(data['thal'])
        ]
        
        features_scaled = scaler.transform([features])
        prediction = model.predict(features_scaled)
        probability = model.predict_proba(features_scaled)[0][1]
        
        # Risk level logic
        risk_level = "Low"
        detailed_analysis = "Based on your parameters, no immediate major risk patterns were detected."
        
        if probability > 0.7:
            risk_level = "High"
            risks = []
            if float(data['cp']) > 0: risks.append("Potential Coronary Artery Disease (CAD) markers")
            if float(data['ca']) > 0: risks.append("Presence of major vessel narrowing")
            if float(data['oldpeak']) > 1.5: risks.append("Ischemic heart strain (ST depression)")
            if float(data['thalach']) < 120: risks.append("Reduced cardiac output/exercise capacity")
            detailed_analysis = "High risk factors detected: " + ", ".join(risks) if risks else "Generic high-risk cardiac profile detected."
        elif probability > 0.3:
            risk_level = "Medium"
            detailed_analysis = "Moderate risk patterns detected. Possible early signs of cardiovascular strain or high cholesterol influence."
            
        return jsonify({
            'prediction': int(prediction[0]),
            'probability': float(probability),
            'risk_level': risk_level,
            'detailed_analysis': detailed_analysis
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/results', methods=['GET'])
def get_results():
    return jsonify(model_results)

if __name__ == '__main__':
    app.run()
