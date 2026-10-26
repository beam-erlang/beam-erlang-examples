# Native function

A native library package. `example_nif:hello/0` returns `<<"Hello, world!">>`
from C. The Erlang stub raises `nif_not_loaded` and cannot produce the greeting.

The format-2 manifest binds `example_nif` to its logical CMake native output.
`beam_target_nif` and `beam_package_native_output` use the selected SDK's public
headers, matching-build metadata and platform naming. The native library never
links a second runtime. There is no `on_load`, OTP application, `code:priv_dir`,
or Erlang `load_nif` initializer. These modern native interfaces are provisional.
A matching C compiler is required; native Windows builds need an MSVC developer
environment and Ninja with an MSVC SDK.

Use the selected BEAM/Erlang installation with format-2 package support,
CMake 3.25+ and Python 3.12+. Run these commands from this directory:

```sh
export BEAM_PREFIX=/absolute/path/to/beam-install
"$BEAM_PREFIX/bin/beam-pkg" build .
"$BEAM_PREFIX/bin/beam-pkg" install .
"$BEAM_PREFIX/bin/beam-pkg" shell --project .
# In the shell: example_nif:hello().
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
tar -czf build/delivery/nif.tar.gz beam.lock build/beam-pkg/artifacts README.md LICENSE.txt
python3 test/smoke.py --prefix "$BEAM_PREFIX" --artifact build/delivery/nif.tar.gz \
  --work-root build/test-work
```

The helper installs the extracted archives into a fresh temporary directory,
checks real execution and removes its disposable environment. It requires success
status and expected output; library shell recovery cannot hide a failed assertion.
On Windows use `beam-pkg.exe` for direct commands. Clean generated outputs by
removing `build/`, `.beam/` and `beam.lock`.

See [validation status](../../README.md#validation-status). An older package tool
rejecting format 2 is a blocker, not a reason to downgrade this example.
