@echo off
setlocal enabledelayedexpansion

echo.
echo === Starting Reticore build (Nuitka + standalone) ===
echo.

:: === Clean up old dist directory ===
if exist dist (
    echo Removing old dist folder...
    rmdir /s /q dist
)

:: === Convert icon path to absolute ===
set ICON=icon.ico
for %%I in (%ICON%) do set ICON_ABS=%%~fI

:: === Build main Reticore GUI ===
echo.
echo === Building Reticore GUI (main.py) ===
python -m nuitka ^
  --follow-imports ^
  --enable-plugin=pyqt6 ^
  --windows-console-mode=disable ^
  --windows-icon-from-ico="%ICON_ABS%" ^
  --standalone ^
  --output-filename=Reticore.exe ^
  --output-dir=dist ^
  --include-data-files=icon.ico=icon.ico ^
  --remove-output ^
  main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Reticore build failed.
    exit /b 1
)

:: === Rename build output directories ===
ren dist\main.dist ReticoreCore

:: === Done ===
echo.
echo === Build completed (Nuitka + standalone) ===
echo dist\ReticoreCore\Reticore.exe
echo.
pause
