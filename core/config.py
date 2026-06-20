import json

CONFIG = "data/config.json"

def carregar():
    with open(CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar(dados):
    with open(CONFIG, "w", encoding="utf-8") as f:
        json.dump(
            dados,
            f,
            indent=4,
            ensure_ascii=False
        )
