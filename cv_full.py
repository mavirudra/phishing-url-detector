import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from features import features

df = pd.read_csv("phishing.csv")
df = df.drop_duplicates(subset="URL").reset_index(drop=True)
y = (df["Label"].str.lower() == "bad").astype(int)
X = pd.DataFrame([features(u) for u in df["URL"]])

model = RandomForestClassifier(
    n_estimators=100, min_samples_leaf=5, n_jobs=-1, random_state=42
)
folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
pred = cross_val_predict(model, X, y, cv=folds)

print(classification_report(y, pred))