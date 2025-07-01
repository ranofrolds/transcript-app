@echo off
REM ===========================================
REM   TRANSCRITOR DE AUDIO - EXECUTAR APP
REM ===========================================

title Iniciando Transcritor...
cd /d "%~dp0"

echo 🎤 Iniciando Transcritor de Audio...
echo.

REM Criar ícone se necessário
if not exist "icon.ico" (
    echo 🎨 Criando icone personalizado...
    python create_icon.py >nul 2>&1
)

echo ✅ Abrindo aplicativo sem terminal...
echo 📝 Agora pode fechar esta janela!
echo.

REM Executar sem mostrar console
start "" pythonw main.pyw

timeout /t 2 >nul
exit 