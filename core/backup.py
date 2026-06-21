import os
import shutil
from datetime import datetime

#core
import core.log_handling as log
import core.notifications as nt
from models.jogo import Jogo

def makeBackup(origem, destino):
    currentTime = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    if os.path.isdir(origem):
        backupFolderName = f"{os.path.basename(origem)}_{currentTime}"
    else:
        raise Exception("Origem inválida")
    if os.path.isdir(destino):
        backupFolderDirectory = os.path.join(destino,backupFolderName)
    else:
        raise Exception("Destino inválido")

    #faz backup compactado
    shutil.make_archive(backupFolderDirectory,"zip",origem)

#Função responsável por fazer o backup do save
#@params game: nome do processo do jogo, origem: diretório raiz do save, destino: diretório de backup
def backupStart(game : Jogo):
    try:
        makeBackup(game.origem,game.destino)
        toast = nt.notification("Game Save Backup",f"{game.nome_exibicao} salvo")
        toast.add_actions(
            label="Abrir pasta",
            launch=game.destino
        )
        toast.show()
        log.salvarBackupLog(game)
        
    except Exception as e:
        log.salvarErroLog(e)