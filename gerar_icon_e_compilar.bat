@echo off
echo 🎨 Gerando ícone personalizado...
python create_icon.py

echo.
echo 📦 Compilando aplicativo com ícone...

if exist "icon.ico" (
    echo ✅ Ícone criado com sucesso!
    echo 🔧 Compilando versão com ícone...
    pyinstaller --onefile --noconsole --icon=icon.ico main.pyw
    echo ✅ Compilação concluída!
) else (
    echo ❌ Erro ao criar ícone, compilando sem ícone...
    pyinstaller --onefile --noconsole main.pyw
)

echo.
echo 🎉 Processo concluído!
echo.
pause 