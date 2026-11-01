#!/bin/bash

tmux new-session -d -s hermes-dev

tmux rename-window -t hermes-dev:0 "hermes"

# Qwen start
echo "Qwen 9b start"
tmux new-window -t hermes-dev -n llama.cpp \
  "cd ~/llama.cpp/ && ./run-qwen9b.sh"

# MCP server start
echo "MCP server start"
tmux new-window -t hermes-dev -n MCP \
  "cd ~/LocalHermesAgents/task_manager/mcp && uv run server.py"

# worker start
echo "worker start"
tmux new-window -t hermes-dev -n worker \
  "cd ~/LocalHermesAgents/task_manager/workers && uv run dummy_worker.py"

# Webhook Receiver start
echo "Webhook Receiver start"
tmux new-window -t hermes-dev -n receiver \
  "cd ~/LocalHermesAgents/task_manager/webhook && uv run uvicorn receiver:app --host 0.0.0.0 --port 1077"

# hermes dashboard start
echo "Herms dashboard start"
tmux new-window -t hermes-dev -n dashboard \
  "cd && hermes dashboard --host 192.168.1.66 --no-open"

# Redis start
echo "Redis CLI Start"
tmux new-window -t hermes-dev -n redis \
  "cd && redis-cli"

# CPU Resorce Monitor start
echo "CPU Resorce Monitor start"
tmux new-window -t hermes-dev -n top \
  "top"

# GPU Resorce Monitor start
echo "GPU Resorce Monitor start"
tmux new-window -t hermes-dev -n nvitop \
  "nvitop"