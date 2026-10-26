# BEAM/Erlang examples

> **Distribution notice:** These examples target the experimental Erlangsters
> BEAM/Erlang distribution and SDK. This is not upstream Erlang/OTP or an official
> upstream examples repository.

> **Work in progress:** We are working towards making these examples build and
> run successfully with published BEAM/Erlang releases. The setup action and
> release artifacts are not available yet. The workflows cannot currently
> complete successfully; intended platform coverage is not passing evidence.

| Example | Purpose | Scope |
| --- | --- | --- |
| [Script](examples/script/) | Run a source file with literal arguments | Implemented; see validation below |
| [Application](examples/app/) | Build, install and run a minimal package | Implemented; see validation below |
| [Library](examples/lib/) | Install and call a pure library | Implemented; see validation below |
| [Embedding](examples/embed/) | Call Erlang from C and deploy a runtime bundle | Implemented; see validation below |
| [NIF](examples/nif/) | Call a C implementation from an Erlang package | Implemented; see validation below |
| [Ping Pong](examples/ping-pong/) | Independent HTTP server and client | Design only; awaits libraries |
| [Android](examples/android/) | Platform-specific examples to be defined | Documentation only |
| [iOS](examples/ios/) | Platform-specific examples to be defined | Documentation only |

Each implemented example owns its sources, tests and build instructions. Run its
commands from that example directory. There is no root umbrella or shared build
framework. All examples are version 0.1.0 and use the Apache-2.0 license.

## Tools and packages

Select an installed BEAM/Erlang distribution explicitly through `BEAM_PREFIX`.
The examples use its `beam`, `beam-pkg`, public headers and CMake targets. No
Rebar3, external Erlang installation or product source build is required.
Use CMake 3.25+, Python 3.12+ for smoke tests, and a matching C compiler for
embedding and NIFs. Native Windows examples target the MSVC SDK/compiler family;
macOS uses AppleClang and Linux uses the installed SDK's matching compiler family.
Ninja is used for the embedding recipe and Windows package-native builds.

Package examples use format 2 and contain no external dependencies. Building
produces SDK-specific archives and `beam.lock`; installation selects those
archives into `.beam/`. These generated files are ignored in source control.
Uploaded artifacts retain the lock and its relative archive paths, so a fresh
directory can install and exercise them with the same selected SDK.

The source script requires its installed runtime. Package artifacts likewise
require a matching installed runtime/package tool. The embedding bundle includes
its runtime and needs no source tree, compiler or SDK prefix when executed.
Native loading interfaces remain experimental; the NIF uses explicit package
binding rather than OTP application loading.

## GitHub Actions

Five manual `example-*.yml` workflows accept an exact distribution version and
use `beam-erlang/setup-beam-erlang@v1`. That action release and its installer are
still pending. Each workflow builds or prepares an artifact, exercises it, and
uploads successful results for 14 days. Failures remain failures.

Each example has six jobs: both `emu` and `jit` on these intended targets.

| OS / architecture | Runner |
| --- | --- |
| Linux x86-64 | `ubuntu-24.04` |
| macOS ARM64 | `macos-15` |
| Windows x86-64 | `windows-2025` |

Windows native builds configure the MSVC developer environment and reject a
non-MSVC SDK. Platform paths and executable suffixes are selected explicitly.
Ping Pong, Android and iOS have no workflows or runnable placeholders.

## Validation status

Local checks on 2026-10-26 selected existing Linux x86-64 development
installations. Both report `BEAM/Erlang 29.0 (erts-17.0)` and SDK identity `29.0`;
they predate the current release numbering. Their SDK build identities are:

- EMU: `50ab237b91ca52ff2604dad4c3c251880e163fa2b436f54ba2d8cb0131df2098`.
- JIT: `e62c2198da47c5ae96c95e1789534dd0bc0968758e033d727eff5d671be82a86`.

| Check | Linux EMU | Linux JIT |
| --- | --- | --- |
| Copied source script, empty and literal arguments | Passed | Passed |
| C embedding build and runtime bundle | Passed | Passed |
| Relocated embedding execution with original SDK/source/build hidden | Passed | Passed |
| Application package build | Blocked by installed package tool | Blocked by installed package tool |
| Library and NIF package build/execution | Not run; same prerequisite | Not run; same prerequisite |
| Staged application package execution | Not run | Not run |

`beam-pkg build .` rejects the application's format-2 manifest with exit status 1
and `beam-pkg: unsupported package format` on both installations. A selected
installation providing format-2 package support is needed to continue package
validation. The manifests remain format 2; no product rebuild, downgrade or
alternate runtime was used to bypass this tooling blocker. In particular, the
NIF's native execution has not yet been validated in this repository.

The passing cases used independent source copies. Embedding bundles ran from an
unrelated directory with loader overrides removed and original SDK/source/build
paths hidden through Linux bubblewrap. Disposable copies, bundles and build
outputs were removed after execution. These checks used CMake 4.2.3 and Python
3.14.4; workflow helpers require Python 3.12 or newer.

All five workflows pass Actionlint 1.7.7. Python and Bash syntax, TOML source
inventories, documentation links and whitespace are checked independently of
runtime compatibility. Windows PowerShell steps have not been executed locally.
No macOS, Windows or GitHub execution has been established. Ping Pong, Android
and iOS remain documentation only and have no runtime validation claims.
