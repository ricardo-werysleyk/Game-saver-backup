#modules
import json
from dataclasses import asdict
import os
import sys

#models
from models.jogo import Jogo

#core
import core.log_handling as log


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(
        base_path,
        relative_path
    )
    
def get_appdata_path(relative_path):
    """Gera o caminho seguro dentro da pasta AppData/Roaming do usuário ativo."""
    # Retorna C:\Users\<Nome>\AppData\Roaming\GameSaveBackup
    base_appdata = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'GameSaveBackup')
    
    # Garante que a pasta do seu aplicativo e a subpasta 'data' existam
    pasta_data = os.path.join(base_appdata, 'data')
    os.makedirs(pasta_data, exist_ok=True)
    
    return os.path.join(base_appdata, relative_path)

JOGOS_CONFIG = get_appdata_path("data/jogos.json")
SETTINGS = get_appdata_path("data/settings.json")
LASTGAME = get_appdata_path("data/lastGame.json")
SETTINGS_PATH = get_appdata_path("data/settings.json")
DATA = get_appdata_path("data")

CONFIG_PADRAO = {
    "iniciar_com_windows": False,
    "iniciar_monitoramento": False,
    "minimizar_para_tray": False,
    "intervalo_monitor_ms": 500,
    "total_backups": 10
}

LASTGAME_PADRAO = {
    "nome": "Game",
    "time": "--"
}

#Função para carregar o arquivo json contendo as informações dos jogos
#{nome: Nome do processo do jogo,origem: diretório origem do save game, destino : diretório onde será salvado o backup compactado}
# {nome, origem, destino}
def carregarJogosJson():
    if not os.path.exists(JOGOS_CONFIG):
        if not os.path.exists(DATA):
            os.mkdir(DATA)
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
        
def carregarSettingsJson():
    if not os.path.exists(SETTINGS):
        if not os.path.exists(DATA):
            os.mkdir(DATA)
        with open(SETTINGS, 'w', encoding='utf-8') as arquivo_json:
            json.dump(CONFIG_PADRAO, arquivo_json)
        
    with open(SETTINGS, 'r', encoding='utf-8') as arquivo:        
        try:
            settings_data = json.load(arquivo)
        except TypeError as e:
            log.salvarErroLog(e)
            
        return settings_data

def salvarSettingsJson(settings):
    with open(SETTINGS, "w",encoding="utf-8") as arquivo:
        json.dump(
            settings,
            arquivo,
            indent=4,
            ensure_ascii=False
        )
        
def salvarLastGameJson(lastGameBk):
    if not os.path.exists(LASTGAME):
        if not os.path.exists(DATA):
            os.mkdir(DATA)
    with open(LASTGAME, "w",encoding="utf-8") as arquivo:
        json.dump(
            lastGameBk,
            arquivo,
            indent=4,
            ensure_ascii=False
        )

def carregarLastGameJson():
    if not os.path.exists(LASTGAME):
        if not os.path.exists(DATA):
            os.mkdir(DATA)
        with open(LASTGAME, 'w', encoding='utf-8') as arquivo_json:
            json.dump(LASTGAME_PADRAO, arquivo_json)
        
    with open(LASTGAME, 'r', encoding='utf-8') as arquivo:        
        try:
            last_game = json.load(arquivo)
        except TypeError as e:
            log.salvarErroLog(e)
            
        return last_game  