"""Install and exercise a staged app archive selection, without source files."""
import argparse
import os
from pathlib import Path
import signal
import subprocess
import tarfile
import tempfile

def capture(command, *, cwd, env, input=None, timeout=30):
    """Bound a child and clean its process group on failure or interruption."""
    options = {"start_new_session": True} if os.name != "nt" else {
        "creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
    proc = subprocess.Popen([str(x) for x in command], cwd=cwd, env=env,
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, encoding="utf-8", **options)
    try:
        out, err = proc.communicate(input, timeout=timeout)
    except BaseException:
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                           capture_output=True, timeout=10)
        else:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        proc.wait(timeout=10)
        raise
    if proc.returncode:
        raise RuntimeError(f"{command[0]} exited {proc.returncode}\n{out[-4000:]}{err[-4000:]}")
    return out, err


def interrupted(*_):
    raise KeyboardInterrupt


signal.signal(signal.SIGTERM, interrupted)

p = argparse.ArgumentParser()
p.add_argument("--prefix", type=Path, required=True)
p.add_argument("--artifact", type=Path, required=True)
p.add_argument("--work-root", type=Path, required=True)
a = p.parse_args()
package = a.prefix.resolve() / "bin" / ("beam-pkg.exe" if os.name == "nt" else "beam-pkg")
env = os.environ.copy()
for key in ("ERL_LIBS", "ERL_FLAGS", "ERL_AFLAGS", "ERL_ZFLAGS", "LD_LIBRARY_PATH", "LD_PRELOAD", "DYLD_LIBRARY_PATH", "DYLD_INSERT_LIBRARIES"):
    env.pop(key, None)
a.work_root.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix="app space-", dir=a.work_root.resolve()) as temp:
    project = Path(temp)
    with tarfile.open(a.artifact.resolve()) as archive:
        archive.extractall(project, filter="data")
    if not (project / "beam.lock").is_file() or (project / "beam.toml").exists():
        raise RuntimeError("Expected only locked archives, without a source manifest")
    capture([package, "install", project], cwd=project, env=env, timeout=60)
    out, err = capture([package, "run", "--project", project], cwd=project, env=env,
                       input=None)
    if err or out != "Hello, world!\n":
        raise RuntimeError(f"Unexpected output: {out[-4000:]!r} {err[-4000:]!r}")
print("app: staged package execution passed")
