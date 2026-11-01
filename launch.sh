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
  "cd ~/LocalHermesAgents && uv run python -m task_manager.mcp.server"

# worker start
echo "worker start"
tmux new-window -t hermes-dev -n worker \
  "cd ~/LocalHermesAgents && uv run python -m task_manager.workers.dummy_worker"

# Webhook Receiver start
echo "Webhook Receiver start"
tmux new-window -t hermes-dev -n receiver \
  "cd ~/LocalHermesAgents && uv run uvicorn task_manager.webhook.receiver:app --host 127.0.0.1 --port 6379"

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