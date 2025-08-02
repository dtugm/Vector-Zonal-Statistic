@echo off
REM Windows batch script to run the Zonal Statistics GUI with Miniconda
REM Handles conda environment activation and proper path resolution

setlocal enabledelayedexpansion

REM ============= CONFIGURATION =============
set "CONDA_ENV_NAME=py310"
REM Change the line above to your environment name
REM =========================================

echo ==========================================
echo  Zonal Statistics GUI Launcher
echo  Environment: %CONDA_ENV_NAME%
echo ==========================================
echo.

REM Get the directory where this batch file is located
set "BIN_DIR=%~dp0"
set "PROJECT_ROOT=%BIN_DIR%.."
set "UI_DIR=%PROJECT_ROOT%\ui"

REM Change to project root directory
cd /d "%PROJECT_ROOT%"

REM Find conda installation
set "CONDA_BASE="

REM Check common conda locations
if exist "%USERPROFILE%\miniconda3\Scripts\conda.exe" (
    set "CONDA_BASE=%USERPROFILE%\miniconda3"
) else if exist "%USERPROFILE%\anaconda3\Scripts\conda.exe" (
    set "CONDA_BASE=%USERPROFILE%\anaconda3"
) else if exist "C:\ProgramData\miniconda3\Scripts\conda.exe" (
    set "CONDA_BASE=C:\ProgramData\miniconda3"
) else if exist "C:\ProgramData\anaconda3\Scripts\conda.exe" (
    set "CONDA_BASE=C:\ProgramData\anaconda3"
) else (
    REM Try to find conda in PATH
    where conda >nul 2>&1
    if !errorlevel! equ 0 (
        for /f "tokens=*" %%i in ('conda info --base 2^>nul') do set "CONDA_BASE=%%i"
    )
)

if "%CONDA_BASE%"=="" (
    echo ERROR: Conda installation not found!
    echo Please ensure Miniconda or Anaconda is installed.
    echo Common locations checked:
    echo   - %USERPROFILE%\miniconda3
    echo   - %USERPROFILE%\anaconda3
    echo   - C:\ProgramData\miniconda3
    echo   - C:\ProgramData\anaconda3
    echo.
    pause
    exit /b 1
)

echo Found conda at: %CONDA_BASE%

REM Initialize conda for this session
call "%CONDA_BASE%\Scripts\activate.bat" "%CONDA_BASE%" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Failed to initialize conda
    echo Please check your conda installation
    pause
    exit /b 1
)

REM Check if environment exists
conda env list | findstr /B "%CONDA_ENV_NAME% " >nul 2>&1
if errorlevel 1 (
    echo ERROR: Conda environment '%CONDA_ENV_NAME%' not found!
    echo.
    echo Available environments:
    conda env list
    echo.
    echo To create the environment, run:
    echo   conda create -n %CONDA_ENV_NAME% python=3.10
    echo   conda activate %CONDA_ENV_NAME%
    echo   pip install geopandas rasterio rasterstats
    echo.
    pause
    exit /b 1
)

REM Activate the conda environment
echo Activating conda environment: %CONDA_ENV_NAME%
call conda activate "%CONDA_ENV_NAME%"
if errorlevel 1 (
    echo ERROR: Failed to activate conda environment: %CONDA_ENV_NAME%
    pause
    exit /b 1
)

echo Environment activated successfully!
echo Python location:
where python
python --version
echo.

REM Check if GUI script exists
if not exist "%UI_DIR%\gui_main.py" (
    echo ERROR: GUI script not found at %UI_DIR%\gui_main.py
    echo Please ensure the project structure is correct
    pause
    exit /b 1
)

REM Check if required modules are available in the environment
echo Checking dependencies in environment '%CONDA_ENV_NAME%'...

python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo ERROR: tkinter is not available in environment '%CONDA_ENV_NAME%'
    echo Please ensure tkinter is installed:
    echo   conda install tk
    echo.
    pause
    exit /b 1
)

set "MISSING_PACKAGES="
for %%p in (geopandas rasterio rasterstats) do (
    python -c "import %%p" >nul 2>&1
    if errorlevel 1 (
        if defined MISSING_PACKAGES (
            set "MISSING_PACKAGES=!MISSING_PACKAGES! %%p"
        ) else (
            set "MISSING_PACKAGES=%%p"
        )
    )
)

if defined MISSING_PACKAGES (
    echo WARNING: Missing packages in environment '%CONDA_ENV_NAME%': !MISSING_PACKAGES!
    echo Install with:
    echo   conda activate %CONDA_ENV_NAME%
    echo   pip install !MISSING_PACKAGES!
    echo.
    set /p "continue=Continue anyway? (y/N): "
    if /i not "!continue!"=="y" (
        pause
        exit /b 1
    )
)

REM Run the GUI application
echo Launching GUI with conda environment '%CONDA_ENV_NAME%'...
echo.
start "Zonal Stats GUI" python "%UI_DIR%\gui_main.py"

REM Wait a moment and check if process started
timeout /t 3 /nobreak >nul
tasklist /fi "imagename eq python.exe" /fi "windowtitle eq Zonal Stats GUI*" >nul 2>&1
if errorlevel 1 (
    echo Note: GUI process may be running. Check for any error messages.
) else (
    echo GUI launched successfully!
    echo Environment: %CONDA_ENV_NAME%
)

echo.
echo You can close this window.
pause
