Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")
cwd = fso.GetAbsolutePathName(".")
shell.CurrentDirectory = cwd
shell.Run "cmd /c start_app.bat", 0, False
