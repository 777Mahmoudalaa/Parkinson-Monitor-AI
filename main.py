import time
import random
import math
import tkinter as tk
import threading

class AnkleMonitorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Parkinson's Ankle Monitor")
        self.root.geometry("650x450")
        
        # العناوين والبيانات الأساسية للمريض
        tk.Label(root, text="🏥 AI PARKINSON'S ANKLE MONITOR", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(root, text="Patient: Mahmoud | ID: ANKLE-M01-2026 | Location: RIGHT Ankle", font=("Arial", 10, "italic")).pack(pady=5)
        
        # شاشة عرض البيانات الحية
        self.lbl_freq = tk.Label(root, text="Tremor Frequency: -- Hz", font=("Arial", 12))
        self.lbl_freq.pack(pady=10)
        
        self.lbl_tilt = tk.Label(root, text="Ankle Tilt -> Pitch: --° , Roll: --°", font=("Arial", 12))
        self.lbl_tilt.pack(pady=10)
        
        self.lbl_status = tk.Label(root, text="AI Diagnosis: Waiting...", font=("Arial", 14, "bold"), fg="blue")
        self.lbl_status.pack(pady=15)

        # حالة المشغلات (الليزر والمواتير العكسية)
        self.lbl_laser = tk.Label(root, text="🔴 LASER CUEING: --", font=("Arial", 11, "bold"))
        self.lbl_laser.pack(pady=5)
        
        self.lbl_motors = tk.Label(root, text="📳 COUNTER-VIBRATORS: --", font=("Arial", 11, "bold"))
        self.lbl_motors.pack(pady=5)

        # تشغيل الخلفية لقراءة البيانات دون تهنيج الشاشة
        self.cycle_id = 0
        self.running = True
        self.thread = threading.Thread(target=self.update_data_loop, daemon=True)
        self.thread.start()

    def update_data_loop(self):
        while self.running:
            self.cycle_id += 1
            base_hz = random.uniform(2.5, 7.0)
            
            if self.cycle_id % 5 == 0:  # حالة تجمد الحركة FoG
                base_hz = random.uniform(8.5, 11.0)
                pitch, roll = random.uniform(-3.0, 3.0), random.uniform(-3.0, 3.0)
                fog_detected = True
            elif self.cycle_id % 4 == 0:  # حالة ميل حاد وخطر سقوط
                pitch, roll = random.uniform(-25.0, -35.0), random.uniform(-18.0, -28.0)
                fog_detected = False
            else:  # وضع طبيعي مستقر
                pitch, roll = random.uniform(-5.0, 5.0), random.uniform(-5.0, 5.0)
                fog_detected = False

            # إرسال البيانات للواجهة
            self.root.after(0, self.update_ui, base_hz, pitch, roll, fog_detected)
            time.sleep(2)

    def update_ui(self, freq, pitch, roll, fog):
        self.lbl_freq.config(text=f"Tremor Frequency: {freq:.2f} Hz")
        self.lbl_tilt.config(text=f"Ankle Tilt -> Pitch: {pitch:.1f}° , Roll: {roll:.1f}°")
        
        if fog:
            self.lbl_status.config(text="AI Diagnosis: 🚨 FREEZING OF GAIT DETECTED!", fg="red")
            self.lbl_laser.config(text="🔴 LASER CUEING: ⚡ ACTIVE (Visual Line Projected)", fg="red")
            self.lbl_motors.config(text="📳 COUNTER-VIBRATORS: Balanced", fg="black")
        elif pitch < -20.0 or roll < -15.0:
            self.lbl_status.config(text="AI Diagnosis: ⚠️ FALL RISK (Ankle Instability)", fg="orange")
            self.lbl_laser.config(text="🔴 LASER CUEING: Idle", fg="black")
            self.lbl_motors.config(text="📳 COUNTER-VIBRATORS: ⬅️ ACTIVE (Counter-Force Pulse)", fg="orange")
        else:
            self.lbl_status.config(text="AI Diagnosis: 🟢 Stable Ankle Kinematics", fg="green")
            self.lbl_laser.config(text="🔴 LASER CUEING: Idle", fg="black")
            self.lbl_motors.config(text="📳 COUNTER-VIBRATORS: Balanced", fg="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = AnkleMonitorGUI(root)
    root.mainloop()