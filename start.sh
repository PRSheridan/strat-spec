#!/bin/bash

# Run frontend in background
bun run dev &

# Run backend
cd server
python app.py
