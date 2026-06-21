import tkinter as tk
from models.jogo import Jogo
import core.notifications as nt
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import os


class App:

    def __init__(self, monitor):
        
        #variáveis globais
        self.monitor = monitor
        self.monitorando = False
        self.tempoProcessamento = 100
        
        #Style
        self.root = tk.Tk()
        
        self.style = ttk.Style()
        self.style.theme_use("alt")
        #Dark theme
        self._primaryColor = "#23272d"
        self._secundaryColor = "#33373c"
        self.btnColor = "#42444d"
        self.fontColor = "#E3E3E3"
        
        self.style.configure(
            "Custom.Vertical.TScrollbar",
            troughcolor=self._primaryColor,     # Cor do canal/pista de fundo
            background=self.btnColor,           # Cor da barra que se move (slider)
            arrowcolor=self._secundaryColor,    # Cor das setas para cima/baixo
            gripcount=0                         # Remove linhas de textura extras
        )        
        # Altera o padrão de todos os tk.Entry que forem criados no projeto
        # self.root.option_add("*Entry.selectBackground", self._primaryColor)
        self.root.option_add("*Entry.selectForeground", self._primaryColor)
        
        #Configurações gerais da root
        self.root.title("Game Save Backup")
        self.root.geometry("480x528")
        self.root.config(bg=self._primaryColor)
        self.root.option_add("*Foreground", self.fontColor)
        self.root.columnconfigure(0, weight=1)
        # self.root.columnconfigure(1, weight=1)
        
        #Frame que engloba as statísticas e botões de ação iniciar e parar monitoramento
        self.stats_frame = tk.Frame(self.root, relief="solid")
        self.stats_frame.grid(row=0, column=0,columnspan=2 ,sticky="ew", padx=20, pady=10)
        self.stats_frame.config(bg=self._primaryColor)
        self.stats_frame.columnconfigure(0, weight=1)
        self.stats_frame.columnconfigure(1, weight=1)
        
        #Label de status
        self.label_status = tk.Label(
            self.stats_frame,
            text="Status: Parado",
            bg=self._primaryColor
        )
        self.label_status.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=10
        )
        #Label que indica o estado de monitoramento
        self.label_monitor = tk.Label(
            self.stats_frame,
            text="Monitor: Desligado",
            bg=self._primaryColor
        )
        self.label_monitor.grid(
            row=1,
            column=0,
            columnspan=2
        )
        #Label que indica uso de memória RAM
        self.label_ram = tk.Label(
            self.stats_frame,
            text="Uso RAM: -- MB",
            bg=self._primaryColor
        )
        self.label_ram.grid(
            row=2,
            column=0,
            columnspan=2
        )
        #Botão de iniciar o monitoramento de jogos
        self.btn_iniciar = tk.Button(
            self.stats_frame,
            text="Iniciar",
            command=self.iniciar,
            bg=self.btnColor
        )
        self.btn_iniciar.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=10,
            pady=20
        )
        #Botão de para o monitoramento de jogos
        self.btn_parar = tk.Button(
            self.stats_frame,
            text="Parar",
            command=self.parar,
            bg=self.btnColor
        )
        self.btn_parar.grid(
            row=3,
            column=1,
            sticky="ew",
            padx=10
        )        
        
        #Frame dos inputs nome, origem e destino
        self.inputs_frame = tk.Frame(self.root, relief="solid")
        self.inputs_frame.grid(row=1, column=0,columnspan=2 ,sticky="ew", padx=20, pady=10)
        self.inputs_frame.config(bg=self._primaryColor)
        self.inputs_frame.columnconfigure(0, weight=1)
        self.inputs_frame.columnconfigure(1, weight=8)
        self.inputs_frame.columnconfigure(2, weight=1)
        
        #Label do nome, input e botão de buscar em arquivos.
        self.label_nome_jogo_inputs_frame = tk.Label(
            self.inputs_frame,
            text="Nome:",
            bg=self._primaryColor
        )
        self.label_nome_jogo_inputs_frame.grid(
            row=0,
            column=0,
            pady=10
        )
        
        #input que recebe o nome do executável do jogo
        self.entry_nome = tk.Entry(self.inputs_frame)
        self.entry_nome.insert(0, " [ Ex: Valheim.exe ]")
        self.entry_nome.config(bg=self._secundaryColor)
        self.entry_nome.grid(
            row=0,
            column=1,
            sticky="ew",
            pady=2,
            ipady=3
        )
        
        #botão que busca executável do jogo nos arquivos
        self.btn_exe = tk.Button(
            self.inputs_frame,
            text="📂",
            command=self.selecionarExecutavel,
            bg=self.btnColor
        )
        self.btn_exe.grid(
            row=0,
            column=2,
            sticky="w",
            padx=4
        )
        
        #Label da origem, input e botão de buscar em arquivos.
        self.label_origem_jogo_inputs_frame = tk.Label(
            self.inputs_frame,
            text="Origem:",
            bg=self._primaryColor
        )
        self.label_origem_jogo_inputs_frame.grid(
            row=1,
            column=0,
            pady=10
        )

        #input que recebe o path da pasta do save do game
        self.entry_origem = tk.Entry(self.inputs_frame)
        self.entry_origem.insert(0, " [ Selecione pasta save ]")
        self.entry_origem.config(bg=self._secundaryColor)
        self.entry_origem.grid(
            row=1,
            column=1,
            sticky="ew",
            pady=2,
            ipady=3
        )
        
        #botão que seleciona a pasta do save do game
        self.btn_origem = tk.Button(
            self.inputs_frame,
            text="📂",
            command=lambda:
                self.selecionarDiretorio(
                    self.entry_origem
                ),
            bg=self.btnColor
        )
        self.btn_origem.grid(
            row=1,
            column=2,
            sticky="w",
            padx=4
        )
        
        #Label do destino, input e botão de buscar em arquivos.
        self.label_destino_jogo_inputs_frame = tk.Label(
            self.inputs_frame,
            text="Destino:",
            bg=self._primaryColor
        )
        self.label_destino_jogo_inputs_frame.grid(
            row=2,
            column=0,
            pady=10
        )

        #input que recebe o path da pasta de backup
        self.entry_destino = tk.Entry(self.inputs_frame)
        self.entry_destino.insert(0, " [ Selecione pasta backup ]")
        self.entry_destino.config(bg=self._secundaryColor)
        self.entry_destino.grid(
            row=2,
            column=1,
            sticky="ew",
            pady=2,
            ipady=3
        )
        
        #botão que seleciona a pasta de backup do savegame
        self.btn_destino = tk.Button(
            self.inputs_frame,
            text="📂",
            command=lambda:
                self.selecionarDiretorio(
                    self.entry_destino
                ),
            bg=self.btnColor
        )
        self.btn_destino.grid(
            row=2,
            column=2,
            sticky="w",
            padx=4
        )
        
        #Botão de adicionar game a jogo.json
        self.btn_adicionar = tk.Button(
            self.inputs_frame,
            text="Adicionar jogo",
            command=self.adicionar,
            bg=self.btnColor
        )
        self.btn_adicionar.grid(
            row=3,
            column=1,
            sticky="ew"
        )
        
        #Frame da lista de jogos cadastrados e botões de ação: Abrir save, Abrir backup, Fazer backup e Remover
        self.lista_jogos_frame = tk.Frame(self.root, relief="solid")
        self.lista_jogos_frame.grid(row=2, column=0,columnspan=2 ,sticky="ew", padx=20, pady=10)
        self.lista_jogos_frame.config(bg=self._primaryColor)
        self.lista_jogos_frame.columnconfigure(0, weight=1)
        self.lista_jogos_frame.columnconfigure(1, weight=1)
        self.lista_jogos_frame.columnconfigure(2, weight=0)        
        self.lista_jogos_scrollbar = ttk.Scrollbar(self.lista_jogos_frame, orient="vertical", style="Custom.Vertical.TScrollbar")
        self.lista_jogos_scrollbar.grid(row=0, column=2, sticky="ns")

        #Lista de jogos em jogos.json
        self.lista = tk.Listbox(
            self.lista_jogos_frame,
            height=5,
            yscrollcommand=self.lista_jogos_scrollbar.set,
            # selectbackground=self._primaryColor,   # Cor de fundo quando selecionado
            selectforeground=self._primaryColor   
        )
        self.lista.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew"
        )
        self.lista.config(bg=self._primaryColor)
        self.lista_jogos_scrollbar.config(command=self.lista.yview)
        
        #Botão que abri pasta do savegame de jogo selecionado na lista
        self.btn_abrir_origem = tk.Button(
            self.lista_jogos_frame,
            text="📂 Abrir save",
            command=self.abrirOrigem,
            pady=2,
            padx=6,
            compound="left",
            anchor="center",
            bg=self.btnColor
        )
        self.btn_abrir_origem.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=5,
            padx=2
        )
        
        #Botão de forçar backup de jogo selecionado na lista
        self.btn_backup_now = tk.Button(
            self.lista_jogos_frame,
            text="💾 Fazer backup",
            command=self.fazerBackup,
            pady=2,
            padx=6,
            compound="left",
            anchor="center",
            bg=self.btnColor
        )
        self.btn_backup_now.grid(
            row=2,
            column=1,
            sticky="ew",
            pady=5,
            padx=2
        )
        
        #Botão que abri pasta do backup do jogo selecionado na lista
        self.btn_abrir_destino = tk.Button(
            self.lista_jogos_frame,
            text="📂 Abrir backup",
            command=self.abrirDestino,
            pady=2,
            padx=6,
            compound="left",
            anchor="center",
            bg=self.btnColor
        )
        self.btn_abrir_destino.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=5,
            padx=2
        )
        
        #Botão de remover jogo selecionado do jogos.json
        self.btn_remover = tk.Button(
            self.lista_jogos_frame,
            text="🗑 Remover",
            command=self.remover,
            pady=2,
            padx=6,
            compound="left",
            anchor="center",
            bg=self.btnColor
        )
        self.btn_remover.grid(
            row=3,
            column=1,
            sticky="ew",
            pady=5,
            padx=2
        )        
        
        self.atualizarLista()
    
    def atualizaLabelMonitor(self):
        self.label_monitor.config(text=f"Monitor: {'Ligado' if self.monitorando else 'Desligado'}")
        if self.monitorando:
            self.btn_iniciar.config(
                state="disabled"
            )
            self.btn_parar.config(
                state="normal"
            )
        else:
            self.btn_parar.config(
                state="disabled"
            )
            self.btn_iniciar.config(
                state="normal"
            )
    
    def atualizaLabelRam(self):
        memoria = self.monitor.memoria_consumida()
        self.label_ram.config(text=f"Uso RAM: {memoria:.2f} MB")

    #Função do botão iniciar monitoramento
    def iniciar(self):        
        if self.monitorando:
            return
        
        nt.notification("Monitor iniciado","Monitorando jogos").show()
        self.monitorando = True
        self.atualizaLabelMonitor()
        self.loopMonitor()
        
    #Função do botão parar monitoramento
    def parar(self):
        self.monitorando = False
        nt.notification("Monitor encerrado","Backup automático parado").show()
        self.label_status.config(text="Status: Parado")
        self.atualizaLabelMonitor()
    
    
    def atualizarStatusInterface(self, estado):
        self.label_status.config(
            text=estado["status"]
        )
    
    def selecionarExecutavel(self):
        caminho = filedialog.askopenfilename(
            filetypes=[
                (
                    "Executáveis",
                    "*.exe"
                )
            ]
        )

        if caminho:
            nome = os.path.basename(caminho)
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, nome)
            
    def selecionarDiretorio(self,campo):
        pasta = filedialog.askdirectory()
        if pasta:
            campo.delete(0,tk.END)
            campo.insert(0, pasta)
    
    #Função chamada pelo botão adicionar jogo, adiciona jogo a lista jogos.json
    def adicionar(self):
        origemValida = os.path.isdir(self.entry_origem.get())
        destinoValido = os.path.isdir(self.entry_destino.get())
        
        if origemValida and destinoValido:
            jogo = Jogo(
                nome=self.entry_nome.get(),
                origem=self.entry_origem.get(),
                destino=self.entry_destino.get()
            )
            
            salvo_sucesso = self.monitor.salvarJogoNovo(jogo)
            if salvo_sucesso:
                self.atualizarLista()
                
                messagebox.showinfo(
                    "Sucesso",
                    "Jogo salvo"
                )
                self.entry_nome.delete(0, tk.END)
                self.entry_origem.delete(0, tk.END)
                self.entry_destino.delete(0, tk.END)
                self.entry_nome.insert(0, " [ Ex: Valheim.exe ]")
                self.entry_origem.insert(0, " [ Selecione pasta save ]")
                self.entry_destino.insert(0, " [ Selecione pasta backup ]")
            else:
                messagebox.showinfo(
                    "Falha",
                    "Jogo já configurado"
                ) 
        else:
            messagebox.showinfo(
                "Falha",
                "Diretório inválido"
            )        
    
    #Atualiza lista de jogos de acordo com jogos.json
    def atualizarLista(self):
        self.lista.delete(0, tk.END)
        
        for jogo in self.monitor.jogos:
            self.lista.insert(tk.END, f"  {jogo.nome_exibicao}")
    
    def verificaJogoLista(self):
        indice = (self.lista.curselection())

        if not indice:
            return

        return (self.monitor.jogos[indice[0]])
    
    def remover(self):
        jogo = self.verificaJogoLista()
        
        response = messagebox.askyesno("Remover jogo", "Remover o jogo da lista?")
        
        if response:
            self.monitor.removerJogo(jogo)

            self.atualizarLista()        
            messagebox.showinfo(
                "Sucesso",
                "Jogo removido"
            )
        
    def fazerBackup(self):
        jogo = self.verificaJogoLista()
        self.monitor.forcarBackup(jogo)
    
    def abrirOrigem(self):
        jogo = self.verificaJogoLista()        
        os.startfile(os.path.normpath(jogo.origem))
    
    def abrirDestino(self):
        jogo = self.verificaJogoLista()        
        os.startfile(os.path.normpath(jogo.destino))
        
    def loopMonitor(self):
        if not self.monitorando:
            self.label_ram.config(text="Uso RAM: -- MB")
            return

        self.atualizaLabelRam()
        estado = self.monitor.executar()

        self.atualizarStatusInterface(estado)

        self.root.after(self.tempoProcessamento, self.loopMonitor)

    def executar(self):
        self.atualizaLabelMonitor()
        self.root.mainloop()