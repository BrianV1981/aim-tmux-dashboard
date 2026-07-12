#!/bin/bash
echo "Setting up aim-tmux-dashboard..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "Installation complete. Run ./bin/aim-dash to start."
