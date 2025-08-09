"""
Debug script to compare desktop vs web processing
"""
import joblib
import pandas as pd
import numpy as np

def test_model_loading():
    """Test if model loads correctly"""
    try:
        model = joblib.load('model.pkl')
        print("✅ Model loaded successfully")
        print(f"Model type: {type(model)}")
        
        # Load labels
        data = pd.read_csv('gestures.csv', header=None)
        labels = sorted(data.iloc[:, -1].unique())
        print(f"✅ Labels: {labels}")
        
        # Test with sample data
        sample_landmarks = data.iloc[0, :-1].values  # First row, all columns except last
        print(f"Sample landmarks shape: {sample_landmarks.shape}")
        print(f"Sample landmarks (first 10): {sample_landmarks[:10]}")
        
        # Test prediction
        prediction = model.predict([sample_landmarks])
        print(f"Sample prediction: {prediction}")
        print(f"Prediction type: {type(prediction)}")
        print(f"Prediction[0]: {prediction[0]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_landmark_format():
    """Test landmark format from CSV"""
    try:
        data = pd.read_csv('gestures.csv', header=None)
        print(f"CSV shape: {data.shape}")
        print(f"First row: {data.iloc[0].values}")
        print(f"Last column (label): {data.iloc[0, -1]}")
        print(f"Feature columns: {data.shape[1] - 1}")
        
        # Check if landmarks are in correct format
        landmarks = data.iloc[0, :-1].values
        print(f"Landmarks length: {len(landmarks)}")
        print(f"Expected: 42, Got: {len(landmarks)}")
        
        if len(landmarks) == 42:
            print("✅ Landmark format is correct")
            # Show x,y pairs
            for i in range(0, min(10, len(landmarks)), 2):
                print(f"Point {i//2}: x={landmarks[i]:.3f}, y={landmarks[i+1]:.3f}")
        else:
            print("❌ Landmark format is incorrect")
            
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")

if __name__ == "__main__":
    print("🔍 SILEXA Debug - Desktop vs Web Comparison")
    print("=" * 50)
    
    print("\n1. Testing Model Loading:")
    test_model_loading()
    
    print("\n2. Testing Landmark Format:")
    test_landmark_format()
    
    print("\n3. Desktop detect_sign.py Process:")
    print("   - MediaPipe extracts 21 landmarks")
    print("   - Each landmark has x,y coordinates")
    print("   - landmarks.extend([lm.x, lm.y]) creates 42 values")
    print("   - model.predict([landmarks])[0] gets prediction")
    
    print("\n4. Web detect.html Process:")
    print("   - MediaPipe extracts 21 landmarks")
    print("   - landmarkArray.push(landmark.x, landmark.y)")
    print("   - Send to /api/predict")
    print("   - Flask: model.predict([landmarks])[0]")
    
    print("\n5. Check if processes are identical...")
