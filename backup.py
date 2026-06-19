import os
import shutil
from datetime import datetime

def makeBackup(origem, destino):
    currentTime = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    if os.path.isdir(origem):
        backupFolderName = f"{os.path.basename(origem)}_{currentTime}"
    else:
        raise Exception("Origem inválida")
    if os.path.isdir(destino):
        backupFolderDirectory =os.path.join(destino,backupFolderName)
    else:
        raise Exception("Destino inválido")

    print("\nCopiando...\n")

    #faz backup compactado
    shutil.make_archive(backupFolderDirectory,"zip",origem)

    print("Backup concluído.")
    print(backupFolderDirectory)