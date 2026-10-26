# Source script

`example_script:main/1` prints its argument list and returns. This uses ordinary
source execution; it has no package manifest or executable wrapper.

Run from this directory with an explicitly selected installation:

```sh
export BEAM_PREFIX=/absolute/path/to/beam-install
"$BEAM_PREFIX/bin/beam" run example_script.erl -- 'hello world' --literal
# Args: ["hello world","--literal"]
```

No arguments prints `Args: []`. Unicode arguments arrive as Unicode charlists;
the term printer may display their code points as integer lists. Empty strings
are empty lists. Successful execution exits zero. An uncaught failure exits nonzero.

Prepare a source archive and run the copied-source checks with Python 3.12+:

```sh
mkdir -p build
tar -czf build/script.tar.gz example_script.erl README.md LICENSE.txt
python3 test/smoke.py --prefix "$BEAM_PREFIX" --artifact build/script.tar.gz \
  --work-root build/test-work
```

The helper extracts into a disposable directory and checks empty arguments,
spaces, Greek text, a leading `--` argument and an empty string. It removes its
copies and bounds child execution. On Windows select `beam.exe` for direct
commands. See [validation status](../../README.md#validation-status).
