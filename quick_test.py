print("🔍 SILEXA Debug Test")
print("=" * 30)

# Test 1: Basic Python
print("✅ Python working")

# Test 2: Flask import
try:
    from flask import Flask
    print("✅ Flask import OK")
except Exception as e:
    print(f"❌ Flask error: {e}")

# Test 3: Model files
import os
print(f"📁 model.pkl exists: {os.path.exists('model.pkl')}")
print(f"📁 gestures.csv exists: {os.path.exists('gestures.csv')}")
print(f"📁 templates exists: {os.path.exists('templates')}")

# Test 4: Model loading
try:
    import joblib
    import pandas as pd
    
    model = joblib.load('model.pkl')
    data = pd.read_csv('gestures.csv', header=None)
    labels = sorted(data.iloc[:, -1].unique())
    
    print(f"✅ Model loaded: {type(model)}")
    print(f"✅ Data loaded: {data.shape}")
    print(f"✅ Labels: {len(labels)} gestures")
    print(f"   First 5 labels: {labels[:5]}")
    
except Exception as e:
    print(f"❌ Model loading error: {e}")

# Test 5: Simple Flask app
print("\n🚀 Starting simple Flask test...")

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>🎉 SILEXA is working!</h1><p>Flask server is running correctly.</p>"

if __name__ == '__main__':
    print("🌐 Server starting at http://localhost:5000")
    app.run(debug=False, host='localhost', port=5000)
