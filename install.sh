#!/bin/bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Run setup to ensure virtual environment and dependencies exist
echo "Running setup..."
"$DIR/scripts/setup.sh"

# Create symlink
sudo ln -sf "$DIR/bin/aim-dash" /usr/local/bin/aim-dash

echo "aim-dash installed successfully to /usr/local/bin/aim-dash."
