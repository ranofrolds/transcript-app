Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Obter diretório do script
strPath = objFSO.GetParentFolderName(WScript.ScriptFullName)

' Mudar para o diretório do script
objShell.CurrentDirectory = strPath

' Verificar se existe o ícone, se não, criar
If Not objFSO.FileExists(strPath & "\icon.ico") Then
    objShell.Run "python create_icon.py", 0, True
End If

' Executar aplicativo sem mostrar janela
objShell.Run "pythonw main.pyw", 0, False 