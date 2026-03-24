# 🧠 AI Diagnostic System — Fever & Hypothermia Classifier

An intelligent health diagnostic tool that classifies fever and hypothermia based on body temperature and symptom duration. Built using a **hybrid AI approach** combining **Machine Learning** (Decision Tree Classifier) and a **Prolog Expert System**, with a fully interactive **CLI interface**.

---

## 📌 Problem Statement

Fever and hypothermia are among the most common yet frequently mismanaged health conditions. Delayed or incorrect self-diagnosis can lead to serious complications. This project addresses the question:

> *Can an intelligent system use minimal inputs — body temperature and symptom duration — to assess health risk and provide actionable diagnostic guidance without requiring a doctor?*

---

## ✨ Features

- 🤖 **ML Risk Assessment** — Decision Tree Classifier predicts Low / Medium / High risk
- 🧠 **Prolog Expert System** — Rule-based diagnosis engine covering 6 clinical conditions
- 🖥️ **Full CLI Interface** — Interactive terminal application with commands, history, and help
- 📊 **ASCII Temperature Gauge** — Colour-coded terminal visual showing temperature zones
- ⚡ **Auto Model Training** — ML model trains automatically on first run if not present
- 🗂️ **Session History** — View all diagnoses made during the current session
- 🎨 **Bonus GUI Version** — Dark-themed Tkinter + matplotlib interface (optional)

---

## 🏗️ Project Structure

```
AIML-PROJECT/
│
├── app_cli.py          # PRIMARY — CLI application (run this)
├── app.py               # BONUS  — GUI version (optional)
├── classifier_model.py  # ML model training and prediction
├── rules.pl             # Prolog knowledge base (diagnosis + treatment rules)
├── risk_classifier.pkl  # Trained model (auto-generated on first run)
├── symptoms_data.csv    # Training dataset (190 rows)
├── requirements.txt     # Python dependencies
└── README.md
```
---

## 🔧 Setup & Installation

### Prerequisites

- Python 3.8 or higher
- SWI-Prolog installed on your system

### Step 1 — Install SWI-Prolog

