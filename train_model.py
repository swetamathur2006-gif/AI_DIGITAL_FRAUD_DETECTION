import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import joblib

# Load the dataset
data = pd.read_csv("dataset/transactions.csv")

# Separate features and target
X = data[
    [
        "amount",
        "hour",
        "new_device",
        "international",
        "location_changed"
    ]
]

y = data["fraud"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create the AI model
model = DecisionTreeClassifier(random_state=42)

# Train the model
model.fit(X_train, y_train)

# Check model accuracy
accuracy = model.score(X_test, y_test)

print("Model training complete!")
print("Model Accuracy:", accuracy)

# Save the trained model
joblib.dump(model, "model/fraud_model.pkl")

print("Fraud detection model saved successfully!")