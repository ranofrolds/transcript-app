@echo off
cd /d "%~dp0"

REM Verificar se existe o ícone, se não, criar
if not exist "icon.ico" (
    python create_icon.py >nul 2>&1
)

REM Executar aplicativo sem mostrar console
start "" /B pythonw main.py
exit 