import psutil
import os
import time
import msvcrt
import backup as bk
from dataclasses import dataclass
from typing import Optional
from winotify import Notification
from datetime import datetime
import traceback


#Variáveis globais
PROCESSO = psutil.Process(os.getpid())
jogando = False

@dataclass(slots=True)
class Jogo:
    nome: Optional[str] = None
    origem: Optional[str] = None
    destino: Optional[str] = None
    
    @property
    def nome_exibicao(self):
        if self.nome:
            return self.nome.removesuffix(".exe")
        return ""

jogoAtual = Jogo()
ultimoJogo = Jogo()

#Função para carregar o arquivo de texto contendo as informações dos jogos separados por vírgula
#Nome do processo do jogo, diretório origem do save game e diretório onde será salvado o backup compactado
# nome, origem, destino
def carregarJogosTxt():
    with open('jogos.txt', 'r', encoding='utf-8') as arquivo:
        return [
            Jogo(*linha.strip().split(",", maxsplit=2)) 
            for linha in arquivo
        ]
        
def salvarErroLog(erro):
    currentTime = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    nome_arquivo = "log_erro.txt"
    with open(nome_arquivo, "a", encoding="utf-8") as arquivo:
        arquivo.write(
            f"\n[{currentTime}]\n"
        )

        arquivo.write(
            f"{type(erro).__name__}: {erro}\n"
        )

        arquivo.write(
            traceback.format_exc()
        )

        arquivo.write(
            "\n-----------------\n"
        )

    print(f"Arquivo salvo com sucesso em: {nome_arquivo}")

#Função geral de notificação do windows
def notification(titulo : str,mensagem : str):
    return Notification(
        app_id="Game Save Backup",
        title=titulo,
        msg=mensagem
    )

#Função responsável por fazer o backup do save
#@params game: nome do processo do jogo, origem: diretório raiz do save, destino: diretório de backup
def backupStart(game : Jogo):
    try:
        bk.makeBackup(game.origem,game.destino)
        toast = notification("Game Save Backup",f"{game.nome_exibicao} salvo")
        toast.add_actions(
            label="Abrir pasta",
            launch=game.destino
        )
        toast.show()
    except Exception as e:
        salvarErroLog(e)

#Função responsável por varrer os processos em aberto do gerenciador de tafera do windows
#Para ser mais eficiente, precarrega apenas o nome de todos os processos e retorna um conjunto (set)
def varrerProcessos():
    processos = {
        p.info["name"].lower()
        for p in psutil.process_iter(
            ["name"]
        )
        if p.info["name"]
    }
    return processos

#Função responsável por verificar se algum jogo do arquivo jogos.txt está com processo aberto
def verificaJogoAberto(processos):    
    for jogo in jogos:
        if jogo.nome.lower() in processos:
            return True, jogo
    
    return False, Jogo()

notification("Monitor iniciado","Monitorando jogos").show()
jogos = carregarJogosTxt()

while True:    
    processos = varrerProcessos()    
    jogoAberto, jogoAtual = verificaJogoAberto(processos)

    #Comparativo responsável por evitar que não faça o backup caso o jogo seja trocado
    #mais rápido que o tempo de processamento do programa
    if jogoAberto and ultimoJogo.nome:
        if jogoAtual.nome != ultimoJogo.nome:
            print("Iniciando backup.")
            backupStart(ultimoJogo)
            ultimoJogo = jogoAtual

    #Lógica de detecção de jogo aberto e se fechou
    if jogoAberto and not jogando:
        print(f"Jogo {jogoAtual.nome_exibicao} iniciou")
        print(f"Pasta origem: {jogoAtual.origem}")
        print(f"Pasta destino: {jogoAtual.destino}")
        jogando = True
        ultimoJogo = jogoAtual
    elif not jogoAberto and jogando:
        print("Jogo fechou")
        print("Iniciando backup.")
        backupStart(ultimoJogo)
        ultimoJogo = Jogo()
        jogando = False

    status = (
        f"Jogando: {jogoAtual.nome_exibicao}"
        if jogando
        else "Aguardando..."
    )

    print(status)
    print("Monitorando...")
    print("Pressione 'F' para encerrar programa.")
    
    # Verifica se alguma tecla foi apertada
    if msvcrt.kbhit():
        tecla = msvcrt.getch()
        if tecla.lower() == b'f':
            print("\nEncerrando monitoramento...")
            notification("Monitor encerrado","Backup automático parado").show()
            break
    
    memoria = (
        PROCESSO.memory_info().rss
        / 1024
        / 1024
    )

    print(
        f"Uso RAM: {memoria:.2f} MB"
    )

    time.sleep(10)
    os.system("cls")
