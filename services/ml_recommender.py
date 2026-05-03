import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib, os, json

df = pd.read_csv("dataset/recommendation.csv")

mapping = {
    "room_type": {"bedroom":0, "living_room":1, "office":2, "guest_room":3},
    "style": {"modern":0, "luxury":1, "minimal":2, "rustic":3},
    "color_family": {"light":0, "medium":1, "dark":2}
}

# =========================
# 🔥 FEATURES (X)
# =========================
X = []

# =========================
# 🔥 TARGET (y) → STILL STYLE
# =========================
y = []

for _, row in df.iterrows():
    X.append([
        mapping["room_type"][row["room_type"]],
        mapping["color_family"][row["color_family"]]
    ])  # ❗ IMPORTANT: style removed from input

    y.append(mapping["style"][row["style"]])

# =========================
# TRAIN / TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# MODEL
# =========================
model = KNeighborsClassifier(n_neighbors=7)
model.fit(X_train, y_train)

os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/recommender.pkl")

# =========================
# EVALUATION
# =========================
preds = model.predict(X_test)

acc = accuracy_score(y_test, preds)
precision = precision_score(y_test, preds, average='macro', zero_division=0)
recall = recall_score(y_test, preds, average='macro', zero_division=0)
f1 = f1_score(y_test, preds, average='macro', zero_division=0)

print("\n🎯 REALISTIC RECOMMENDER METRICS")
print("Accuracy:", acc)
print("Precision:", precision)
print("Recall:", recall)
print("F1:", f1)

# =========================
# SAVE METRICS
# =========================
os.makedirs("analytics", exist_ok=True)

with open("analytics/recommender_metrics.json", "w") as f:
    json.dump({
        "accuracy": float(acc),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1),
        "dataset_size": len(X)
    }, f)

print("✅ Recommender FIXED PROPERLY")
