# Library

A library package without an executable entry. `example_lib:hello/0` returns
`<<"Hello, world!">>`; the project shell supplies a convenient caller.

Use the selected BEAM/Erlang installation with format-2 package support,
CMake 3.25+ and Python 3.12+. Run these commands from this directory:

```sh
export BEAM_PREFIX=/absolute/path/to/beam-install
"$BEAM_PREFIX/bin/beam-pkg" build .
"$BEAM_PREFIX/bin/beam-pkg" install .
"$BEAM_PREFIX/bin/beam-pkg" shell --project .
# In the shell: example_lib:hello().
# <<"Hello, world!">>
# Exit with q().
```

Build, install and execution are separate steps. There are no external dependencies
or network acquisition steps. Building writes archives under
`build/beam-pkg/artifacts/` and generates `beam.lock` for the selected SDK.
Installation writes `.beam/`; execution never rebuilds or fetches missing inputs.
The lock and installed environment are generated outputs, not portable source locks.

Package the locked archives and exercise them without their source tree:

```sh
mkdir -p build/delivery
tar -czf build/delivery/lib.tar.gz beam.lock build/beam-pkg/artifacts README.md LICENSE.txt
python3 test/smoke.py --prefix "$BEAM_PREFIX" --artifact build/delivery/lib.tar.gz \
  --work-root build/test-work
```

The helper installs the extracted archives into a fresh temporary directory,
checks real execution and removes its disposable environment. It requires success
status and expected output; library shell recovery cannot hide a failed assertion.
On Windows use `beam-pkg.exe` for direct commands. Clean generated outputs by
removing `build/`, `.beam/` and `beam.lock`.

See [validation status](../../README.md#validation-status). An older package tool
rejecting format 2 is a blocker, not a reason to downgrade this example.
