@echo off
cd /d "%~dp0"

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Instale Python 3.8+ de: https://python.org
    pause
    exit /b 1
)

REM Verificar se existe o ícone, se não, criar
if not exist "icon.ico" (
    python create_icon.py >nul 2>&1
)

REM Tentar executar com pythonw (sem console) usando start para desacoplar
start "" pythonw main.pyw
if errorlevel 1 (
    REM Se pythonw falhar, tentar com .py
    start "" pythonw main.py
    if errorlevel 1 (
        REM Como último recurso, usar python normal
        echo Executando com terminal (pythonw nao funcionou)...
        python main.py
        pause
    )
) 