| OS | Command |
|----|---------|
| Ubuntu/Debian | `sudo apt install swi-prolog` |
| macOS | `brew install swi-prolog` |
| Windows | Download from [https://www.swi-prolog.org/download](https://www.swi-prolog.org/download) |

### Step 2 — Clone the Repository

```bash
git clone https://github.com/KHUSH241/AIML-PROJECT.git
cd AIML-PROJECT
```

### Step 3 — Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run (CLI — Primary)

```bash
python app_cli.py
```

On first launch, the ML model will be trained automatically from `symptoms_data.csv` and saved as `risk_classifier.pkl`. No setup needed beyond the installation steps above.

---

## 🖥️ CLI Commands

Once the program starts, you will see a prompt:

```
  diagnose>
```

| Command | Description |
|---------|-------------|
| `diagnose` | Run a new AI diagnosis |
| `history` | View all diagnoses from this session |
| `about` | Learn how the hybrid AI system works |
| `help` | Show all available commands |
| `exit` | Exit the program |

---

## 📋 How to Use (Step by Step)

1. Run `python app_cli.py` in your terminal
2. At the prompt, type `diagnose` and press Enter
3. Enter **Body Temperature** in °C when asked (e.g. `38.5`)
4. Enter **Symptom Duration** in days when asked (e.g. `3`)
5. The system will display:
   - **ASCII Temperature Gauge** — shows your reading against health zones
   - **ML Risk Level** — Low / Medium / High (colour coded)
   - **Diagnosis** — e.g. Severe Infection, Hypothermia, Healthy
   - **Treatment Recommendation** — actionable medical advice
6. Type `diagnose` again for another reading, or `history` to review past results

---

## 🧪 Example Session

```
  diagnose> diagnose

  🌡  Enter Body Temperature (°C): 40.5
  ⏱  Enter Symptom Duration (days): 6

  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░
  Reading: 40.5°C  →  Zone: HIGH FEVER

  ══════════════════════════════════════════
  ML RISK ASSESSMENT  :  HIGH
  DIAGNOSIS           :  SEVERE INFECTION
  ──────────────────────────────────────────
  TREATMENT ADVICE

  High risk: seek immediate medical attention.
  Visit a hospital urgently and avoid
  self-medication.
  ══════════════════════════════════════════
```

---

## 🧪 Example Outputs

| Temperature | Duration | Risk   | Diagnosis        |
|-------------|----------|--------|------------------|
| 40.5°C      | 6 days   | High   | Severe Infection |
| 39.0°C      | 2 days   | High   | Acute Infection  |
| 38.5°C      | 3 days   | Medium | Mild Viral Fever |
| 36.5°C      | 1 day    | Low    | Healthy          |
| 34.0°C      | 2 days   | High   | Hypothermia      |

---
## 📸 Screenshots (CLI Version)
![1](https://github.com/user-attachments/assets/1cb538f9-fa13-4e79-bfc3-0cf24aa8e784)

![2](https://github.com/user-attachments/assets/915efa6a-9c4a-472a-8fe6-8038c5c4f8bc)

![3](https://github.com/user-attachments/assets/498e7b83-d568-4b94-9360-efd5ec079b12)

![4](https://github.com/user-attachments/assets/82530cdd-c1b7-498b-9b4c-56bbeb484dd6)

---
## 📸 Screenshots (GUI Version)

> Run `python app.py` to launch the optional GUI version.

<img width="600" height="650" alt="AI Diagnostic System GUI" src="https://github.com/user-attachments/assets/391d50cc-d868-4d5f-9bac-01546522008e" />
<img width="600" height="650" alt="Diagnosis Result" src="https://github.com/user-attachments/assets/c40e47a0-5da3-4f32-8884-5c95377a4a40" />
<img width="600" height="650" alt="Severe Infection" src="https://github.com/user-attachments/assets/c3f19707-3fcf-49f7-a476-b9687dc79463" />
<img width="600" height="650" alt="Hypothermia" src="https://github.com/user-attachments/assets/873af9ba-ebfc-461d-b587-6106255554ad" />
<img width="600" height="650" alt="Healthy" src="https://github.com/user-attachments/assets/904e3c51-d355-4177-a520-2d00fc0aba45" />
<img width="600" height="650" alt="Mild Fever" src="https://github.com/user-attachments/assets/c256fa11-01af-406a-9323-69bedad330c6" />

---

## 🤖 How It Works

### Machine Learning (`classifier_model.py`)
- Trains a **Decision Tree Classifier** on 190 labelled samples
- Features: Temperature (°C) and Symptom Duration (days)
- Predicts risk level: **Low**, **Medium**, or **High**
- Model is serialised with `joblib` for persistence across sessions
- Temperatures below 32°C are hardcoded as High risk (extreme edge case)

### Prolog Expert System (`rules.pl`)
- Temperature and duration are converted to symbolic facts (`symptom/2`)
- Inference rules derive one of 6 diagnoses:
  - `severe_infection`, `acute_infection`, `mild_viral_fever`
  - `prolonged_fever`, `hypothermia`, `healthy`
- Matched treatment text is returned alongside the diagnosis
- Facts are retracted and re-asserted per query (fully stateless)

### CLI (`app_cli.py`)
- Interactive command loop with `diagnose`, `history`, `about`, `help`, `exit`
- Colour-coded terminal output using ANSI escape codes
- ASCII temperature gauge with visual health zones
- Session history stored in memory during runtime

---

## 📊 Dataset Format (`symptoms_data.csv`)

```
Temperature_C,Symptom_Duration_Days,Risk_Category
40.2,6,High
38.1,3,Medium
36.5,1,Low
34.0,4,High
29.7,1,High
...
```

190 rows covering the full clinical range: severe hypothermia (25°C) to high fever (41.5°C).

---

## 💡 What Makes This Unique

This system combines two AI paradigms rarely seen together in student projects:

- **ML** handles probabilistic, data-driven risk prediction
- **Prolog** handles transparent, logical, rule-based diagnosis

This mirrors how real clinical decision support systems are designed — not relying on a single AI approach, but combining the strengths of both.

---

## 🔮 Future Improvements

- Add more input features (heart rate, SpO2, blood pressure)
- Upgrade to Random Forest for improved accuracy on larger datasets
- Deploy as a web application with Flask + React frontend
- Add multilingual support for regional languages

---

## 📦 Requirements

```
pyswip
scikit-learn
numpy
joblib
matplotlib
```

Install via: `pip install -r requirements.txt`

---

## 👤 Author

**Author:** Khush M Lohar

