"""GPU health sampler: nvidia-smi every N seconds to a CSV (SPEC §8)."""
import datetime, os, pathlib, subprocess, threading

FIELDS = "temperature.gpu,power.draw,memory.used,memory.total,clocks.sm,clocks.mem,utilization.gpu"


def query():
    out = subprocess.run(["nvidia-smi", f"--query-gpu={FIELDS}", "--format=csv,noheader,nounits"],
                         capture_output=True, text=True, timeout=20).stdout.strip()
    return [x.strip() for x in out.split(",")]


def vram_used_mb():
    try:
        return float(query()[2])
    except Exception:  # noqa: BLE001
        return float("nan")


class GpuLogger(threading.Thread):
    def __init__(self, path, interval_s=10, run_name=""):
        super().__init__(daemon=True)
        self.path = pathlib.Path(path); self.interval = interval_s; self.run_name = run_name
        self.phase = "init"; self._stop = threading.Event()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("timestamp,run,phase," + FIELDS.replace(".", "_") + "\n")

    def run(self):
        while not self._stop.is_set():
            try:
                row = [datetime.datetime.now().isoformat(timespec="seconds"), self.run_name, self.phase] + query()
                with open(self.path, "a") as f:
                    f.write(",".join(row) + "\n"); f.flush(); os.fsync(f.fileno())
            except Exception as e:  # noqa: BLE001
                with open(self.path, "a") as f:
                    f.write(f"{datetime.datetime.now().isoformat(timespec='seconds')},{self.run_name},{self.phase},ERROR {e!r}\n")
            self._stop.wait(self.interval)

    def stop(self):
        self._stop.set()
