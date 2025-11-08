# ATM_Socket_Program

Small example ATM client/server using Python sockets. The server sends simple JSON messages to tell the client when it expects input. The client prints server messages and sends plain UTF-8 text responses back to the server.

This repository contains two runnable scripts at the project root:

- `server.py` — a simple ATM server that keeps an in-memory balance and interacts with one client at a time.
- `client.py` — a terminal client that connects to the server and sends user input.

## Protocol (current implementation)

- The server usually sends JSON-encoded messages. Each JSON object has the shape:

```json
{ "input": <bool>, "data": "<string message>" }
```

- When `input` is `true`, the client should prompt the user and send the typed response as a plain UTF-8 string (no JSON wrapping).
- When `input` is `false`, the client should display the `data` text and not prompt.

Notes:

- The current implementation sends raw JSON bytes (no length-prefix framing). That works for small messages but is fragile when messages can be split/merged by the TCP stream. If you see JSONDecodeError on the client, it means the client attempted to parse a partial or concatenated message.

## Requirements

- Python 3.8+ (the code was tested with Python 3.11+ but uses only stdlib modules)

## Run (Windows PowerShell)

Open two PowerShell windows.

In the first terminal, start the server:

```powershell
python .\server.py
```

In the second terminal, start the client:

```powershell
python .\client.py
```

Interact with the client when it prompts. Use `exit` to close only the client; use `quit` to request the server to shut down as well.

## Common issues & troubleshooting

- JSONDecodeError in the client: this happens when the client does json.loads(...) on bytes that do not contain one full JSON object (because TCP can split or combine packets). The current client attempts to parse every recv() into JSON which is fragile. Workarounds:
  - Keep messages small and run client/server on the same host (reduces chance of splitting).
  - Or use the updated client implementation that catches JSON errors and treats non-JSON as plain text (recommended).

## Recommended improvements (next steps)

1. Framing: send a 4-byte length prefix before JSON payloads so the receiver can read exactly one message at a time. Example pattern: pack length with `struct.pack('!I', len(payload))`, then send header+payload. Receiver reads 4 bytes, unpacks length, then reads length bytes.
2. Always send JSON (server sends, client replies) so both sides have a well-defined data format. Alternatively, keep the current plain-text replies but document it clearly.
3. Add simple tests and a small script that demonstrates a full deposit/withdraw flow automatically.

## Files

- `server.py` — ATM server. Sends JSON messages: `{ "input": bool, "data": str }` and expects plain text replies when `input` is true.
- `client.py` — Client that connects to the server, parses JSON (when possible), and sends back plain UTF-8 strings.

If you want, I can:

- Patch both scripts to use length-prefixed JSON for every message (robust framing) and update the client to send JSON replies as well.
- Or add a short test script that runs server and client in the same process for demonstration.

Tell me which improvement you'd like and I'll implement it.
