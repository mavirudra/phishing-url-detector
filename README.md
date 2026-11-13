# 🛡️ Phishing URL Detector

A machine learning web app that checks whether a URL looks like phishing, using only the structure of the link.

**Live demo:** https://isitsafe.streamlit.app

## How it works

1. Each URL is converted into 20 numeric features (see below).
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
| `entropy`, `host_entropy` | How random the characters look; random hostnames are common in phishing |
| `question`, `equals`, `ampersands`, `percent`, `underscores`, `special_total`, `special_ratio` | Counts of `?` `=` `&` `%` `_` plus the total and share of special characters |

## Results

Trained on all 507,195 unique URLs (duplicates removed), split 80/20 and tested on 101,439 unseen URLs.

| Class | Precision | Recall | F1 |
|---|---|---|---|
| Legitimate | 0.92 | 0.98 | 0.95 |
| Phishing | 0.90 | 0.71 | 0.79 |

**Overall accuracy: 92%**

## Model comparison

All models use the same 20 features, the same training split and the same 101,439 unseen test URLs (phishing class metrics).

| Model | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Logistic Regression | 0.844 | 0.827 | 0.388 | 0.528 |
| **Random Forest** | **0.917** | **0.903** | **0.707** | **0.793** |
| Gradient Boosting | 0.899 | 0.869 | 0.650 | 0.743 |

Random Forest wins on every metric, so it is the model in the app.

## Dataset

[Phishing Site URLs](https://www.kaggle.com/datasets/taruntiwarihp/phishing-site-urls) from Kaggle (about 549,000 URLs labeled good or bad).

Duplicate URLs were removed (549,346 rows became 507,195 unique URLs).

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

To rerun the model comparison, run `python compare.py`.

## Command-line usage

Check a URL without the web app:

```bash
python check.py http://paypal-login.verify-account.xyz/update
```

Run `python check.py` with no arguments for interactive mode.

## Project structure

```
app.py             Streamlit web app
features.py        URL feature extraction
check.py           Command-line checker
train.py           Model training and evaluation
compare.py         Model comparison
model.pkl          Trained model
results.csv        Model comparison results
requirements.txt   Dependencies
```

## Limitations

- It only looks at the URL text, not page content, domain age, or reputation.
- Phishing recall is 71%, so it misses about 3 in 10 phishing links.
- It was trained on a single dataset, so results may differ on URLs from other sources.

## Roadmap

- [x] Compare Logistic Regression, Random Forest and Gradient Boosting
- [x] Add URL entropy features
- [x] Add special-character features
- [x] Train on the full dataset
- [ ] Try XGBoost
- [ ] Add domain-age checks
- [ ] Build a browser extension

## License

MIT
