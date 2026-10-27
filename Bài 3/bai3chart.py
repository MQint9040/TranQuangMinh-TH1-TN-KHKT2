#Code đồ thị so sánh lọc và thô
import csv
import serial
import matplotlib.pyplot as plt
import numpy as np

PORT, BAUD = "COM11", 115200   # đổi COM
WINDOW = 400                  

ser = serial.Serial(PORT, BAUD, timeout=0.05)
t, tho, loc = [], [], []
t0 = None

plt.ion()
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlabel("thời gian (s)")
ax.set_ylabel("giá trị ADC (0-4095)")
ax.grid(alpha=0.3)
(l_tho,) = ax.plot([], [], color="#e0603a", lw=1, label="tho (thô)")
(l_loc,) = ax.plot([], [], color="#2e8b57", lw=2, label="loc (trung bình trượt N=8)")
ax.legend(loc="upper left")

try:
    while plt.fignum_exists(fig.number):
        parts = ser.readline().decode(errors="ignore").strip().split(",")
        if len(parts) == 3 and all(p.isdigit() for p in parts):
            ms, a, b = map(int, parts)
            if t0 is None:
                t0 = ms
            t.append((ms - t0) / 1000)
            tho.append(a)
            loc.append(b)

            l_tho.set_data(t[-WINDOW:], tho[-WINDOW:])
            l_loc.set_data(t[-WINDOW:], loc[-WINDOW:])
            ax.relim()
            ax.autoscale_view()
            if len(tho) >= 50:
                ax.set_title(f"Độ lệch chuẩn 50 mẫu cuối: tho = {np.std(tho[-50:]):.1f} | "
                             f"loc = {np.std(loc[-50:]):.1f}", fontsize=10)
        plt.pause(0.01)
finally:
    ser.close()
    with open("adc_log.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["time_s", "tho", "loc"])
        w.writerows(zip(t, tho, loc))