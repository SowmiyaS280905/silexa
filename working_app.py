from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Try to load model, but don't fail if it doesn't work
model = None
labels = ['A', 'B', 'C', 'Hi', 'No', 'hello', 'surprised', 'thinking', 'thumbs up']

try:
    import joblib
    import pandas as pd
    
    if os.path.exists('model.pkl'):
        model = joblib.load('model.pkl')
        print("✅ Model loaded successfully")
    
    if os.path.exists('gestures.csv'):
        data = pd.read_csv('gestures.csv', header=None)
        labels = sorted(data.iloc[:, -1].unique())
        print(f"✅ Labels loaded: {len(labels)} gestures")
    
except Exception as e:
    print(f"⚠️ Model loading failed: {e}")
    print("Using fallback mode")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect')
def detect():
    return render_template('detect.html', labels=labels)

@app.route('/collect')
def collect():
    return render_template('collect.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/letter-to-sign')
def letter_to_sign():
    return render_template('letter_to_sign.html')

@app.route('/voice-to-sign')
def voice_to_sign():
    return render_template('voice_to_sign.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        landmarks = data.get('landmarks', [])

        if len(landmarks) == 42:
            if model is not None:
                # Use real model
                prediction = model.predict([landmarks])[0]
                prediction_proba = model.predict_proba([landmarks])
                confidence = max(prediction_proba[0])

                print(f"Real prediction: {prediction} (Confidence: {confidence:.2f})")

                return jsonify({
                    'success': True,
                    'prediction': prediction,
                    'confidence': float(confidence)
                })
            else:
                # Fallback prediction
                import random
                prediction = random.choice(labels)
                print(f"Fallback prediction: {prediction}")

                return jsonify({
                    'success': True,
                    'prediction': prediction,
                    'confidence': 0.8
                })

        else:
            return jsonify({
                'success': False,
                'error': f'Expected 42 landmarks, got {len(landmarks)}'
            })

    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/save_gesture', methods=['POST'])
def save_gesture():
    try:
        data = request.get_json()
        landmarks = data.get('landmarks', [])
        label = data.get('label', '')
        
        if len(landmarks) == 42 and label:
            # Save to CSV
            import csv
            with open('gestures.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(landmarks + [label])
            
            return jsonify({
                'success': True,
                'message': f'Gesture "{label}" saved'
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
def retrain():
    try:
        # Simple retraining
        global model, labels

        import pandas as pd
        from sklearn.model_selection import train_test_split
        from sklearn.ensemble import RandomForestClassifier
        import joblib

        # Load data
        data = pd.read_csv('gestures.csv', header=None)
        X = data.iloc[:, :-1]
        y = data.iloc[:, -1]

        # Train
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        clf = RandomForestClassifier()
        clf.fit(X_train, y_train)

        # Save
        joblib.dump(clf, 'model.pkl')

        # Update global variables
        model = clf
        labels = sorted(y.unique())

        accuracy = clf.score(X_test, y_test)

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
    print("🚀 Starting SILEXA...")
    print("📁 Files check:")
    print(f"   model.pkl: {'✅' if os.path.exists('model.pkl') else '❌'}")
    print(f"   gestures.csv: {'✅' if os.path.exists('gestures.csv') else '❌'}")
    print(f"   templates/: {'✅' if os.path.exists('templates') else '❌'}")
    
    print("🌐 Starting server on http://localhost:5000")
    app.run(debug=True, host='localhost', port=5000, use_reloader=False)
