@echo off
echo ========================================
echo  Transcritor de Audio - OpenAI Whisper
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Por favor, instale Python 3.8+ de: https://python.org
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo.

REM Verificar se pip está disponível
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] pip nao encontrado!
    echo Reinstale o Python com pip incluido
    pause
    exit /b 1
)

echo [OK] pip encontrado
echo.

REM Atualizar pip primeiro
echo Atualizando pip...
python -m pip install --upgrade pip

REM Instalar dependências
echo.
echo Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [AVISO] Tentativa 1 falhou. Tentando com versoes minimas...
    pip install -r requirements_minimal.txt
    if errorlevel 1 (
        echo.
        echo [AVISO] Tentativa 2 falhou. Tentando instalacao individual...
        pip install sounddevice soundfile numpy requests pyperclip
        if errorlevel 1 (
            echo.
            echo [ERRO] Todas as tentativas falharam!
            echo.
            echo === SOLUCOES ALTERNATIVAS ===
            echo 1. Tente: pip install -r requirements.txt --user
            echo 2. Use Anaconda: conda install -c conda-forge sounddevice soundfile numpy requests pyperclip
            echo 3. Baixe Python 3.11 em vez de 3.12: https://python.org
            echo.
            pause
            exit /b 1
        )
    )
)

echo.
echo [OK] Dependencias instaladas com sucesso!
echo.

REM Executar aplicativo
echo Iniciando aplicativo...
echo.
python main.py

pause 