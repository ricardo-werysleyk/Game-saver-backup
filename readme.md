# 🎮 Game Saver Backup v2.0

O **Game Save Backup** é uma ferramenta leve para Windows que monitora seus jogos em execução e cria cópias de segurança (.zip) automáticas dos seus saves assim que ocerrem mudanças neles. Nunca mais perca seu progresso por culpa de saves corrompidos, falhas no sistema, queda de energia ou crash de mods!

---

## Como Instalar (Simples e Rápido)

Não precisa instalar o Python para jogar. Siga os passos abaixo:

1. Baixe o instalador oficial do programa clicando em **[[Link/Seção de Releases do seu GitHub](https://github.com/ricardo-werysleyk/Game-saver-backup/releases/tag/GameSaverBk2)]** (ou execute o arquivo `setup.exe` fornecido).
2. Siga as instruções do assistente de instalação na tela.
3. Pronto! O programa criará um atalho diretamente na sua **Área de Trabalho**.

---

## Como Configurar seu Primeiro Jogo

Configurar o monitoramento leva menos de 1 minuto:

1. **Selecione o Jogo**: Clique em *Selecionar executável* e escolha o arquivo `.exe` principal do seu jogo.
2. **Pasta do Save**: Indique a pasta original onde o jogo salva o seu progresso (Ex: dentro de `Documents` ou `AppData`).
3. **Pasta de Backup**: Escolha qualquer pasta do seu computador (ou HD Externo/Drive na Nuvem) onde quer guardar as cópias seguras.
4. **Adicione**: Clique em *Adicionar jogo* e depois em *Iniciar monitoramento*.

*Agora você pode jogar normalmente. Assim que alterações forem detectadas, o backup surgirá na pasta de destino de forma 100% silenciosa!*

---

## Funcionalidades Principais

* **Totalmente Automatizado**: Detecta sozinho quando o jogo abre e fecha.
*  **Compactação Inteligente**: Salva os arquivos estruturados em arquivos `.zip` para economizar espaço.
*  **Segundo Plano (System Tray)**: Minimize o aplicativo para a barra de tarefas (perto do relógio do Windows) para não atrapalhar sua jogatina.
*  **Múltiplos Jogos**: Monitore quantos jogos você quiser ao mesmo tempo.
*  **Inicialização com o Windows**: Configure o app para abrir junto com o sistema operacional e garanta que nenhum jogo fique sem proteção.

---

## Onde ficam salvas minhas configurações?

Para garantir estabilidade e rodar sem a necessidade de privilégios de Administrador no Windows, seus dados de configuração e logs de erros ficam guardados de forma isolada e segura na sua pasta de usuário:

📂 **Caminho**: `C:\Users\SEU_USUARIO\AppData\Roaming\GameSaveBackup\`

---

# Guia de Desenvolvimento (v2.0)

Este é o guia técnico para desenvolvedores que desejam clonar, modificar, compilar ou contribuir com o projeto **Game Save Backup**.

O projeto foi desenvolvido em **Python** utilizando **Tkinter** para a interface gráfica e **psutil** para a monitoração de processos assíncronos do Windows.

---

## Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:
* Python 3.10 ou superior
* Gerenciador de pacotes `pip`
* **Inno Setup Compiler** (opcional, necessário apenas se quiser gerar o instalador `.exe`)

---

## Configuração do Ambiente de Desenvolvimento

Siga os passos abaixo para clonar o repositório e configurar o ambiente virtual:

1. **Clone o repositório:**
   ```bash
   git clone https://github.com
   cd Game-saver-backup
   ```

2. **Crie e ative um ambiente virtual (Recomendado):**
   ```bash
   python -m venv venv
   # No Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # No Windows (CMD):
   .\venv\Scripts\activate.bat
   ```

3. **Instale as dependências do projeto:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o projeto em modo de desenvolvimento:**
   ```bash
   python main.py
   ```

---

## Estrutura de Diretórios

O projeto segue uma arquitetura modular estruturada da seguinte forma:

```text
GameSaveBackup/
├── main.py            # Ponto de entrada da aplicação
├── main.spec          # Arquivo de configuração do PyInstaller
├── core/              # Módulos principais de lógica de negócios
│   ├── backup.py           # Lógica de compressão e backup em .zip
│   ├── arquive_handling.py # Utilitários de manipulação de sistema de arquivos
│   ├── notifications.py    # Integração com winotify (Notificações do Windows)
│   └── log_handling.py     # Escrita de logs de erros assíncronos
├── gui/               # Telas e componentes visuais
│   └── main_window.py     # Interface gráfica em Tkinter
├── models/            # Classes de modelagem de dados e threads
│   ├── monitor.py         # Thread de monitoramento do psutil
│   └── jogo.py            # Dataclass do objeto Jogo
└── requirements.txt   # Lista de dependências do ecossistema Python
```

---

## Como Compilar e Gerar o Executável

O processo de empacotamento é feito em duas etapas: geração do binário via PyInstaller e empacotamento via Inno Setup.

### Passo 1: Gerar a pasta do Executável com PyInstaller
Execute o comando abaixo na raiz do projeto para criar a pasta distribuível:
```bash
pyinstaller --onedir --windowed --icon=assets/main.ico --name="Game Saver Backup" --add-data "assets;assets" --hidden-import=pystray._win32 --hidden-import=PIL._tkinter_finder main.py
```
*Este comando gerará a pasta `dist/main/` contendo o executável e a pasta interna de dependências `_internal`.*

### Passo 2: Gerar o Instalador do Windows
1. Abra o arquivo de script do **Inno Setup** (`.iss`) do seu instalador.
2. Certifique-se de que a seção `[Files]` aponta corretamente para a pasta `_internal` sem desestruturá-la:
   ```pascal
   [Files]
   Source: ".\(\dist\main\Game\) Saver Backup.exe"; DestDir: "{app}"; Flags: ignoreversion
   Source: ".\dist\main\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs
   ```
3. Compile o script no Inno Setup para gerar o instalador `setup.exe` final.

---

## Persistência e Diretrizes de Escrita

Para respeitar as diretivas de segurança do Windows e evitar erros `PermissionError (Errno 13)`, o software **não grava dados** na pasta de instalação (`C:\Program Files`). 

Toda a persistência de estados (`jogos.json`, `settings.json`) e logs são redirecionados dinamicamente para o ambiente isolado do usuário corrente:
* **Destino:** `%APPDATA%\GameSaveBackup\`

---

## Próximos passos

- Estatísticas 
	- Backups realizados: 241  
	- Espaço utilizado: 14 GB  
	- Jogos cadastrados: 8  
	- Tempo monitorando: 214 h
- Salvar na nuvem e compartilhar save entre máquinas

## Licença

Este repositório está sob a licença MIT. Sinta-se à vontade para abrir *Issues* ou enviar *Pull Requests* com melhorias no monitoramento de processos.
