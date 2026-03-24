import os
import sys
from pyswip import Prolog
from classifier_model import load_data_and_train, load_and_predict_risk


class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    CYAN   = "\033[96m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    RED    = "\033[91m"
    WHITE  = "\033[97m"
    DIM    = "\033[2m"
    BG_DARK= "\033[40m"

def colored(text, color):
    return f"{color}{text}{C.RESET}"

def risk_color(risk):
    r = str(risk).lower()
    if r == "high":   return C.RED
    if r == "medium": return C.YELLOW
    return C.GREEN

def print_banner():
    print()
    print(colored("╔══════════════════════════════════════════════════╗", C.CYAN))
    print(colored("║        🧠  AI DIAGNOSTIC SYSTEM  🧠              ║", C.CYAN + C.BOLD))
    print(colored("║   Fever & Hypothermia Classifier  v2.0           ║", C.CYAN))
    print(colored("║   ML (Decision Tree) + Prolog Expert System      ║", C.CYAN))
    print(colored("╚══════════════════════════════════════════════════╝", C.CYAN))
    print()

def print_gauge(temp):
    zones = [(0,   32,  "SEVERE HYPOTHERMIA", C.RED),(32,  35,  "HYPOTHERMIA",        C.CYAN),(35,  37.5,"NORMAL",             C.GREEN),(37.5,39,  "MILD FEVER",         C.YELLOW),(39,  50,  "HIGH FEVER",         C.RED),]

    label = "UNKNOWN"
    col   = C.WHITE
    for lo, hi, lbl, c in zones:
        if lo <= temp < hi:
            label = lbl
            col   = c
            break

    bar_width = 40
    t_min, t_max = 25.0, 42.0
    pos = int((temp - t_min) / (t_max - t_min) * bar_width)
    pos = max(0, min(bar_width - 1, pos))

    bar = list("░" * bar_width)
    bar[pos] = "█"
    bar_str = "".join(bar)

    print(colored("  ┌─────────────────── Temperature Gauge ───────────────────┐", C.DIM))
    print(f"  │  {colored(bar_str, col)}  │")
    print(f"  │  25°C {'':>10} 32°C {'':>4} 35°C {'':>3} 37.5°C {'':>2} 39°C  42°C  │")
    print(colored("  └───────────────────────────────────────────────────────────┘", C.DIM))
    print(f"  {'':>4} Reading: {colored(f'{temp}°C', C.BOLD + col)}  →  Zone: {colored(label, C.BOLD + col)}")
    print()

def divider(char="─", width=52, color=C.DIM):
    print(colored(char * width, color))

def print_help():
    print()
    print(colored("  AVAILABLE COMMANDS", C.BOLD + C.CYAN))
    divider()
    cmds = [
        ("diagnose",   "Run a new diagnosis"),
        ("history",    "View past diagnoses this session"),
        ("about",      "About this system"),
        ("help",       "Show this help menu"),
        ("exit / quit","Exit the program"),
    ]
    for cmd, desc in cmds:
        print(f"  {colored(cmd, C.CYAN):<20} {desc}")
    print()

def print_about():
    print()
    print(colored("  ABOUT THIS SYSTEM", C.BOLD + C.CYAN))
    divider()
    lines = [
        "This system uses a HYBRID AI approach:",
        "",
        "  1. Machine Learning (Decision Tree Classifier)",
        "     → Predicts risk level: Low / Medium / High",
        "     → Trained on 190 temperature + duration samples",
        "",
        "  2. Prolog Expert System (SWI-Prolog + pyswip)",
        "     → Rule-based diagnosis engine",
        "     → Covers 6 conditions:",
        "        • Severe Infection   • Acute Infection",
        "        • Mild Viral Fever   • Prolonged Fever",
        "        • Hypothermia        • Healthy",
        "",
        "  Inputs  : Body Temperature (°C) + Symptom Duration (days)",
        "  Outputs : Risk Level + Diagnosis + Treatment Advice",
    ]
    for line in lines:
        print(f"  {line}")
    print()

def run_diagnosis(prolog, history):
    print()
    print(colored("  ── NEW DIAGNOSIS ──────────────────────────────", C.BOLD + C.CYAN))
    print()

    while True:
        try:
            temp_input = input(colored("  🌡  Enter Body Temperature (°C): ", C.WHITE)).strip()
            if temp_input.lower() in ("exit", "quit", "back"):
                return
            temp = float(temp_input)
            if temp <= 0 or temp > 50:
                print(colored("  ⚠  Please enter a realistic temperature (1–50°C).", C.YELLOW))
                continue
            break
        except ValueError:
            print(colored("  ✗  Invalid input. Enter a number like 38.5", C.RED))

    while True:
        try:
            dur_input = input(colored("  ⏱  Enter Symptom Duration (days): ", C.WHITE)).strip()
            if dur_input.lower() in ("exit", "quit", "back"):
                return
            duration = float(dur_input)
            if duration <= 0:
                print(colored("  ⚠  Duration must be greater than 0.", C.YELLOW))
                continue
            break
        except ValueError:
            print(colored("  ✗  Invalid input. Enter a number like 3", C.RED))

    print()
    print(colored("  ⚡ Running AI Analysis...", C.DIM))
    print()
    
    if temp < 32:
        risk = "High"
    elif temp < 35:
        risk = "High"
    else:
        risk = load_and_predict_risk(temp, duration)
        if isinstance(risk, str) and risk.lower().startswith("error"):
            risk = "Unknown"

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
        diagnosis  = str(result[0]['X']).replace("_", " ").upper()
        treatment  = str(result[0]['T'])
    else:
        diagnosis  = "UNKNOWN"
        treatment  = "No rule matched. Please consult a healthcare professional."

    print_gauge(temp)

    rc = risk_color(risk)
    divider("═", 52, C.CYAN)
    print(f"  {colored('ML RISK ASSESSMENT', C.BOLD)}  :  {colored(risk.upper(), C.BOLD + rc)}")
    print(f"  {colored('DIAGNOSIS', C.BOLD)}          :  {colored(diagnosis, C.BOLD + rc)}")
    divider("─", 52)
    print(f"  {colored('TREATMENT ADVICE', C.BOLD + C.WHITE)}")
    print()
    words = treatment.split()
    line  = "  "
    for word in words:
        if len(line) + len(word) + 1 > 57:
            print(colored(line, C.WHITE))
            line = "  " + word + " "
        else:
            line += word + " "
    if line.strip():
        print(colored(line, C.WHITE))
    divider("═", 52, C.CYAN)
    print()

    history.append({
        "temp": temp, "duration": duration,
        "risk": risk, "diagnosis": diagnosis,
        "treatment": treatment
    })

def print_history(history):
    print()
    if not history:
        print(colored("  No diagnoses recorded yet this session.", C.DIM))
        print()
        return
    print(colored(f"  SESSION HISTORY  ({len(history)} record(s))", C.BOLD + C.CYAN))
    divider()
    for i, h in enumerate(history, 1):
        rc = risk_color(h['risk'])
        print(f"  [{i}] Temp: {colored(str(h['temp'])+'°C', C.WHITE)}  "
              f"Duration: {h['duration']} day(s)  "
              f"Risk: {colored(h['risk'].upper(), rc)}  "
              f"Dx: {colored(h['diagnosis'], rc)}")
    print()

def main():
    if not os.path.exists('risk_classifier.pkl'):
        print(colored("  ⚙  Training ML model for the first time...", C.DIM))
        ok = load_data_and_train()
        if not ok:
            print(colored("  ✗  symptoms_data.csv not found. Cannot train model.", C.RED))
            sys.exit(1)
        print(colored("  ✓  Model trained and saved.\n", C.GREEN))

    try:
        prolog = Prolog()
        prolog.consult("rules.pl")
    except Exception as e:
        print(colored(f"  ✗  Failed to load Prolog rules: {e}", C.RED))
        print(colored("     Make sure SWI-Prolog is installed and rules.pl is present.", C.YELLOW))
        sys.exit(1)

    history = []
    print_banner()
    print(colored("  Type 'help' to see available commands.\n", C.DIM))

    while True:
        try:
            cmd = input(colored("  diagnose> ", C.BOLD + C.CYAN)).strip().lower()
        except (KeyboardInterrupt, EOFError):
            print()
            print(colored("\n  Goodbye! Stay healthy. 👋\n", C.CYAN))
            break

        if cmd in ("exit", "quit"):
            print(colored("\n  Goodbye! Stay healthy. 👋\n", C.CYAN))
            break
        elif cmd == "diagnose" or cmd == "":
            run_diagnosis(prolog, history)
        elif cmd == "history":
            print_history(history)
        elif cmd == "about":
            print_about()
        elif cmd == "help":
            print_help()
        else:
            print(colored(f"\n  ✗  Unknown command: '{cmd}'. Type 'help' for options.\n", C.YELLOW))

if __name__ == "__main__":
    main()
