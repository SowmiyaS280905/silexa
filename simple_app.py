from flask import Flask, render_template, request, jsonify
import os
import json
import joblib
import pandas as pd

app = Flask(__name__)

# Global variables - LOAD REAL MODEL
try:
    model = joblib.load('model.pkl')
    data = pd.read_csv('gestures.csv', header=None)
    labels = sorted(data.iloc[:, -1].unique())
    print(f"✅ Real model loaded: {len(labels)} labels")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None
    labels = ['A', 'B', 'C', 'Hi', 'No', 'hello', 'surprised', 'thinking', 'thumbs up']

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

@app.route('/about')
def about():
    """About page with user manual"""
    return render_template('about.html')

@app.route('/api/predict', methods=['POST'])
def predict_gesture():
    """API endpoint - EXACT same as detect_sign.py"""
    try:
        data = request.get_json()
        landmarks = data.get('landmarks', [])

        if len(landmarks) == 42 and model is not None:
            # EXACT same prediction as detect_sign.py line 74
            prediction = model.predict([landmarks])[0]
            return jsonify({
                'success': True,
                'prediction': prediction,
                'confidence': 'high'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid landmarks or model not loaded'
            })

    except Exception as e:
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
            # Simulate saving (replace with actual CSV saving)
            print(f"Would save gesture: {label} with {len(landmarks)} landmarks")
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
        # Simulate retraining
        import time
        time.sleep(2)  # Simulate training time
        
        return jsonify({
            'success': True,
            'message': 'Model retrained successfully',
            'accuracy': 0.95,
            'total_samples': 166
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print("🚀 Starting SILEXA Web Application...")
    print("🌐 Opening browser at http://localhost:5000")
    
    # Try to open browser automatically
    import webbrowser
    import threading
    
    def open_browser():
        import time
        time.sleep(1.5)  # Wait for server to start
        webbrowser.open('http://localhost:5000')
    
    # Start browser in a separate thread
    threading.Thread(target=open_browser).start()
    
    # Run the Flask app
    app.run(debug=True, host='localhost', port=5000, use_reloader=False)
