#modules
import json

#models
from models.jogo import Jogo

#core
import core.error_handling as error

JOGOS_CONFIG = "data/jogos.json"

#Função para carregar o arquivo json contendo as informações dos jogos
#{nome: Nome do processo do jogo,origem: diretório origem do save game, destino : diretório onde será salvado o backup compactado}
# {nome, origem, destino}
def carregarJogosJson():
    with open(JOGOS_CONFIG, 'r', encoding='utf-8') as arquivo:
        game_data = json.load(arquivo)
        jogos = []
        for game in game_data:
            try:
                jogos.append(Jogo(**game))
            except TypeError as e:
                error.salvarErroLog(e)
            
        return jogos