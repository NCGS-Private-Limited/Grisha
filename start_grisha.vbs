Set WshShell = CreateObject("WScript.Shell")

WshShell.CurrentDirectory = "N:\Grisha_F2\F2"

WshShell.Run """N:\Grisha_F2\F2\.venv\Scripts\python.exe"" ""N:\Grisha_F2\F2\main.py""", 0, False

Set WshShell = Nothing