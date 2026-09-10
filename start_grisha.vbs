Set WshShell = CreateObject("WScript.Shell")

WshShell.CurrentDirectory = "N:\Grisha_F2\F2"

WshShell.Run _
    """C:\Users\gamin\AppData\Local\Python\bin\python.exe"" ""N:\Grisha_F2\F2\main.py""", _
    0, _
    False

Set WshShell = Nothing