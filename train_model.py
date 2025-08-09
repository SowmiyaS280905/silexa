import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import matplotlib.pyplot as plt

# Load data (CSV has no headers, last column is the label)
data = pd.read_csv('gestures.csv', header=None)
X = data.iloc[:, :-1]  # All columns except the last one (features)
y = data.iloc[:, -1]   # Last column (labels)

# Split data into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define hyperparameter grid for Random Forest
param_dist = {
    "n_estimators": [100, 200, 300],
    "max_depth": [10, 20, None],
    "min_samples_split": [2, 5],
    "min_samples_leaf": [1, 2],
    "bootstrap": [True, False],
    "class_weight": ['balanced']
}

# Initialize base model
rf = RandomForestClassifier(random_state=42)

# Use RandomizedSearchCV to find the best model
clf = RandomizedSearchCV(rf, param_distributions=param_dist, n_iter=10, cv=3, verbose=1, n_jobs=-1)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

# Cross-validation scores
cv_scores = cross_val_score(clf.best_estimator_, X, y, cv=5)
print(f"\nCross-validation scores: {cv_scores}")
print(f"Mean CV accuracy: {cv_scores.mean():.2f}")

# Print dataset info
print(f"\nDataset Info:")
print(f"Total samples: {len(data)}")
print(f"Features: {X.shape[1]}")
print(f"Training samples: {len(X_train)}")
print(f"Test samples: {len(X_test)}")
print(f"Unique labels: {sorted(y.unique())}")

# Save best model
joblib.dump(clf.best_estimator_, 'model.pkl')
print("✅ Model saved to model.pkl")

# Optional: Plot feature importance
importances = clf.best_estimator_.feature_importances_
plt.figure(figsize=(10, 4))
plt.title("Feature Importances")
plt.bar(range(len(importances)), importances)
plt.xlabel("Feature Index")
plt.ylabel("Importance")
plt.tight_layout()
print("✅ Script completed.")
exit()
