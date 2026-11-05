import os
import time
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from features import features

t0 = time.time()
df = pd.read_csv("phishing.csv")
print("rows:", len(df))
df = df.drop_duplicates(subset="URL").reset_index(drop=True)
print("rows after removing duplicates:", len(df))

y = (df["Label"].str.lower() == "bad").astype(int)
X = pd.DataFrame([features(u) for u in df["URL"]])
print("features done in", round(time.time() - t0), "seconds")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=100, min_samples_leaf=5, n_jobs=-1, random_state=42
)
model.fit(X_train, y_train)
print("training done in", round(time.time() - t0), "seconds")

print(classification_report(y_test, model.predict(X_test)))
joblib.dump(model, "model.pkl", compress=3)
print("model.pkl size (MB):", round(os.path.getsize("model.pkl") / 1e6, 1))
