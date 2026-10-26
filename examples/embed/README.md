# Embed Erlang in C

A C host compiles and embeds `answer.erl`, calls `answer:value/0`, checks the exact
returned integer `42`, stops and terminates the VM/system, and only then prints
`42` from C. Native lifecycle calls remain visible in `main.c`. This small example
decodes only its known integer result; it does not need a shared ETF codec.

Use an installed SDK, CMake 3.25+, Ninja, a matching C compiler and Python 3.12+.
Run from this directory:

```sh
export BEAM_PREFIX=/absolute/path/to/beam-install
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH="$BEAM_PREFIX"
cmake --build build
cmake --install build --prefix "$PWD/build/bundle"
mkdir -p build/delivery
tar -czf build/delivery/embed.tar.gz -C build/bundle .
python3 test/smoke.py --artifact build/delivery/embed.tar.gz --work-root build/test-work
```

CMake discovers `BEAM::CLI` and `BEAM::Runtime` through the installed SDK. A small
local CMake helper turns the compiled module into a C byte array. The bare
deployment profile bundles the runtime and its platform dependencies; it does
not require loose application bytecode or compiler tooling at execution time.
The recipe and lifecycle are adapted from the SDK's Apache-2.0 first-call example.

The smoke test extracts and relocates the bundle, runs it from an unrelated
working directory with loader overrides removed, and expects exactly `42`
followed by a newline and exit zero. On Linux, add `--isolate` and repeated
`--deny /absolute/path` arguments to hide the original SDK, source and build
prefixes using bubblewrap. Keep its work directory outside the hidden paths.
Tests own and clean temporary copies and processes.

Windows needs the matching MSVC developer environment; configure with
`-DCMAKE_C_COMPILER=cl` and execute `bin/example-embed.exe` from the bundle.
Unix systems use `bin/example-embed`. No fallback runtime is selected.
See [validation status](../../README.md#validation-status).
