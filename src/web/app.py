"""Localhost status and control page over runs/ and logs/ (STATUS.md design).

    .venv/bin/uvicorn src.web.app:app --host 127.0.0.1 --port 8787

Controls act through runs/<run>/control.json at step/pass boundaries; start/restart launch `python -m src.runner`
with nohup and record the PID in logs/<run>.pid. Nothing here ever deletes or rewrites data under runs/.
"""
import json, os, pathlib, signal, subprocess, time
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse

ROOT = pathlib.Path(__file__).resolve().parents[2]
RUNS, LOGS, CONFIGS = ROOT / "runs", ROOT / "logs", ROOT / "configs"
PY = ROOT / ".venv/bin/python"
app = FastAPI(title="ai_to_ai_loops")
from .demo import router as demo_router  # noqa: E402  (fast-pair demo grid, /demo)
app.include_router(demo_router)


def _json(p, default=None):
    try:
        return json.loads(pathlib.Path(p).read_text())
    except Exception:  # noqa: BLE001
        return default


def _tail(p, n=20):
    try:
        return pathlib.Path(p).read_text(errors="replace").splitlines()[-n:]
    except Exception:  # noqa: BLE001
        return []


def _pid(run):
    pid = _json(RUNS / run / "progress.json", {}).get("pid")
    if pid is None:
        try: pid = int((LOGS / f"{run}.pid").read_text().strip())
        except Exception: return None  # noqa: BLE001
    try:
        os.kill(pid, 0); return pid
    except OSError:
        return None


def _write_control(run, state):
    p = RUNS / run / "control.json"; tmp = p.with_suffix(".json.tmp")
    tmp.write_text(json.dumps({"state": state, "set_at": time.strftime("%Y-%m-%dT%H:%M:%S")})); os.replace(tmp, p)


def _start(run, config):
    cfg = CONFIGS / config
    if not cfg.exists(): raise HTTPException(404, f"no config {config}")
    LOGS.mkdir(exist_ok=True)
    out = open(LOGS / f"{run}.out", "a")
    proc = subprocess.Popen(["nohup", str(PY), "-m", "src.runner", str(cfg.relative_to(ROOT)), "--run-name", run],
                            cwd=ROOT, stdout=out, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, start_new_session=True)
    (LOGS / f"{run}.pid").write_text(str(proc.pid))
    return proc.pid


@app.get("/api/runs")
def runs():
    out = []
    for d in sorted(RUNS.iterdir()) if RUNS.exists() else []:
        if d.is_dir():
            pr = _json(d / "progress.json", {}); out.append({"run": d.name, "state": pr.get("state"), "alive": _pid(d.name) is not None,
                                                             "completed_steps": pr.get("completed_steps"), "total_steps": pr.get("total_steps"), "updated": pr.get("updated")})
    return out


@app.get("/api/run/{run}")
def run_status(run: str):
    d = RUNS / run
    if not d.exists(): raise HTTPException(404)
    m = _json(d / "manifest.json", {})
    return {"run": run, "alive": _pid(run) is not None, "progress": _json(d / "progress.json", {}), "control": _json(d / "control.json", {}),
            "config_path": m.get("config_path"), "git_commit": m.get("git_commit"), "captioner": (m.get("captioner") or {}).get("digest"),
            "log_tail": _tail(LOGS / f"{run}.log", 25), "gpu_tail": _tail(LOGS / "gpu.csv", 6),
            "events_tail": _tail(d / "events.jsonl", 5)}


@app.get("/api/run/{run}/image/{traj}/{step}")
def image(run: str, traj: int, step: int):
    p = RUNS / run / f"traj_{traj:03d}" / f"step_{step:03d}.png"
    if not p.exists(): raise HTTPException(404)
    return FileResponse(p)


@app.get("/api/run/{run}/record/{traj}/{step}")
def record(run: str, traj: int, step: int):
    p = RUNS / run / f"traj_{traj:03d}" / f"step_{step:03d}.json"
    if not p.exists(): raise HTTPException(404)
    return JSONResponse(_json(p))


@app.post("/api/run/{run}/control/{action}")
def control(run: str, action: str, config: str = ""):
    if action in ("pause", "resume", "stop"):
        if not (RUNS / run).exists(): raise HTTPException(404)
        _write_control(run, {"pause": "paused", "resume": "running", "stop": "stopped"}[action])
        return {"ok": True, "state": _json(RUNS / run / "control.json")}
    if action == "start":
        if _pid(run): raise HTTPException(409, "already running")
        if (RUNS / run / "control.json").exists(): _write_control(run, "running")
        return {"ok": True, "pid": _start(run, config or (_json(RUNS / run / "manifest.json", {}).get("config_path", "").split("/")[-1]))}
    if action == "restart":
        pid = _pid(run)
        if pid:
            _write_control(run, "stopped")
            for _ in range(600):           # the runner exits after the current item (an SDXL call or one caption)
                if _pid(run) is None: break
                time.sleep(1)
            else:
                os.kill(pid, signal.SIGTERM); time.sleep(5)
        _write_control(run, "running")
        return {"ok": True, "pid": _start(run, config or _json(RUNS / run / "manifest.json", {}).get("config_path", "").split("/")[-1])}
    raise HTTPException(400, "unknown action")


