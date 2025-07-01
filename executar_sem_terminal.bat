@echo off

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Instale Python 3.8+ de: https://python.org
    pause
    exit /b 1
)

REM Tentar executar com pythonw (sem console)
pythonw main.pyw >nul 2>&1
if errorlevel 1 (
    REM Se pythonw falhar, tentar com .py
    pythonw main.py >nul 2>&1
    if errorlevel 1 (
        REM Como último recurso, usar python normal
        echo Executando com terminal (pythonw nao funcionou)...
        python main.py
    )
) 