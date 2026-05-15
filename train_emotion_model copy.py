import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import make_pipeline
import joblib

# Dummy training data (replace with real features if available)
X = np.random.rand(200, 40)  # 200 samples, 40 features (MFCCs)
y = np.random.choice(['happy', 'sad', 'angry', 'neutral'], 200)

# Encode labels
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Train SVM model
model = make_pipeline(StandardScaler(), SVC(kernel='rbf', probability=True))
model.fit(X, y_encoded)

# Save model and encoder
joblib.dump(model, 'emotion_model.joblib')
joblib.dump(encoder, 'label_encoder.joblib')

print("✅ Emotion model and encoder saved successfully!")
