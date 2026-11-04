import sys
import joblib
import pandas as pd
from features import features

model = joblib.load("model.pkl")

def check(url):
    prob = model.predict_proba(pd.DataFrame([features(url)]))[0][1]
    verdict = "LIKELY PHISHING" if prob > 0.5 else "LOOKS LEGIT"
    print(f"{url}\n  -> {verdict} ({prob:.0%} phishing probability)")

if len(sys.argv) > 1:
    for u in sys.argv[1:]:
        check(u)
else:
    print("Type a URL and press Enter (blank line to quit)")
    while True:
        u = input("> ").strip()
        if not u:
            break
        check(u)