import psutil
from copy import copy
import os

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
        self.PROCESSO = psutil.Process(os.getpid())

    def memoria_consumida(self):
        return (
            self.PROCESSO.memory_info().rss
            / 1024
            / 1024
        )
    
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
    
    def verificaJogoJson(self, jogo_verif):
        return  any(
            jogo == jogo_verif
            for jogo in self.jogos
        )
    
    def salvarJogoNovo(self, novo_jogo: Jogo):
        existe = self.verificaJogoJson(novo_jogo)

        if existe:
            return False

        self.jogos.append(
            novo_jogo
        )

        arquive.salvarJogosJson(
            self.jogos
        )

        return True
        
    def removerJogo(self, jogo_rmv):
        existe = self.verificaJogoJson(jogo_rmv)
        
        if not existe:
            return False
        
        self.jogos.remove(
            jogo_rmv
        )

        arquive.salvarJogosJson(
            self.jogos
        )
        
        return True
    
    def forcarBackup(self, jogo_bk):
        existe = self.verificaJogoJson(jogo_bk)
        if existe:
            bk.backupStart(jogo_bk)
    
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
                self.ultimoJogo = copy(self.jogoAtual)
    
    def verificarFechamento(self):
        #Lógica de detecção de jogo aberto e se fechou
        if self.jogoAberto and not self.jogando:
            self.jogando = True
            self.ultimoJogo = copy(self.jogoAtual)
        elif not self.jogoAberto and self.jogando:
            print("Iniciando backup.")
            self.gameBackup()
            self.ultimoJogo = self.JOGO_VAZIO
            self.jogando = False
    
    def obterEstado(self):
        return {
            "jogando": self.jogando,
            "status": (
                f"Jogando: {self.jogoAtual.nome_exibicao}"
                if self.jogando
                else "Aguardando..."
            ),
            "jogo": self.jogoAtual
        }
    
    def executar(self):
        self.jogoAberto, self.jogoAtual = self.verificaJogoAberto()        
        self.verificarTrocaJogo()
        self.verificarFechamento()
        
        return self.obterEstado()
        
        