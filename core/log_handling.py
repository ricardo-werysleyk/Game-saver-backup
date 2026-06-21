from datetime import datetime
import traceback
import os

def preLog():
    os.makedirs("logs", exist_ok=True)
    return datetime.now().strftime("%d-%m-%Y %H-%M-%S")

def salvarErroLog(erro):
    currentTime = preLog()
    nome_arquivo = "logs/log_erro.txt"
        
    with open(nome_arquivo, "a", encoding="utf-8") as arquivo:
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
    nome_arquivo = "logs/log_backup.txt"
        
    with open(nome_arquivo, "a", encoding="utf-8") as arquivo:
        arquivo.write(
            f"\n[{currentTime}]\n"
        )
        arquivo.write("Backup feito com sucesso.")
        arquivo.write(f"{jogo}")
        arquivo.write(
            "\n-----------------\n"
        )