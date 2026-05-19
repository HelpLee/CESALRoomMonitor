@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo Building CESALRoomMonitor.exe for Windows
echo This step is only for the developer/build machine.
echo Final users do NOT need Python after the exe is generated.
echo ============================================================
echo.

python --version >nul 2>nul
if errorlevel 1 (
  echo Python was not found on this build machine.
  echo Recommended: use GitHub Actions instead, so local users do not need Python.
  pause
  exit /b 1
)

python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

pyinstaller --noconfirm --clean --onefile --name CESALRoomMonitor check_cesal_rooms.py

if not exist release mkdir release
if exist release\CESALRoomMonitor_Windows_NoPython rmdir /s /q release\CESALRoomMonitor_Windows_NoPython
mkdir release\CESALRoomMonitor_Windows_NoPython
mkdir release\CESALRoomMonitor_Windows_NoPython\logs
mkdir release\CESALRoomMonitor_Windows_NoPython\state

copy /y dist\CESALRoomMonitor.exe release\CESALRoomMonitor_Windows_NoPython\
copy /y config.example.txt release\CESALRoomMonitor_Windows_NoPython\
copy /y README_FIRST_USE.txt release\CESALRoomMonitor_Windows_NoPython\
copy /y LICENSE release\CESALRoomMonitor_Windows_NoPython\ >nul 2>nul

powershell -NoProfile -ExecutionPolicy Bypass -Command "Compress-Archive -Path 'release\CESALRoomMonitor_Windows_NoPython\*' -DestinationPath 'release\CESALRoomMonitor_Windows_NoPython.zip' -Force"

echo.
echo Done.
echo Output: release\CESALRoomMonitor_Windows_NoPython.zip
echo.
pause
