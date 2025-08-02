#!/bin/bash
# Shell script to run the Zonal Statistics GUI with Miniconda environment
# This version is optimized for double-click execution in macOS Finder

# ============= CONFIGURATION =============
CONDA_ENV_NAME="py310"  # Change this to your environment name
# =========================================

set -e  # Exit on any error

# Function to pause and wait for user input (for double-click execution)
pause_for_user() {
    echo
    echo "Press any key to continue..."
    read -n 1 -s
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "=========================================="
echo " Zonal Statistics GUI Launcher"
echo " Environment: $CONDA_ENV_NAME"
echo "=========================================="
echo

# Get script directory and project paths
# Handle both direct execution and double-click from Finder
if [[ -n "$BASH_SOURCE" ]]; then
    BIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
else
    BIN_DIR="$(cd "$(dirname "$0")" && pwd)"
fi

PROJECT_ROOT="$(dirname "$BIN_DIR")"
UI_DIR="$PROJECT_ROOT/ui"

echo "Project root: $PROJECT_ROOT"
echo "UI directory: $UI_DIR"
echo "Conda environment: $CONDA_ENV_NAME"
echo

# Change to project root directory
cd "$PROJECT_ROOT" || {
    echo "ERROR: Cannot change to project directory: $PROJECT_ROOT"
    pause_for_user
    exit 1
}

# Find conda installation
CONDA_BASE=""
if [[ -n "$CONDA_PREFIX" ]]; then
    # If already in conda environment, get base
    CONDA_BASE="$(conda info --base 2>/dev/null || echo "")"
elif [[ -d "$HOME/miniconda3" ]]; then
    CONDA_BASE="$HOME/miniconda3"
elif [[ -d "$HOME/anaconda3" ]]; then
    CONDA_BASE="$HOME/anaconda3"
elif [[ -d "/opt/miniconda3" ]]; then
    CONDA_BASE="/opt/miniconda3"
elif [[ -d "/opt/anaconda3" ]]; then
    CONDA_BASE="/opt/anaconda3"
elif command_exists conda; then
    CONDA_BASE="$(conda info --base 2>/dev/null || echo "")"
fi

if [[ -z "$CONDA_BASE" || ! -d "$CONDA_BASE" ]]; then
    echo "ERROR: Conda installation not found!"
    echo "Please ensure Miniconda or Anaconda is installed."
    echo "Common locations checked:"
    echo "  - $HOME/miniconda3"
    echo "  - $HOME/anaconda3"
    echo "  - /opt/miniconda3"
    echo "  - /opt/anaconda3"
    pause_for_user
    exit 1
fi

echo "Found conda at: $CONDA_BASE"

# Initialize conda for this shell session
source "$CONDA_BASE/etc/profile.d/conda.sh" || {
    echo "ERROR: Failed to initialize conda"
    echo "Please check your conda installation"
    pause_for_user
    exit 1
}

# Check if environment exists
if ! conda env list | grep -q "^$CONDA_ENV_NAME "; then
    echo "ERROR: Conda environment '$CONDA_ENV_NAME' not found!"
    echo
    echo "Available environments:"
    conda env list
    echo
    echo "To create the environment, run:"
    echo "  conda create -n $CONDA_ENV_NAME python=3.10"
    echo "  conda activate $CONDA_ENV_NAME"
    echo "  pip install geopandas rasterio rasterstats"
    pause_for_user
    exit 1
fi

# Activate the conda environment
echo "Activating conda environment: $CONDA_ENV_NAME"
conda activate "$CONDA_ENV_NAME" || {
    echo "ERROR: Failed to activate conda environment: $CONDA_ENV_NAME"
    pause_for_user
    exit 1
}

echo "Environment activated successfully!"
echo "Python location: $(which python)"
python --version
echo

# Check if GUI script exists
if [ ! -f "$UI_DIR/gui_main.py" ]; then
    echo "ERROR: GUI script not found at $UI_DIR/gui_main.py"
    echo "Please ensure the project structure is correct"
    pause_for_user
    exit 1
fi

# Check if required modules are available in the environment
echo "Checking dependencies in environment '$CONDA_ENV_NAME'..."

if ! python -c "import tkinter" >/dev/null 2>&1; then
    echo "ERROR: tkinter is not available in environment '$CONDA_ENV_NAME'"
    echo "Please ensure tkinter is installed:"
    echo "  conda install tk"
    pause_for_user
    exit 1
fi

missing_packages=()
for package in geopandas rasterio rasterstats; do
    if ! python -c "import $package" >/dev/null 2>&1; then
        missing_packages+=("$package")
    fi
done

if [ ${#missing_packages[@]} -gt 0 ]; then
    echo "WARNING: Missing packages in environment '$CONDA_ENV_NAME': ${missing_packages[*]}"
    echo "Install with:"
    echo "  conda activate $CONDA_ENV_NAME"
    echo "  pip install ${missing_packages[*]}"
    echo
    echo "Would you like to continue anyway? (y/N)"
    read -n 1 -r REPLY
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        pause_for_user
        exit 1
    fi
fi

# Run the GUI application
echo "Launching GUI with conda environment '$CONDA_ENV_NAME'..."
echo
python "$UI_DIR/gui_main.py" &

# Wait a moment to see if the GUI starts successfully
sleep 2

# Check if the Python process is still running
if pgrep -f "gui_main.py" > /dev/null; then
    echo "GUI launched successfully!"
    echo "Environment: $CONDA_ENV_NAME"
    echo "You can close this terminal window."
else
    echo "ERROR: GUI failed to start"
    echo "Check the error messages above"
    pause_for_user
    exit 1
fi

# For double-click execution, keep terminal open briefly
echo
echo "Terminal will close in 5 seconds..."
sleep 5
