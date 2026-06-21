#modules
import json
from dataclasses import asdict
import os

#models
from models.jogo import Jogo

#core
import core.log_handling as log

JOGOS_CONFIG = "data/jogos.json"

#Função para carregar o arquivo json contendo as informações dos jogos
#{nome: Nome do processo do jogo,origem: diretório origem do save game, destino : diretório onde será salvado o backup compactado}
# {nome, origem, destino}
def carregarJogosJson():
    if not os.path.exists("data"):
        os.mkdir("data")
        with open(JOGOS_CONFIG, 'w', encoding='utf-8') as arquivo_json:
            json.dump({}, arquivo_json)
        
    with open(JOGOS_CONFIG, 'r', encoding='utf-8') as arquivo:
        game_data = json.load(arquivo)
        jogos = []
        for game in game_data:
            try:
                jogos.append(Jogo(**game))
            except TypeError as e:
                log.salvarErroLog(e)
            
        return jogos

#Função por salvar o arquivo json contendo as informações dos jogos
def salvarJogosJson(jogos):
    with open(JOGOS_CONFIG, "w",encoding="utf-8") as arquivo:
        json.dump(
            [asdict(jogo) for jogo in jogos],
            arquivo,
            indent=4,
            ensure_ascii=False
        )