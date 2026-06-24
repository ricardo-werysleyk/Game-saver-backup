import winshell
import os
from win32com.client import Dispatch
import sys


def criarAtalhoStartup():
    startup = winshell.startup()
    caminho = os.path.join(startup, "Game Save Backup.lnk")
    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(caminho)
    
    if getattr(sys, 'frozen', False):
        exe_path = sys.executable
    else:
        exe_path = os.path.abspath("GameSaveBackup.exe")

    shortcut.Targetpath = exe_path
    shortcut.WorkingDirectory = os.getcwd()
    shortcut.save()
    
def removerAtalhoStartup():
    startup = winshell.startup()
    caminho = os.path.join(startup, "Game Save Backup.lnk")
    if os.path.exists(caminho):
        os.remove(caminho)