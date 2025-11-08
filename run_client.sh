#!/usr/bin/env bash
# Start server and save output to server.log
python3 server.py > server.log 2>&1 &
# give the server a moment to start and bind the port
sleep 0.2
python3 client.py
# Leave the server running after the client exits
echo "Client exited; leaving server running. Server output is in server.log"

