"""Exercise an extracted source archive through the selected BEAM command."""
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
beam = a.prefix.resolve() / "bin" / ("beam.exe" if os.name == "nt" else "beam")
a.work_root.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix="script space-", dir=a.work_root.resolve()) as temp:
    copied = Path(temp)
    with tarfile.open(a.artifact.resolve()) as archive:
        archive.extractall(copied, filter="data")
    for args, expected in [([], "Args: []\n"),
                           (["hello world", "κόσμε", "--literal", ""],
                            'Args: ["hello world",[954,972,963,956,949],"--literal",[]]\n')]:
        out, err = capture([beam, "run", copied / "example_script.erl", "--", *args],
                           cwd=copied, env=os.environ.copy())
        if out != expected or err:
            raise RuntimeError(f"Unexpected output: {out!r} {err!r}")
print("script: copied source and literal arguments passed")