PAGE = """<!doctype html><html><head><meta charset=utf-8><title>ai_to_ai_loops</title>
<style>body{font:14px system-ui;margin:16px;background:#111;color:#ddd}a{color:#8cf}table{border-collapse:collapse}td,th{padding:2px 8px;border-bottom:1px solid #333;text-align:left}
pre{background:#000;padding:8px;overflow:auto;max-height:260px;font-size:12px}button{margin:2px 4px 2px 0}.thumbs img{width:128px;height:128px;margin:2px;object-fit:cover}.ok{color:#8f8}.bad{color:#f88}</style></head><body>
<h2>ai_to_ai_loops <small id=clock></small> <small>(refreshes every 15 s; thumbnails are each trajectory's latest completed step)</small></h2><div id=runs></div><div id=run></div>
<script>
let cur=new URLSearchParams(location.search).get('run');
async function j(u,o){const r=await fetch(u,o);return r.json()}
async function act(a){await j(`/api/run/${cur}/control/${a}`,{method:'POST'});setTimeout(load,800)}
async function load(){
 const rs=await j('/api/runs'); if(!cur&&rs.length){const live=rs.filter(r=>r.alive); cur=(live.length?live:rs.slice().sort((a,b)=>(a.updated||'').localeCompare(b.updated||'')))[live.length?0:rs.length-1].run;}
 document.getElementById('runs').innerHTML='<b>runs:</b> '+rs.map(r=>`<a href="?run=${r.run}">${r.run}</a> <span class="${r.alive?'ok':'bad'}">${r.alive?'alive':'not running'}</span> ${r.state||''} ${r.completed_steps||0}/${r.total_steps||'?'}`).join(' &nbsp;|&nbsp; ');
 if(!cur)return; const s=await j(`/api/run/${cur}`); const p=s.progress||{}; const lat=p.latest_complete_step||{};
 const thumbs=Object.entries(lat).map(([t,st])=>st>=0?`<a href="/api/run/${cur}/record/${t}/${st}" title="traj ${t} step ${st}"><img src="/api/run/${cur}/image/${t}/${st}?v=${st}"></a>`:'').join('');
 document.getElementById('run').innerHTML=`<h3>${cur} <span class="${s.alive?'ok':'bad'}">${s.alive?'alive pid '+p.pid:'not running'}</span> state=${p.state||'?'} control=${(s.control||{}).state||'?'}</h3>
 <div><button onclick="act('start')">start</button><button onclick="act('pause')">pause</button><button onclick="act('resume')">resume</button><button onclick="act('stop')">stop</button><button onclick="act('restart')">restart</button></div>
 <table><tr><th>step</th><td>${p.step} / ${p.steps_total}</td><th>phase</th><td>${p.phase||''}</td></tr>
 <tr><th>trajectory-steps</th><td>${p.completed_steps} / ${p.total_steps}</td><th>s / traj-step</th><td>${p.s_per_traj_step||'-'} (eta ${p.eta_hours||'-'} h)</td></tr>
 <tr><th>config</th><td>${s.config_path||''}</td><th>git / captioner</th><td>${(s.git_commit||'').slice(0,8)} / ${(s.captioner||'').slice(0,12)}</td></tr>
 <tr><th>updated</th><td>${p.updated||''}</td><th>last step</th><td>${JSON.stringify(p.last_step||{})}</td></tr></table>
 <h4>latest image per trajectory</h4><div class=thumbs>${thumbs}</div>
 <h4>log</h4><pre>${s.log_tail.join('\\n')}</pre><h4>gpu.csv</h4><pre>${s.gpu_tail.join('\\n')}</pre><h4>events</h4><pre>${s.events_tail.join('\\n')}</pre>`;
 document.getElementById('clock').textContent=new Date().toLocaleTimeString();
}
load(); setInterval(load,15000);
</script></body></html>"""


@app.get("/", response_class=HTMLResponse)
def index():
    return PAGE


@app.get("/demo", response_class=HTMLResponse)
def demo_page():
    return (pathlib.Path(__file__).parent / "demo_page.html").read_text()
