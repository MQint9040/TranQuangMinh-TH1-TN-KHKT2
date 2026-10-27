#Code đồ thị debounce
import csv
import serial
import matplotlib.pyplot as plt

PORT, BAUD, DEB_MS = "COM11", 115200, 60   # đổi COM

ser = serial.Serial(PORT, BAUD, timeout=0.05)
t, raw, deb = [], [], []
t0 = None
log_text = "Chưa có lần nhấn nào"

plt.ion()
fig = plt.figure(figsize=(10, 6))
fig.suptitle(f"VD2 — Chống dội (debounce {DEB_MS}ms) — {PORT} @ {BAUD} baud",
             fontsize=10, fontweight="bold")

fig.text(0.25, 0.86, "rawEdgeCount (sườn xuống THÔ)", ha="center", color="#c0553a")
fig.text(0.75, 0.86, "debouncedCount (lần nhấn THỰC)", ha="center", color="#3a7d5c")
big_raw = fig.text(0.25, 0.72, "0", ha="center", fontsize=40,
                   fontweight="bold", color="#c0553a")
big_deb = fig.text(0.75, 0.72, "0", ha="center", fontsize=40,
                   fontweight="bold", color="#3a7d5c")
log_box = fig.text(0.05, 0.60, log_text, fontsize=9,
                   bbox=dict(boxstyle="round", fc="#f8dcd8", ec="#d9a9a2"))

ax = fig.add_axes([0.1, 0.1, 0.85, 0.40])
ax.set_xlabel("thời gian (s)")
ax.set_ylabel("số lần đếm (count)")
ax.grid(alpha=0.3)
(l_raw,) = ax.step([], [], where="post", color="#e0603a", label="rawEdgeCount (thô)")
(l_deb,) = ax.step([], [], where="post", color="#2e8b57", label="debouncedCount (đã lọc)")
ax.legend(loc="upper left", fontsize=8)

try:
    while plt.fignum_exists(fig.number):
        line = ser.readline().decode(errors="ignore").strip()
        parts = line.split(",")
        if len(parts) == 3 and all(p.isdigit() for p in parts):
            ms, r, d = map(int, parts)
            if t0 is None:
                t0 = ms
            prev_d = deb[-1] if deb else 0
            t.append((ms - t0) / 1000)
            raw.append(r)
            deb.append(d)

            big_raw.set_text(str(r))
            big_deb.set_text(str(d))
            if d > prev_d:
                log_box.set_text(f"Lần nhấn #{d}: 1 sườn xuống hợp lệ -> debouncedCount +1")
            else:
                log_box.set_text(f"Sườn xuống #{r}: nhiễu dội, bị loại (debouncedCount giữ {d})")

            l_raw.set_data(t, raw)
            l_deb.set_data(t, deb)
            ax.relim()
            ax.autoscale_view()
        plt.pause(0.01)
finally:
    ser.close()
    with open("debounce_log.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["time_s", "rawEdgeCount", "debouncedCount"])
        w.writerows(zip(t, raw, deb))