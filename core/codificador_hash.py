import os
import hashlib

def calcular_hash_pasta(caminho_save):
    if not os.path.exists(caminho_save):
        return None

    hash_global = hashlib.md5()

    for raiz, _, arquivos in os.walk(caminho_save):
        for arquivo in sorted(arquivos):
            caminho_completo = os.path.join(raiz, arquivo)            
            try:
                with open(caminho_completo, "rb") as f:
                    for bloco in iter(lambda: f.read(4096), b""):
                        hash_global.update(bloco)
            except (PermissionError, FileNotFoundError):
                continue

    return hash_global.hexdigest()