# Game Save Backup

Backup automático de saves de jogos no Windows utilizando Python.

O programa monitora processos em execução e, ao detectar que um jogo foi fechado, cria automaticamente um backup compactado do diretório de save configurado.

## Funcionalidades

* Monitoramento automático de jogos em execução
* Backup automático ao fechar o jogo
* Backup compactado (.zip)
* Suporte a múltiplos jogos
* Configuração simples via arquivo `jogos.txt`
* Notificações nativas do Windows
* Baixo consumo de memória
* Registro automático de erros em arquivo de log

---

## Como funciona

O programa verifica periodicamente os processos em execução.

Quando detecta:

* Jogo iniciou → apenas monitora
* Jogo fechou → gera backup do save automaticamente

Também detecta troca rápida entre jogos sem perder backups.

---

## Estrutura

```txt
project/
│
├── main.py
├── backup.py
├── jogos.txt
└── README.md
```

---

## Instalação

Clone o repositório:

```bash
git clone <url-do-repositorio>
cd GameSaveBackup
```

Instale dependências:

```bash
pip install psutil winotify
```

Execute:

```bash
python main.py
```

---

## Configuração

Edite o arquivo `jogos.txt`.

Formato:

```txt
processo.exe,caminho_save,caminho_backup
```

Exemplo:

```txt
eurotrucks2.exe,C:\Users\User\Documents\Euro Truck Simulator 2\profiles,D:\Backup_games\ETS2

SpaceEngineers.exe,C:\Users\User\AppData\Roaming\SpaceEngineers\Saves,D:\Backup_games\SpaceEngineers
```

---

## Uso

Execute o programa.

Ao fechar um jogo monitorado:

* o save será compactado;
* uma notificação aparecerá no Windows;
* será possível abrir diretamente a pasta do backup.

Para encerrar:

```txt
Pressione F
```

---

## Tecnologias

* Python
* psutil
* winotify
* shutil

---

## Roadmap

### v1.1

* [ ] Histórico de backups
* [ ] Arquivo de logs
* [ ] Ignorar linhas inválidas do jogos.txt
* [ ] Não gerar backup se save não mudou

### v1.2

* [ ] Executar em segundo plano
* [ ] Inicializar junto com Windows
* [ ] Ícone na bandeja do sistema

### v2.0

* [ ] Interface gráfica
* [ ] Configuração sem editar arquivos
* [ ] Backup incremental
* [ ] Restaurar backups
* [ ] Forçar backups

---

## Licença

MIT
