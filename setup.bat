@echo off
REM ZenFox Setup — double-click launcher for Windows (no console window).
REM No args: opens the windowed UI (Simple + Custom tabs, offline, nothing to download).
REM With args: runs the CLI in this console, e.g.
REM   setup.bat --preset advancedfox --adv-level strong --profile work --yes
REM   setup.bat --list-sections
cd /d "%~dp0"
if not "%~1"=="" goto :cli
where pythonw >nul 2>nul
if %errorlevel%==0 (
    start "" /b pythonw setup.py --gui
) else (
    python setup.py --gui
)
goto :eof
:cli
where python >nul 2>nul
if %errorlevel%==0 (
    python setup.py %*
) else (
    echo ERROR: python not found. Install Python 3.8+ from python.org, then re-run setup.bat.
    exit /b 2
)
