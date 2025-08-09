"""
Test Flask API with exact same data as desktop version
"""
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import json

app = Flask(__name__)

# Load model and data (same as detect_sign.py)
print("🔍 Loading model and data...")
model = joblib.load('model.pkl')
data = pd.read_csv('gestures.csv', header=None)
labels = sorted(data.iloc[:, -1].unique())

print(f"✅ Model loaded: {type(model)}")
print(f"✅ Labels: {labels}")
print(f"✅ Data shape: {data.shape}")

@app.route('/')
def home():
    return f'''
    <h1>🧪 SILEXA API Test</h1>
    <p>Model: {type(model)}</p>
    <p>Labels: {labels}</p>
    <p>Data shape: {data.shape}</p>
    
    <h2>Test with Sample Data</h2>
    <button onclick="testSample()">Test Sample Prediction</button>
    <div id="result"></div>
    
    <script>
    async function testSample() {{
        try {{
            const response = await fetch('/test_sample');
            const data = await response.json();
            document.getElementById('result').innerHTML = 
                '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
        }} catch (error) {{
            document.getElementById('result').innerHTML = 
                '<p style="color: red;">Error: ' + error + '</p>';
        }}
    }}
    </script>
    '''

@app.route('/test_sample')
def test_sample():
    """Test with sample data from CSV"""
    try:
        # Get first row from CSV (same data as desktop test)
        sample_landmarks = data.iloc[0, :-1].values.tolist()
        expected_label = data.iloc[0, -1]
        
        # Test prediction (exact same as detect_sign.py)
        prediction_array = model.predict([sample_landmarks])
        prediction = prediction_array[0]
        
        return jsonify({
            'success': True,
            'sample_landmarks_length': len(sample_landmarks),
            'sample_landmarks_first_10': sample_landmarks[:10],
            'expected_label': expected_label,
            'prediction': prediction,
            'prediction_type': str(type(prediction)),
            'matches_expected': prediction == expected_label,
            'available_labels': labels
        })
        
    except Exception as e:
        import traceback
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        })

@app.route('/api/predict', methods=['POST'])
def predict_gesture():
    """Same API as main app but with more debugging"""
    try:
        data_json = request.get_json()
        landmarks = data_json.get('landmarks', [])
        
        print(f"🔍 Received landmarks: {len(landmarks)}")
        print(f"🔍 First 6 values: {landmarks[:6] if len(landmarks) >= 6 else landmarks}")
        
        if len(landmarks) == 42:
            # EXACT same prediction as detect_sign.py line 74
            prediction_array = model.predict([landmarks])
            prediction = prediction_array[0]
            
            print(f"🧠 Prediction: '{prediction}' (type: {type(prediction)})")
            
            return jsonify({
                'success': True,
                'prediction': str(prediction),
                'confidence': 'high',
                'debug': {
                    'landmarks_length': len(landmarks),
                    'landmarks_sample': landmarks[:6],
                    'prediction_type': str(type(prediction)),
                    'available_labels': labels
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Wrong landmarks count: {len(landmarks)}, expected 42'
            })
            
    except Exception as e:
        import traceback
        print(f"❌ Error: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        })

if __name__ == '__main__':
    print("🚀 Starting test API server...")
    print("🌐 Open http://localhost:5001 to test")
    app.run(debug=True, host='localhost', port=5001)
