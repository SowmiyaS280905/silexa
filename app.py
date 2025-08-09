from flask import Flask, render_template, request, jsonify, Response
import numpy as np
import joblib
import pandas as pd
import json
import os
import csv
from datetime import datetime

app = Flask(__name__)

# Global variables
model = None
labels = []

def initialize_model():
    """Initialize the ML model - EXACTLY like detect_sign.py"""
    global model, labels

    try:
        # Load the trained model (same as detect_sign.py)
        if os.path.exists('model.pkl'):
            model = joblib.load('model.pkl')
            print("✅ Model loaded successfully")
            print(f"Model type: {type(model)}")
        else:
            print("❌ model.pkl not found!")
            model = None

        # Load labels from training data (same as detect_sign.py)
        if os.path.exists('gestures.csv'):
            data = pd.read_csv('gestures.csv', header=None)
            labels = sorted(data.iloc[:, -1].unique())
            print(f"✅ Labels loaded ({len(labels)} total): {labels}")
        else:
            print("❌ gestures.csv not found!")
            labels = []

    except Exception as e:
        print(f"❌ Error initializing: {e}")
        model = None
        labels = []

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/collect')
def collect_data():
    """Data collection page"""
    return render_template('collect.html')

@app.route('/detect')
def real_time_detection():
    """Real-time detection page"""
    return render_template('detect.html', labels=labels)

@app.route('/api/predict', methods=['POST'])
def predict_gesture():
    """API endpoint for gesture prediction - EXACTLY like detect_sign.py"""
    try:
        data = request.get_json()
        landmarks = data.get('landmarks', [])

        print(f"🔍 API Debug - Received {len(landmarks)} landmarks")

        if len(landmarks) == 42:
            if model is not None:
                # EXACT same process as detect_sign.py line 74:
                # prediction = model.predict([landmarks])[0]
                prediction_array = model.predict([landmarks])
                prediction = prediction_array[0]

                print(f"🧠 Model prediction: '{prediction}' (type: {type(prediction)})")
                print(f"📊 Available labels: {labels}")

                return jsonify({
                    'success': True,
                    'prediction': str(prediction),  # Ensure string
                    'confidence': 'high',
                    'debug_info': {
                        'landmarks_count': len(landmarks),
                        'model_type': str(type(model)),
                        'prediction_type': str(type(prediction))
                    }
                })
            else:
                print("❌ Model is None - not loaded properly")
                return jsonify({
                    'success': False,
                    'error': 'Model not loaded - check model.pkl file'
                })
        else:
            print(f"❌ Wrong landmark count: {len(landmarks)}, expected 42")
            return jsonify({
                'success': False,
                'error': f'Invalid landmarks count: {len(landmarks)}, expected 42'
            })

    except Exception as e:
        print(f"❌ Prediction error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/save_gesture', methods=['POST'])
def save_gesture():
    """API endpoint to save gesture data"""
    try:
        data = request.get_json()
        landmarks = data.get('landmarks', [])
        label = data.get('label', '')
        
        if len(landmarks) == 42 and label:
            # Save to CSV
            csv_file = 'gestures.csv'
            with open(csv_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(landmarks + [label])
            
            return jsonify({
                'success': True,
                'message': f'Gesture "{label}" saved successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid data'
            })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/retrain', methods=['POST'])
def retrain_model():
    """API endpoint to retrain the model"""
    try:
        # Import training logic
        from sklearn.model_selection import train_test_split
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import classification_report
        
        # Load data
        data = pd.read_csv('gestures.csv', header=None)
        X = data.iloc[:, :-1]
        y = data.iloc[:, -1]
        
        # Split and train
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        clf = RandomForestClassifier()
        clf.fit(X_train, y_train)
        
        # Evaluate
        y_pred = clf.predict(X_test)
        accuracy = (y_pred == y_test).mean()
        
        # Save model
        joblib.dump(clf, 'model.pkl')
        
        # Reload the model globally
        global model, labels
        model = clf
        labels = sorted(y.unique())
        
        return jsonify({
            'success': True,
            'message': 'Model retrained successfully',
            'accuracy': float(accuracy),
            'total_samples': len(data)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    # Initialize the model
    print("🚀 Starting SILEXA Web Application...")
    initialize_model()

    # Run the Flask app
    print("🌐 Starting Flask server on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
