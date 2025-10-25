import subprocess, sys, time, threading

processes = []

def start(script):
    p = subprocess.Popen([sys.executable, script])
    processes.append(p)
    time.sleep(0.5)

def start_gui():
    time.sleep(3)  # انتظر شوية عشان الخدمات تخلص تحميل
    subprocess.Popen([sys.executable, "gui/main_gui.py"])

try:
    start("services/adder.py")
    start("services/subtractor.py")
    start("services/multiplier.py")
    start("services/divider.py")
    start("gateway/api_gateway.py")
    
    print("All services and gateway started!")
    print("🎮 Starting GUI now...")
    
    # شغل الواجهة في خيط منفصل
    threading.Thread(target=start_gui, daemon=True).start()
    
    for p in processes: 
        p.wait()
        
except KeyboardInterrupt:
    print("Stopping all services...")
    for p in processes: 
        p.terminate()
