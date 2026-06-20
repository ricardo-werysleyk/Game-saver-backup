import psutil

import core.arquive_handling as arquive
import core.backup as bk
from models.jogo import Jogo


class Monitor:  
    
    def __init__(self):
        self.jogos = arquive.carregarJogosJson()
        self.JOGO_VAZIO = Jogo()
        self.jogoAtual = Jogo()
        self.ultimoJogo = Jogo()
        self.jogoAberto = False
        self.jogando = False

    #Função responsável por varrer os processos em aberto do gerenciador de tafera do windows
    #Para ser mais eficiente, precarrega apenas o nome de todos os processos e retorna um conjunto (set)
    def varrerProcessos(self):
        processos = {
            p.info["name"].lower()
            for p in psutil.process_iter(
                ["name"]
            )
            if p.info["name"]
        }
        return processos
    
    #Função responsável por verificar se algum jogo do arquivo jogos.txt está com processo aberto
    def verificaJogoAberto(self):   
        processos = self.varrerProcessos()
        for jogo in self.jogos:
            if jogo.nome.lower() in processos:
                return True, jogo
        
        return False, self.JOGO_VAZIO
    
    def gameBackup(self):
        bk.backupStart(self.ultimoJogo)
    
    def verificarTrocaJogo(self):
        #Comparativo responsável por evitar que não faça o backup caso o jogo seja trocado
        #mais rápido que o tempo de processamento do programa
        if  (
            self.jogoAberto 
            and self.ultimoJogo.nome 
            and self.jogoAtual.nome != self.ultimoJogo.nome
            ):
                print("Iniciando backup.")
                self.gameBackup()
                self.ultimoJogo = self.jogoAtual
    
    def verificarFechamento(self):
        #Lógica de detecção de jogo aberto e se fechou
        if self.jogoAberto and not self.jogando:
            self.jogando = True
            self.ultimoJogo = self.jogoAtual
        elif not self.jogoAberto and self.jogando:
            print("Iniciando backup.")
            self.gameBackup()
            self.ultimoJogo = self.JOGO_VAZIO
            self.jogando = False
    
    def obterEstado(self):
        status = (
            f"Jogando: {self.jogoAtual.nome_exibicao}"
            if self.jogando
            else "Aguardando..."
        )
        return status
    
    def executar(self):
        self.jogoAberto, self.jogoAtual = self.verificaJogoAberto()        
        self.verificarTrocaJogo()
        self.verificarFechamento()
        
        return {
            "jogando": self.jogando,
            "status": self.obterEstado(),
            "jogo": self.jogoAtual
        }