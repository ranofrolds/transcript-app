@echo off
echo ========================================
echo   Resolver Problemas de Instalacao
echo ========================================
echo.

echo Detectando problema...
python --version
echo.

REM Estratégia 1: Atualizar pip e tentar novamente
echo === ESTRATEGIA 1: Atualizando pip ===
python -m pip install --upgrade pip
if errorlevel 1 (
    echo [AVISO] Falha ao atualizar pip
) else (
    echo [OK] pip atualizado
    echo Tentando instalar novamente...
    pip install -r requirements.txt
    if not errorlevel 1 (
        echo [SUCESSO] Instalacao bem-sucedida!
        goto :sucesso
    )
)

echo.
echo === ESTRATEGIA 2: Instalacao com --user ===
pip install -r requirements.txt --user
if not errorlevel 1 (
    echo [SUCESSO] Instalacao bem-sucedida com --user!
    goto :sucesso
)

echo.
echo === ESTRATEGIA 3: Versoes minimas ===
pip install -r requirements_minimal.txt
if not errorlevel 1 (
    echo [SUCESSO] Instalacao bem-sucedida com versoes minimas!
    goto :sucesso
)

echo.
echo === ESTRATEGIA 4: Instalacao individual ===
echo Instalando sounddevice...
pip install sounddevice
echo Instalando soundfile...
pip install soundfile
echo Instalando numpy...
pip install numpy
echo Instalando requests...
pip install requests
echo Instalando pyperclip...
pip install pyperclip

echo.
echo === ESTRATEGIA 5: Wheels pre-compiladas ===
pip install --only-binary=all sounddevice soundfile numpy requests pyperclip

echo.
echo === TESTE FINAL ===
python -c "import sounddevice, soundfile, numpy, requests, pyperclip; print('Todas as dependencias importadas com sucesso!')"
if not errorlevel 1 (
    echo [SUCESSO] Todas as dependencias funcionando!
    goto :sucesso
)

echo.
echo ========================================
echo          OPCOES ALTERNATIVAS
echo ========================================
echo.
echo 1. ANACONDA/MINICONDA (Recomendado):
echo    conda install -c conda-forge sounddevice soundfile numpy requests pyperclip
echo.
echo 2. PYTHON 3.11 (Mais compativel):
echo    Baixe em: https://www.python.org/downloads/release/python-3118/
echo.
echo 3. INSTALACAO MANUAL:
echo    pip install sounddevice --no-build-isolation
echo    pip install soundfile --no-build-isolation
echo    pip install numpy --no-build-isolation
echo    pip install requests pyperclip
echo.
echo 4. USAR VERSOES ESPECIFICAS:
echo    pip install numpy==1.26.0
echo    pip install sounddevice==0.4.7
echo.
goto :fim

:sucesso
echo.
echo ========================================
echo        INSTALACAO CONCLUIDA!
echo ========================================
echo.
echo Testando aplicativo...
python main.py

:fim
echo.
pause 