import os
import glob
import shutil
from datetime import datetime

#core
import core.log_handling as log
import core.notifications as nt
#models
from models.jogo import Jogo
from models.settings import Settings

config = Settings()

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
        total_backups = sum(1 for item in os.scandir(game.destino) if item.is_file())
        
        if total_backups > config.total_backups:
            deletar_arquivo(game.destino)
        
        toast = nt.notification("Game Save Backup",f"{game.nome_exibicao} salvo")
        toast.add_actions(
            label="Abrir pasta",
            launch=game.destino
        )
        toast.show()
        log.salvarBackupLog(game)
        
    except Exception as e:
        log.salvarErroLog(e)
        
def arquivo_mais_antigo(caminho_pasta):
    padrao_busca = os.path.join(caminho_pasta, "*.zip")
    arquivos = glob.glob(padrao_busca)
    if not arquivos:
        return None
    
    return min(arquivos, key=os.path.getmtime)

def deletar_arquivo(caminho_pasta):
    save_antigo = arquivo_mais_antigo(caminho_pasta)
    os.remove(save_antigo)

def arquivo_mais_recente(caminho_pasta):
    padrao_busca = os.path.join(caminho_pasta, "*.zip")
    arquivos = glob.glob(padrao_busca)
    if not arquivos:
        return None
    
    return max(arquivos, key=os.path.getmtime)

def limpar_pasta(caminho_pasta):
    if os.path.exists(caminho_pasta):
        shutil.rmtree(caminho_pasta)
    
    os.makedirs(caminho_pasta)

def restaurarBackup(game : Jogo):
    backupDir = game.destino
    backup = arquivo_mais_recente(backupDir)
    
    try:
        limpar_pasta(game.origem)
        shutil.unpack_archive(backup, game.origem)
        toast = nt.notification("Game Save Backup",f"{game.nome_exibicao} restaurado")
        toast.add_actions(
            label="Abrir pasta",
            launch=game.origem
        )
        toast.show()
    except Exception as e:
        log.salvarErroLog(e)