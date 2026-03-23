import tkinter as tk
from tkinter import messagebox
import os
from pyswip import Prolog
from classifier_model import load_data_and_train, load_and_predict_risk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ------------------ MODEL ------------------
if not os.path.exists('risk_classifier.pkl'):
    load_data_and_train()

# ------------------ PROLOG ------------------
prolog = Prolog()
prolog.consult("rules.pl")

# ------------------ ROOT ------------------
root = tk.Tk()
root.title("AI Diagnostic System")
root.geometry("900x700")
root.configure(bg="#0f172a")

# ------------------ COLORS ------------------
BG = "#0f172a"
CARD = "#1e293b"
ACCENT = "#38bdf8"
TEXT = "#e2e8f0"
SUCCESS = "#22c55e"
WARNING = "#facc15"
DANGER = "#ef4444"

# ------------------ MAIN CARD ------------------
main_card = tk.Frame(root, bg=CARD)
main_card.place(relx=0.5, rely=0.5, anchor="center", width=820, height=650)

# ------------------ TITLE ------------------
tk.Label(main_card, text="🧠 AI Diagnostic System",
         font=("Helvetica", 24, "bold"),
         fg=ACCENT, bg=CARD).pack(pady=10)

# ------------------ INPUT ------------------
def create_input(label):
    frame = tk.Frame(main_card, bg=CARD)
    frame.pack(pady=6)

    tk.Label(frame, text=label, fg=TEXT, bg=CARD,
             font=("Helvetica", 13)).pack(anchor="w")

    entry = tk.Entry(frame, font=("Helvetica", 15),
                     bg="#334155", fg="white",
                     insertbackground="white", relief="flat", width=25)
    entry.pack(ipady=6)
    return entry

temp_entry = create_input("🌡 Body Temperature (°C)")
duration_entry = create_input("⏱ Duration (days)")

# ------------------ BUTTON ------------------
analyze_btn = tk.Button(main_card,
                        text="⚡ Run AI Analysis",
                        font=("Helvetica", 14, "bold"),
                        bg=ACCENT,
                        fg="black",
                        command=lambda: run_diagnosis())
analyze_btn.pack(pady=15)
def on_enter(e):
    analyze_btn.config(bg="#0ea5e9")

def on_leave(e):
    analyze_btn.config(bg=ACCENT)

analyze_btn.bind("<Enter>", on_enter)
analyze_btn.bind("<Leave>", on_leave)

# ------------------ RESULTS ------------------
tk.Label(main_card, text="📊 Analysis Results",
         font=("Helvetica", 16, "bold"),
         fg=ACCENT, bg=CARD).pack(pady=10)

risk_text = tk.StringVar(value="Awaiting Input...")
diagnosis_text = tk.StringVar()
treatment_text = tk.StringVar()

risk_label = tk.Label(main_card,
    textvariable=risk_text,
    font=("Helvetica", 16, "bold"),
    bg="#0f172a",
    fg="white",
    padx=12,
    pady=6,
    relief="flat"
)
risk_label.pack(pady=5)

diagnosis_label = tk.Label(main_card, textvariable=diagnosis_text,
                           font=("Helvetica", 20, "bold"),
                           fg=DANGER, bg=CARD)
diagnosis_label.pack(pady=8)

treatment_label = tk.Label(main_card, textvariable=treatment_text,
                           wraplength=700,
                           justify="center",
                           fg=TEXT, bg=CARD)
treatment_label.pack(pady=5)

# ------------------ GRAPH ------------------

fig, ax = plt.subplots(figsize=(4,4))
canvas = FigureCanvasTkAgg(fig, master=main_card)
canvas.get_tk_widget().pack(pady=20)

def update_graph(temp):
    ax.clear()

    fig.patch.set_facecolor("#1e293b")
    ax.set_facecolor("#1e293b")

    # 🔥 Dynamic range (FINAL FIX)
    min_limit = min(20, temp - 2)
    max_limit = max(45, temp + 2)

    ax.set_xlim(min_limit, max_limit)
    ax.set_ylim(-1, 1)

    # Remove ticks
    ax.set_xticks([])
    ax.set_yticks([])

    # 🔥 Zones (adjust with range)
    ax.barh([0], [35 - min_limit], left=min_limit, color="#38bdf8", alpha=0.4)  # Hypothermia
    ax.barh([0], [2.5], left=35, color="#22c55e", alpha=0.6)                   # Normal
    ax.barh([0], [1.5], left=37.5, color="#facc15", alpha=0.6)                 # Mild
    ax.barh([0], [max_limit - 39], left=39, color="#ef4444", alpha=0.4)        # High

    # Marker
    ax.plot(temp, 0, "o", color="white", markersize=10)

    # Label
    ax.text(temp, 0.4, f"{temp}°C",
            color="white", ha="center", fontsize=12, weight="bold")

    # Border
    for spine in ax.spines.values():
        spine.set_color("white")

    canvas.draw()

# ------------------ COLOR LOGIC ------------------
def update_risk_color(risk):
    r = str(risk).lower()
    if r == "high":
        risk_label.config(fg=DANGER)
    elif r == "medium":
        risk_label.config(fg=WARNING)
    else:
        risk_label.config(fg=SUCCESS)

# ------------------ MAIN LOGIC ------------------
def run_diagnosis():
    try:
        temp = float(temp_entry.get())
        duration = float(duration_entry.get())

        if temp <= 0 or duration <= 0:
            messagebox.showerror("Error", "Invalid input")
            return

        # ML Risk
        if temp < 32:
            risk = "high"
        elif temp < 35:
            risk = "medium"
        else:
            risk = load_and_predict_risk(temp, duration)

        risk_text.set(f"ML RISK ASSESSMENT: {risk.upper()}")
        update_risk_color(risk)

        # Prolog
        prolog.retractall("symptom(patient,_)")

        if temp >= 39:
            prolog.assertz("symptom(patient, fever_high)")
        elif temp >= 37.5:
            prolog.assertz("symptom(patient, fever_low)")
        elif temp >= 35:
            prolog.assertz("symptom(patient, normal_temp)")
        else:
            prolog.assertz("symptom(patient, temp_very_low)")

        if duration >= 5:
            prolog.assertz("symptom(patient, duration_long)")
        else:
            prolog.assertz("symptom(patient, duration_short)")

        result = list(prolog.query("get_diagnosis(X,T)"))

        if result:
            diagnosis_text.set(f"DIAGNOSIS: {result[0]['X'].upper()}")
            treatment_text.set(result[0]['T'])
        else:
            diagnosis_text.set("DIAGNOSIS: UNKNOWN")
            treatment_text.set("No rule matched.")

        update_graph(temp)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ------------------ START ------------------
root.mainloop()
