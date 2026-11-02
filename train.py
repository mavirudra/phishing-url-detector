import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from features import features

df = pd.read_csv("phishing.csv")
df = df.sample(50000, random_state=42)
y = (df["Label"].str.lower() == "bad").astype(int)
X = pd.DataFrame([features(u) for u in df["URL"]])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(n_estimators=100, n_jobs=2, random_state=42)
model.fit(X_train, y_train)

print(classification_report(y_test, model.predict(X_test)))
joblib.dump(model, "model.pkl", compress=3)
print("Saved model.pkl")