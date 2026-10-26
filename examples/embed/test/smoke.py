"""Run a relocated bundle, optionally hiding original inputs on Linux."""
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
p.add_argument("--artifact", type=Path, required=True)
p.add_argument("--work-root", type=Path, required=True)
p.add_argument("--isolate", action="store_true")
p.add_argument("--deny", type=Path, action="append", default=[])
a = p.parse_args()
if a.deny and not a.isolate:
    p.error("--deny requires --isolate")
a.work_root.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix="embed space-", dir=a.work_root.resolve()) as temp:
    work = Path(temp)
    bundle = work / "relocated bundle"
    bundle.mkdir()
    with tarfile.open(a.artifact.resolve()) as archive:
        archive.extractall(bundle, filter="data")
    executable = bundle / "bin" / ("example-embed.exe" if os.name == "nt" else "example-embed")
    env = os.environ.copy()
    for key in list(env):
        if key.startswith(("LD_", "DYLD_", "BEAM_", "ERL_")):
            env.pop(key)
    env["PATH"] = str(Path(os.environ["SystemRoot"]) / "System32") if os.name == "nt" else "/usr/bin:/bin"
    command = [str(executable)]
    if a.isolate:
        command = ["/usr/bin/bwrap", "--die-with-parent", "--ro-bind", "/", "/",
                   "--dev-bind", "/dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp"]
        for denied in a.deny:
            command += ["--tmpfs", str(denied.resolve())]
        command += ["--ro-bind", str(bundle), "/tmp/example-bundle", "--chdir", "/tmp",
                    "/tmp/example-bundle/bin/example-embed"]
    out, err = capture(command, cwd=work, env=env)
    if (out, err) != ("42\n", ""):
        raise RuntimeError(f"Unexpected output: {out!r} {err!r}")
print("embed: relocated bundle passed")
