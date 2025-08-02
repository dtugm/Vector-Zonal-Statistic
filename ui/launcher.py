"""
Cross-platform launcher for the Zonal Statistics GUI
Handles dependency checking and proper path resolution
"""
import sys
import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import importlib.util
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are available"""
    required_modules = ['tkinter', 'geopandas', 'rasterio', 'rasterstats']
    missing_modules = []
    
    for module in required_modules:
        if module == 'tkinter':
            try:
                import tkinter
            except ImportError:
                missing_modules.append('tkinter')
        else:
            if importlib.util.find_spec(module) is None:
                missing_modules.append(module)
    
    return missing_modules

def show_dependency_error(missing_modules):
    """Show error message for missing dependencies"""
    root = tk.Tk()
    root.withdraw()
    
    message = f"Missing required modules: {', '.join(missing_modules)}\n\n"
    message += "Please install them using:\n"
    message += f"pip install {' '.join(missing_modules)}"
    
    messagebox.showerror("Missing Dependencies", message)
    root.destroy()

def main():
    """Main launcher function with proper path handling"""
    # Check dependencies
    missing = check_dependencies()
    if missing:
        show_dependency_error(missing)
        return 1
    
    # Get script directory and project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    gui_script = script_dir / 'gui_main.py'
    
    # Change to project root directory
    os.chdir(project_root)
    
    # Launch GUI
    try:
        if gui_script.exists():
            subprocess.run([sys.executable, str(gui_script)], check=True)
        else:
            raise FileNotFoundError(f"GUI script not found: {gui_script}")
    except subprocess.CalledProcessError as e:
        print(f"Error launching GUI: {e}")
        return 1
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
