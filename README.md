# 🛡️ Phishing URL Detector

A machine learning web app that checks whether a URL looks like phishing, using only the structure of the link.

**Live demo:** https://isitsafe.streamlit.app

## How it works

1. Each URL is converted into 11 numeric features (see below).
2. A Random Forest classifier (100 trees) scores the features.
3. The Streamlit app shows the phishing probability and a verdict.

| Feature | What it captures |
|---|---|
| `length`, `host_length` | Long URLs and long hostnames are more suspicious |
| `dots`, `subdomains` | Many dots and subdomains often hide the real domain |
| `hyphens`, `digits`, `slashes` | Character patterns common in fake URLs |
| `at` | An `@` symbol can hide the real destination |
| `has_ip` | Raw IP address used instead of a domain |
| `https` | Whether the link uses HTTPS |
| `bad_words` | Words like `login`, `verify`, `secure`, `bank` |

## Results

Trained on a 50,000-URL sample, split 80/20 and tested on 10,000 unseen URLs.

| Class | Precision | Recall | F1 |
|---|---|---|---|
| Legitimate | 0.90 | 0.94 | 0.92 |
| Phishing | 0.82 | 0.73 | 0.77 |

**Overall accuracy: 88%**

## Model comparison

All models trained on the same 40,000 URLs and tested on the same 10,000 unseen URLs (phishing class metrics).

| Model | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Logistic Regression | 0.792 | 0.810 | 0.354 | 0.493 |
| **Random Forest** | **0.878** | 0.824 | **0.728** | **0.773** |
| Gradient Boosting | 0.866 | 0.850 | 0.646 | 0.734 |

Random Forest was chosen for the app: best accuracy, recall and F1. Logistic Regression misses most phishing links because a linear boundary can't capture non-linear URL patterns.

## Dataset

[Phishing Site URLs](https://www.kaggle.com/datasets/taruntiwarihp/phishing-site-urls) from Kaggle (about 549,000 URLs labeled good or bad).

## Run it locally

```bash
git clone https://github.com/mavirudra/phishing-url-detector.git
cd phishing-url-detector
pip install -r requirements.txt
streamlit run app.py
```

To retrain the model, download the dataset, save it as `phishing.csv` in the project folder, and run:

```bash
python train.py
```

## Project structure

```
app.py             Streamlit web app
features.py        URL feature extraction
train.py           Model training and evaluation
model.pkl          Trained model
requirements.txt   Dependencies
```

## Limitations

- It only looks at the URL text, not page content, domain age, or reputation.
- Phishing recall is 73%, so it misses about 1 in 4 phishing links. Don't rely on it as your only protection.
- Trained on a sample of the data, so more data and features could improve it.

## Roadmap

- [ ] Compare Logistic Regression, Random Forest and XGBoost
- [ ] Add URL entropy and special-character features
- [ ] Train on the full dataset

## License

MIT
