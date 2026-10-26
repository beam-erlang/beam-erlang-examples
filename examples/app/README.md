# Application

A minimal executable package. `example_app:main/1` prints `Hello, world!`
and returns successfully. This is not an OTP application or supervision tree.

Use the selected BEAM/Erlang installation with format-2 package support,
CMake 3.25+ and Python 3.12+. Run these commands from this directory:

```sh
export BEAM_PREFIX=/absolute/path/to/beam-install
"$BEAM_PREFIX/bin/beam-pkg" build .
"$BEAM_PREFIX/bin/beam-pkg" install .
"$BEAM_PREFIX/bin/beam-pkg" run --project .
# Hello, world!
```

Build, install and execution are separate steps. There are no external dependencies
or network acquisition steps. Building writes archives under
`build/beam-pkg/artifacts/` and generates `beam.lock` for the selected SDK.
Installation writes `.beam/`; execution never rebuilds or fetches missing inputs.
The lock and installed environment are generated outputs, not portable source locks.

Package the locked archives and exercise them without their source tree:

```sh
mkdir -p build/delivery
tar -czf build/delivery/app.tar.gz beam.lock build/beam-pkg/artifacts README.md LICENSE.txt
python3 test/smoke.py --prefix "$BEAM_PREFIX" --artifact build/delivery/app.tar.gz \
  --work-root build/test-work
```

The helper installs the extracted archives into a fresh temporary directory,
checks real execution and removes its disposable environment. It requires success
status and expected output; library shell recovery cannot hide a failed assertion.
On Windows use `beam-pkg.exe` for direct commands. Clean generated outputs by
removing `build/`, `.beam/` and `beam.lock`.

See [validation status](../../README.md#validation-status). An older package tool
rejecting format 2 is a blocker, not a reason to downgrade this example.
