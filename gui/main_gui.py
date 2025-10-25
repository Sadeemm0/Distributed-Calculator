import tkinter as tk
from tkinter import messagebox
import requests
import threading

GATEWAY_URL = "http://127.0.0.1:5000"

# ألوان هادئة
BG_COLOR = "#f0f2f5"
TEXT_COLOR = "#333333"

def call_service(op, a, b):
    url = f"{GATEWAY_URL}/calculate/{op}"
    try:
        resp = requests.post(url, json={"a": a, "b": b}, timeout=5)
        return resp.json()
    except:
        return {"error": "Gateway unreachable"}

def on_compute(op):
    a = entry_a.get().strip()
    b = entry_b.get().strip()
    if not a or not b:
        messagebox.showwarning("Missing", "Please enter both numbers")
        return
    
    # تعطيل الأزرار مؤقتاً
    for btn in [btn_add, btn_sub, btn_mul, btn_div]:
        btn.config(state="disabled")
    
    lbl_result.config(text="Computing...", fg="orange")

    def compute():
        result = call_service(op, a, b)
        
        # تحديث الواجهة في الخيط الرئيسي
        root.after(0, lambda: update_result(result))

    threading.Thread(target=compute, daemon=True).start()

def update_result(result):
    # إعادة تفعيل الأزرار
    for btn in [btn_add, btn_sub, btn_mul, btn_div]:
        btn.config(state="normal")
    
    if "result" in result:
        lbl_result.config(text=f"Result: {result['result']}", fg="green")
    else:
        lbl_result.config(text=f"Error: {result.get('error', 'Unknown')}", fg="red")

# إنشاء النافذة
root = tk.Tk()
root.title("Distributed Calculator - نظام موزع")
root.geometry("450x400")  # زيادة العرض والطول
root.configure(bg=BG_COLOR)
root.resizable(False, False)

# العنوان
title_label = tk.Label(root, text=" Distributed Calculator", 
                      bg=BG_COLOR, fg=TEXT_COLOR, font=("Arial", 16, "bold"))
title_label.pack(pady=15)


# إطار المدخلات
input_frame = tk.Frame(root, bg=BG_COLOR)
input_frame.pack(pady=15)

tk.Label(input_frame, text="Number A:", bg=BG_COLOR, fg=TEXT_COLOR, 
         font=("Arial", 11)).grid(row=0, column=0, padx=8, pady=8)
entry_a = tk.Entry(input_frame, width=18, font=("Arial", 12), justify='center')
entry_a.grid(row=0, column=1, padx=8, pady=8)

tk.Label(input_frame, text="Number B:", bg=BG_COLOR, fg=TEXT_COLOR,
         font=("Arial", 11)).grid(row=1, column=0, padx=8, pady=8)
entry_b = tk.Entry(input_frame, width=18, font=("Arial", 12), justify='center')
entry_b.grid(row=1, column=1, padx=8, pady=8)

# إطار الأزرار
button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.pack(pady=20)

# أزرار أكبر وأوضح
btn_add = tk.Button(button_frame, text="➕ ", width=10, height=2,
                   command=lambda: on_compute("add"), bg="#2196F3", fg="white", 
                   font=("Arial", 11, "bold"), cursor="hand2")
btn_add.grid(row=0, column=0, padx=6, pady=5)

btn_sub = tk.Button(button_frame, text="➖ ", width=10, height=2,
                   command=lambda: on_compute("subtract"), bg="#FF9800", fg="white", 
                   font=("Arial", 11, "bold"), cursor="hand2")
btn_sub.grid(row=0, column=1, padx=6, pady=5)

btn_mul = tk.Button(button_frame, text="✖️ ", width=10, height=2,
                   command=lambda: on_compute("multiply"), bg="#9C27B0", fg="white", 
                   font=("Arial", 11, "bold"), cursor="hand2")
btn_mul.grid(row=0, column=2, padx=6, pady=5)

btn_div = tk.Button(button_frame, text="➗ ", width=10, height=2,
                   command=lambda: on_compute("divide"), bg="#F44336", fg="white", 
                   font=("Arial", 11, "bold"), cursor="hand2")
btn_div.grid(row=0, column=3, padx=6, pady=5)

# نتيجة
lbl_result = tk.Label(root, text="Result: —", bg=BG_COLOR, fg=TEXT_COLOR, 
                     font=("Arial", 14, "bold"), pady=10)
lbl_result.pack(pady=20)


root.mainloop()