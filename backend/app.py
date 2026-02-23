from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# Get absolute path of the current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, '..', 'models')

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
        if probability > 0.7:
            risk_level = "High"
        elif probability > 0.3:
            risk_level = "Medium"
            
        return jsonify({
            'prediction': int(prediction[0]),
            'probability': float(probability),
            'risk_level': risk_level
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/results', methods=['GET'])
def get_results():
    return jsonify(model_results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
