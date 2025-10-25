# gui/main_gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import requests

# تكوين الألوان الفاتحة الهادية
BG = "#f5f7fb"
CARD = "#ffffff"
ACCENT = "#6b9bd1"
TEXT = "#222222"

SERVICES = {
    "add":    ("http://127.0.0.1:5001", "/add"),
    "subtract": ("http://127.0.0.1:5002", "/subtract"),
    "multiply": ("http://127.0.0.1:5003", "/multiply"),
    "divide":   ("http://127.0.0.1:5004", "/divide"),
}

def call_service(op, a, b):
    base, endpoint = SERVICES[op]
    url = base + endpoint
    try:
        resp = requests.post(url, json={"a": a, "b": b}, timeout=3)
    except requests.exceptions.RequestException as e:
        return {"error": "service unreachable", "detail": str(e)}
    try:
        return resp.json()
    except:
        return {"error": "invalid response", "status_code": resp.status_code, "text": resp.text}

def on_compute(op):
    a = entry_a.get().strip()
    b = entry_b.get().strip()
    if a == "" or b == "":
        messagebox.showwarning("Missing", "Please enter both numbers")
        return
    result = call_service(op, a, b)
    if "result" in result:
        lbl_result_var.set(f"Result: {result['result']}")
    else:
        err = result.get("error", "Unknown error")
        detail = result.get("detail", "")
        lbl_result_var.set(f"Error: {err}")
        if detail:
            print("detail:", detail)

def check_services():
    statuses = {}
    for k, (base, _) in SERVICES.items():
        try:
            r = requests.get(base + "/health", timeout=1)
            statuses[k] = (r.status_code == 200)
        except:
            statuses[k] = False
    # تحديث الأيقونات
    for k, val in statuses.items():
        lbl = status_labels[k]
        lbl.config(text="●" if val else "○", foreground="green" if val else "gray")
    root.after(2000, check_services)

# UI
root = tk.Tk()
root.title("Distributed Calculator — حاسبة موزعة")
root.geometry("420x320")
root.configure(bg=BG)

frame = ttk.Frame(root, padding=12)
frame.pack(fill="both", expand=True)

style = ttk.Style()
style.theme_use("default")

# Cards-like area
card = tk.Frame(frame, bg=CARD, bd=0, relief="flat")
card.pack(fill="both", expand=True, padx=6, pady=6)

title = tk.Label(card, text="Distributed Calculator", bg=CARD, fg=TEXT, font=("Segoe UI", 14, "bold"))
title.pack(pady=(10, 2))

subtitle = tk.Label(card, text="Light & calm interface — كل خدمة مستقلة", bg=CARD, fg=TEXT, font=("Segoe UI", 9))
subtitle.pack(pady=(0, 10))

# inputs
inp_frame = tk.Frame(card, bg=CARD)
inp_frame.pack(pady=8)

tk.Label(inp_frame, text="A:", bg=CARD, fg=TEXT).grid(row=0, column=0, sticky="e", padx=6, pady=6)
entry_a = ttk.Entry(inp_frame, width=20)
entry_a.grid(row=0, column=1, padx=6, pady=6)

tk.Label(inp_frame, text="B:", bg=CARD, fg=TEXT).grid(row=1, column=0, sticky="e", padx=6, pady=6)
entry_b = ttk.Entry(inp_frame, width=20)
entry_b.grid(row=1, column=1, padx=6, pady=6)

# buttons
btn_frame = tk.Frame(card, bg=CARD)
btn_frame.pack(pady=6)

btn_add = ttk.Button(btn_frame, text="A + B", command=lambda: on_compute("add"))
btn_add.grid(row=0, column=0, padx=6, pady=6)

btn_sub = ttk.Button(btn_frame, text="A - B", command=lambda: on_compute("subtract"))
btn_sub.grid(row=0, column=1, padx=6, pady=6)

btn_mul = ttk.Button(btn_frame, text="A × B", command=lambda: on_compute("multiply"))
btn_mul.grid(row=0, column=2, padx=6, pady=6)

btn_div = ttk.Button(btn_frame, text="A ÷ B", command=lambda: on_compute("divide"))
btn_div.grid(row=0, column=3, padx=6, pady=6)

# result
lbl_result_var = tk.StringVar(value="Result: —")
lbl_result = tk.Label(card, textvariable=lbl_result_var, bg=CARD, fg=TEXT, font=("Segoe UI", 12))
lbl_result.pack(pady=10)

# service status
status_frame = tk.Frame(card, bg=CARD)
status_frame.pack(pady=(6, 12))

tk.Label(status_frame, text="Services:", bg=CARD, fg=TEXT).grid(row=0, column=0, sticky="w", padx=6)
status_labels = {}
col = 1
for key in SERVICES.keys():
    lbl = tk.Label(status_frame, text="○", bg=CARD, fg="gray", font=("Segoe UI", 10, "bold"))
    lbl.grid(row=0, column=col, padx=8)
    tk.Label(status_frame, text=key, bg=CARD, fg=TEXT).grid(row=1, column=col, padx=8)
    status_labels[key] = lbl
    col += 1

# start polling service health
root.after(500, check_services)

root.mainloop()
