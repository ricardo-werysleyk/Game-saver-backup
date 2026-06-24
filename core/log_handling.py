from datetime import datetime
import traceback
import os

def get_appdata_path_log(relative_path):
    """Gera o caminho seguro dentro da pasta AppData/Roaming do usuário ativo."""
    # Retorna C:\Users\<Nome>\AppData\Roaming\GameSaveBackup
    base_appdata = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'GameSaveBackup')
    
    # Garante que a pasta do seu aplicativo e a subpasta 'data' existam
    pasta_data = os.path.join(base_appdata, 'logs')
    os.makedirs(pasta_data, exist_ok=True)
    
    return os.path.join(base_appdata, relative_path)

LOGS = get_appdata_path_log("logs")
LOG_ARQUIVE = get_appdata_path_log("logs/log_erro.txt")
LOG_BACKUP = get_appdata_path_log("logs/log_backup.txt")

def preLog():
    os.makedirs(LOGS, exist_ok=True)
    return datetime.now().strftime("%d-%m-%Y %H-%M-%S")

def salvarErroLog(erro):
    currentTime = preLog()
        
    with open(LOG_ARQUIVE, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"\n[{currentTime}]\n")
        arquivo.write(f"{type(erro).__name__}: {erro}\n")
        arquivo.write(
            "".join(
                traceback.format_exception(
                    type(erro),
                    erro,
                    erro.__traceback__
                )
            )
        )
        arquivo.write(
            "\n-----------------\n"
        )

def salvarBackupLog(jogo):
    currentTime = preLog()
        
    with open(LOG_BACKUP, "a", encoding="utf-8") as arquivo:
        arquivo.write(
            f"\n[{currentTime}]\n"
        )
        arquivo.write("Backup feito com sucesso.")
        arquivo.write(f"{jogo}")
        arquivo.write(
            "\n-----------------\n"
        )