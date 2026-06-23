# Game Save Backup

Backup automático de saves de jogos para Windows.

O **Game Save Backup** monitora jogos em execução e cria automaticamente backups compactados dos saves quando o jogo é encerrado.

O objetivo é evitar perda de progresso e tornar o processo de backup totalmente transparente para o jogador.

---

## Beta teste

Utilize o arquivo executável na pasta dist para testar o programa.

## Funcionalidades

### Monitoramento

* Monitoramento automático de processos de jogos
* Detecção de abertura e fechamento do jogo
* Detecção de troca rápida entre jogos

### Backup

* Backup automático ao encerrar o jogo
* Backup manual pela interface
* Compressão automática em `.zip`
* Suporte a múltiplos jogos

### Interface

* Interface gráfica (GUI)
* Adicionar jogos sem editar arquivos manualmente
* Remover jogos diretamente pela aplicação
* Seleção de executável (`.exe`) pelo explorador
* Seleção de diretórios por interface

### Sistema

* Configuração persistida em `jogos.json`
* Notificações nativas do Windows
* Registro automático de erros
* Baixo consumo de memória

---

## Demonstração

Fluxo básico:

```text
Selecionar jogo
↓
Selecionar pasta de save
↓
Selecionar pasta de backup
↓
Iniciar monitoramento
↓
Jogar normalmente
↓
Fechar jogo
↓
Backup criado automaticamente
```

---

## Estrutura do projeto

```text
GameSaveBackup/
│
├── main.py
│
├── core/
│   ├── backup.py
│   ├── arquive_handling.py
│   ├── notifications.py
│   ├── log_handling.py
│
├── gui/
│   └── main_window.py
│
├── models/
│   ├── monitor.py
│   └── jogo.py
│
├── data/
│   └── jogos.json
│
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
pip install -r requirements.txt
```

Execute:

```bash
python main.py
```

---

## Configuração

Agora não é mais necessário editar arquivos manualmente.

Pela interface:

1. Clique em **Selecionar executável**
2. Escolha o `.exe` do jogo
3. Selecione a pasta do save
4. Escolha o diretório de backup
5. Clique em **Adicionar jogo**
6. Inicie o monitoramento

Os dados serão salvos automaticamente em:

```text
data/jogos.json
```

---

## Arquivo de configuração

Exemplo de `jogos.json`:

```json
[
    {
        "nome": "Valheim.exe",
        "origem": "C:/Users/User/AppData/LocalLow/IronGate/Valheim",
        "destino": "D:/GameBackups/Valheim"
    },
    {
        "nome": "SpaceEngineers.exe",
        "origem": "C:/Save",
        "destino": "D:/Backups"
    }
]
```

---

## Logs

Erros encontrados durante execução são registrados automaticamente.

Local:

```text
data/logs/log_erro.txt
```

Formato:

```text
[18-06-2026 21-35-10]

FileNotFoundError:
Arquivo não encontrado
```

---

## Tecnologias utilizadas

* Python
* tkinter
* psutil
* winotify
* json
* zipfile

---

## Roadmap

### v1.1 (Atual)

* [x] Interface gráfica
* [x] Configuração via GUI
* [x] jogos.txt → jogos.json
* [x] Lista de jogos monitorados
* [x] Backup manual
* [x] Logs automáticos
* [x] Seleção de diretórios
* [x] Seleção automática do executável

---

### v1.2

* [X] Executar em segundo plano
* [X] Histórico de backups
* [X] Ícone na bandeja
* [X] Display de status
* [X] Configurações persistentes
* [X] Minimizar para tray

---

### v2.0

* [ ] Inicializar junto com Windows
* [ ] Backup incremental
* [X] Restaurar backups
* [ ] Detectar alteração de save
* [ ] Compactação configurável

---

## Licença

Distribuído sob licença MIT.

---

Feito com Python para nunca perder um save novamente.
