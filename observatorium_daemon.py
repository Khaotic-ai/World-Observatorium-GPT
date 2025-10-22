
import time, datetime, subprocess, sys

def run_observatorium():
    print("⏱ Running daily World Observatorium report…")
    cmd = [sys.executable, "observatorium_report.py"]
    subprocess.run(cmd, check=False)

print("🌍 World Observatorium Daemon (UTC-true) — awaiting midnight snapshots.")
while True:
    now_utc = datetime.datetime.utcnow()
    if now_utc.minute == 0 and now_utc.hour == 0:
        run_observatorium()
        time.sleep(65)
    time.sleep(5)
