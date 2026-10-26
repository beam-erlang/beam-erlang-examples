# Ping Pong — planned

This example is documentation only. The goal is two independent HTTP/1.1
programs: a server built with a future Erlangsters equivalent of Cowboy and a
client built with a future Erlangsters equivalent of Gun. Those libraries are
not implemented. Their package names, APIs, versions and runtime integration
remain to be established. There is no raw-TCP replacement, runnable stub or workflow.

## Intended interface

- The server listens on `127.0.0.1:8080`. `PING_PONG_PORT` selects another valid
  port; malformed configuration fails with a useful diagnostic.
- `GET /ping` returns status `200`, content type `text/plain`, and exact body `pong`.
- Unknown routes return `404`; unsupported methods on `/ping` return `405`.
- The client accepts one complete HTTP URL, verifies status, content type and
  body, prints `pong` followed by a newline, and exits `0`.
- Client `--help` exits `0`; invalid arguments or unsupported URLs exit `2`;
  connection failures, timeouts and unexpected responses exit `1` with useful stderr.
- Connection and response waits are each bounded to five seconds. No retries,
  redirects, HTTPS, HTTP/2 or WebSockets are intended for the first version.

## Future acceptance

Build server and client independently, run repeated requests through their
packaged artifacts, and check invalid input, unavailable servers, timeouts,
wrong responses, routes and methods. Own and close sockets/processes on both
normal and failed startup. Stop the server, confirm cleanup, restart and repeat.

The [server](server/) and [client](client/) folders record responsibilities only.
Choose their build and launch interfaces once the libraries and required runtime
capabilities exist. Root [validation status](../../README.md#validation-status)
does not claim any implementation or execution for this example.
