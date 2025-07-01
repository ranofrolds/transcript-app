@echo off
echo ========================================
echo     Compilar Transcritor para .EXE
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo.

REM Instalar PyInstaller se necessário
echo Verificando PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Instalando PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo [ERRO] Falha ao instalar PyInstaller
        pause
        exit /b 1
    )
)

echo [OK] PyInstaller disponivel
echo.

REM Gerar ícone personalizado
echo Gerando icone personalizado...
python create_icon.py
if exist "icon.ico" (
    echo [OK] Icone criado com sucesso!
) else (
    echo [AVISO] Icone nao foi criado, compilando sem icone
)
echo.

REM Limpar builds anteriores
if exist "build" (
    echo Limpando build anterior...
    rmdir /s /q "build"
)

if exist "dist" (
    echo Limpando dist anterior...
    rmdir /s /q "dist"
)

REM Compilar aplicativo
echo.
echo Compilando aplicativo...
echo Isso pode demorar alguns minutos...
echo.

pyinstaller --onefile --windowed --name "Transcritor" --icon=icon.ico main.pyw 2>nul

if errorlevel 1 (
    echo Tentando com main.py...
    pyinstaller --onefile --windowed --name "Transcritor" --icon=icon.ico main.py 2>nul
    if errorlevel 1 (
        echo Tentando sem icone...
        pyinstaller --onefile --windowed --name "Transcritor" main.pyw 2>nul
        if errorlevel 1 (
            pyinstaller --onefile --windowed --name "Transcritor" main.py
            if errorlevel 1 (
                echo [ERRO] Falha na compilacao
                pause
                exit /b 1
            )
        )
    )
)

echo.
echo [OK] Compilacao concluida!
echo.
echo Executavel criado em: dist\Transcritor.exe
echo.

REM Testar executável se existir
if exist "dist\Transcritor.exe" (
    echo Teste rapido do executavel...
    echo Pressione qualquer tecla para testar ou Ctrl+C para sair
    pause >nul
    echo.
    echo Executando teste...
    start "" "dist\Transcritor.exe"
    echo.
    echo Se o aplicativo abriu corretamente, a compilacao foi bem-sucedida!
) else (
    echo [AVISO] Executavel nao encontrado em dist\Transcritor.exe
)

echo.
pause 