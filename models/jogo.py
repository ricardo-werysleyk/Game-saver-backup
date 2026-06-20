from dataclasses import dataclass
from typing import Optional

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