#!/bin/bash
# Shell script to run the Zonal Statistics GUI with Miniconda environment
# Standard version for command line execution

# ============= CONFIGURATION =============
CONDA_ENV_NAME="py310"  # Change this to your environment name
# =========================================

set -e  # Exit on any error

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
BIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$BIN_DIR")"
UI_DIR="$PROJECT_ROOT/ui"

echo "Project root: $PROJECT_ROOT"
echo "Conda environment: $CONDA_ENV_NAME"
echo

# Change to project root directory
cd "$PROJECT_ROOT" || {
    echo "ERROR: Cannot change to project directory: $PROJECT_ROOT"
    exit 1
}

# Find conda installation
CONDA_BASE=""
if [[ -n "$CONDA_PREFIX" ]]; then
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
    exit 1
fi

echo "Found conda at: $CONDA_BASE"

# Initialize conda for this shell session
source "$CONDA_BASE/etc/profile.d/conda.sh" || {
    echo "ERROR: Failed to initialize conda"
    exit 1
}

# Check if environment exists
if ! conda env list | grep -q "^$CONDA_ENV_NAME "; then
    echo "ERROR: Conda environment '$CONDA_ENV_NAME' not found!"
    echo "Available environments:"
    conda env list
    echo
    echo "To create the environment, run:"
    echo "  conda create -n $CONDA_ENV_NAME python=3.10"
    echo "  conda activate $CONDA_ENV_NAME"
    echo "  pip install geopandas rasterio rasterstats"
    exit 1
fi

# Activate the conda environment
echo "Activating conda environment: $CONDA_ENV_NAME"
conda activate "$CONDA_ENV_NAME" || {
    echo "ERROR: Failed to activate conda environment: $CONDA_ENV_NAME"
    exit 1
}

echo "Environment activated successfully!"
echo "Python location: $(which python)"
python --version
echo

# Check dependencies and run GUI
echo "Checking dependencies in environment '$CONDA_ENV_NAME'..."

missing_packages=()
for package in tkinter geopandas rasterio rasterstats; do
    if ! python -c "import $package" >/dev/null 2>&1; then
        missing_packages+=("$package")
    fi
done

if [ ${#missing_packages[@]} -gt 0 ]; then
    echo "WARNING: Missing packages: ${missing_packages[*]}"
    echo "Install with: pip install ${missing_packages[*]}"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Run the GUI application
echo "Launching GUI with conda environment '$CONDA_ENV_NAME'..."
python "$UI_DIR/gui_main.py"

echo "GUI application closed"
