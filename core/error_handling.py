from datetime import datetime
import traceback
import os

def salvarErroLog(erro):
    currentTime = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    nome_arquivo = "logs/log_erro.txt"
    
    os.makedirs(
        "logs",
        exist_ok=True
    )
        
    with open(nome_arquivo, "a", encoding="utf-8") as arquivo:
        arquivo.write(
            f"\n[{currentTime}]\n"
        )

        arquivo.write(
            f"{type(erro).__name__}: {erro}\n"
        )

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

    print(f"Arquivo salvo com sucesso em: {nome_arquivo}")