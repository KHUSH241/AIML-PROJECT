# 🧠 AI Diagnostic System — Fever & Hypothermia Classifier

An intelligent health diagnostic tool that classifies fever and hypothermia based on body temperature and symptom duration. Built using a hybrid AI approach combining **Machine Learning** (Decision Tree Classifier) and a **Prolog Expert System**, wrapped in a modern **Tkinter GUI**.

---

## 📌 Problem Statement

Fever and hypothermia are among the most common yet frequently mismanaged health conditions. Delayed or incorrect self-diagnosis can lead to serious complications. This project addresses the question:

> *Can an intelligent system use minimal inputs — body temperature and symptom duration — to assess health risk and provide actionable diagnostic guidance without requiring a doctor?*

---

## ✨ Features

- 🤖 **ML Risk Assessment** — Decision Tree Classifier predicts Low / Medium / High risk
- 🧠 **Prolog Expert System** — Rule-based diagnosis engine identifies conditions and recommends treatment
- 📊 **Live Temperature Gauge** — Real-time matplotlib chart showing temperature against health zones
- 🖥️ **Modern Dark-Themed GUI** — Built with Tkinter, responsive and intuitive
- ⚡ **Auto Model Training** — ML model is trained automatically on first launch if not present

---

## 🏗️ Project Structure

```
ai-diagnostic-system/
│
├── main.py                  # Main GUI application (entry point)
├── classifier_model.py      # ML model training and prediction
├── rules.pl                 # Prolog knowledge base (diagnosis + treatment rules)
├── symptoms_data.csv        # Training dataset
├── risk_classifier.pkl      # Trained model (auto-generated on first run)
└── README.md
```

---

## 🔧 Setup & Installation

### Prerequisites

- Python 3.8 or higher
- SWI-Prolog installed on your system

### Install SWI-Prolog

| OS | Command |
|----|---------|
| Ubuntu/Debian | `sudo apt install swi-prolog` |
| macOS | `brew install swi-prolog` |
| Windows | Download from [https://www.swi-prolog.org/download](https://www.swi-prolog.org/download) |

### Install Python Dependencies

```bash
pip install pyswip scikit-learn joblib matplotlib numpy
```

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-diagnostic-system.git
cd ai-diagnostic-system
```

---

## 🚀 How to Run

```bash
python app.py
```

On first launch, the ML model will be trained automatically from `symptoms_data.csv` and saved as `risk_classifier.pkl`.

---

## 🖥️ How to Use

1. Enter **Body Temperature** in °C (e.g., `38.5`)
2. Enter **Duration** in days (e.g., `3`)
3. Click **⚡ Run AI Analysis**
4. The system will display:
   - **ML Risk Level** — Low / Medium / High (colour coded)
   - **Diagnosis** — e.g., Severe Infection, Hypothermia, Healthy
   - **Treatment Recommendation** — Actionable advice
   - **Temperature Gauge** — Visual chart showing your temperature in context

---

## 🧪 Example Outputs

| Temperature | Duration | Risk  | Diagnosis        |
|-------------|----------|-------|------------------|
| 40.5°C      | 6 days   | High  | Severe Infection |
| 38.5°C      | 3 days   | Medium| Acute Infection  |
| 36.5°C      | 1 day    | Low   | Healthy          |
| 34.0°C      | 2 days   | High  | Hypothermia      |

---

## 🤖 How It Works

### Machine Learning (classifier_model.py)
- Trains a **Decision Tree Classifier** on labelled temperature + duration data
- Predicts risk level: **Low**, **Medium**, or **High**
- Model is serialised with `joblib` for persistence across sessions
- Extreme hypothermia (<32°C) is hardcoded as High risk

### Prolog Expert System (rules.pl)
- Temperature and duration are converted to symbolic facts (`symptom/2`)
- Inference rules derive the diagnosis (e.g., `severe_infection`, `hypothermia`)
- Matched treatment text is returned alongside the diagnosis
- Facts are retracted and re-asserted for each query (stateless per query)

### GUI (main.py)
- Dark-themed Tkinter interface
- Matplotlib chart embedded inside the window for live temperature visualisation
- Colour-coded result labels (green = safe, yellow = moderate, red = danger)

---

## 📊 Dataset Format (symptoms_data.csv)

```
temperature,duration,risk
40.2,6,High
38.1,3,Medium
36.5,1,Low
34.0,4,High
...
```

---

## 🔮 Future Improvements

- Add more input features (heart rate, SpO2, blood pressure)
- Upgrade to Random Forest for better accuracy
- Deploy as a web app with Flask + React frontend
- Add multilingual support

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 👤 Author

Developed as a BYOP (Bring Your Own Project) submission for the Artificial Intelligence & Machine Learning course.
