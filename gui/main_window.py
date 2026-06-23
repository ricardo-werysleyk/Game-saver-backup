import tkinter as tk
from models.jogo import Jogo
from models.settings import Settings
import core.notifications as nt
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import os
from core.tray import Tray
import core.backup as bk
import core.startup as startup
import core.arquive_handling as arquive


class App:

    def __init__(self, monitor):
        
        #Settings
        self.config = Settings()
        # self.config.settings["iniciar_com_windows"] = True
        # self.config.salvarConfig(self.config.settings)
        
        #variáveis globais
        self.monitor = monitor
        self.monitorando = self.config.settings["iniciar_monitoramento"]
        self.tray = Tray(self)
        self.iniciarMinimizado = self.config.settings["minimizar_para_tray"]
        
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
        
        self.icone = tk.PhotoImage(
            file=arquive.resource_path(
                "assets/main.png"
            )
        )
        
        #Configurações gerais da root
        self.root.title("Game Save Backup")
        self.root.geometry("512x592")
        self.root.iconphoto(True, self.icone)
        self.root.config(bg=self._primaryColor)
        self.root.option_add("*Foreground", self.fontColor)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.resizable(False, False)
        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.fecharJanela
        )
        
        
        #Botão de iniciar o monitoramento de jogos
        self.btnPrinc_frame = tk.Frame(self.root, relief="solid",width=256,height=96)
        self.btnPrinc_frame.grid(row=0, column=0 ,sticky="ew", padx=20, pady=8)
        self.btnPrinc_frame.config(bg=self._primaryColor)
        self.btnPrinc_frame.columnconfigure(0, weight=1)
        self.btnPrinc_frame.grid_propagate(False)
        self.btn_iniciar = tk.Button(
            self.btnPrinc_frame,
            text="Iniciar",
            command=self.iniciar,
            bg=self.btnColor,
            cursor="hand2",
            width=30
        )
        self.btn_iniciar.grid(
            row=0,
            column=0,
            pady=3
        )
        #Botão de para o monitoramento de jogos
        self.btn_parar = tk.Button(
            self.btnPrinc_frame,
            text="Parar",
            command=self.parar,
            bg=self.btnColor,
            cursor="hand2",
            width=30
        )
        self.btn_parar.grid(
            row=1,
            column=0,
            pady=3
        )
        #Botão que abre arquivo config.js
        self.btn_config = tk.Button(
            self.btnPrinc_frame,
            text="Config",
            command=self.abrirConfig,
            bg=self.btnColor,
            cursor="hand2",
            width=30
        )
        self.btn_config.grid(
            row=2,
            column=0,
            pady=3
        )
        
        #Frame que engloba as statísticas e botões de ação iniciar e parar monitoramento
        self.stats_frame = tk.Frame(self.root, width=256,height=96,relief="ridge", bd=2)
        self.stats_frame.grid(row=0, column=1,sticky="ew", padx=20, pady=8)
        self.stats_frame.config(bg=self._secundaryColor)
        self.stats_frame.columnconfigure(0, weight=1)
        self.stats_frame.rowconfigure(0,weight=1)
        self.stats_frame.rowconfigure(4,weight=1)
        self.stats_frame.grid_propagate(False)
        
        #Label de status
        self.label_status = tk.Label(
            self.stats_frame,
            text="Status: Parado",
            bg=self._secundaryColor
        )
        self.label_status.grid(
            row=1,
            column=0,
            sticky="we"
        )
        #Label que indica o estado de monitoramento
        self.label_monitor = tk.Label(
            self.stats_frame,
            text="Monitor: Desligado",
            bg=self._secundaryColor
        )
        self.label_monitor.grid(
            row=2,
            column=0,
            sticky="we"
        )
        #Label que indica uso de memória RAM
        self.label_ram = tk.Label(
            self.stats_frame,
            text="Uso RAM: -- MB",
            bg=self._secundaryColor
        )
        self.label_ram.grid(
            row=3,
            column=0,
            sticky="we"
        )
        
        #checklboxes settings
        self.checkBoxSettings_frame = tk.Frame(self.root, relief="solid")
        self.checkBoxSettings_frame.grid(row=1, column=0, sticky="ew", padx=20)
        self.checkBoxSettings_frame.config(bg=self._primaryColor)
        self.checkBoxSettings_frame.columnconfigure(0, weight=1)
        self.checkBoxSettings_frame.columnconfigure(1, weight=9)
        
        #Checkbox iniciar com windows
        self.starWin_valor_check = tk.BooleanVar()
        
        def verificar_estado_starWin():
            if self.starWin_valor_check.get():
                self.config.settings["iniciar_com_windows"] = True
                startup.criarAtalhoStartup()
            else:
                self.config.settings["iniciar_com_windows"] = False
                startup.removerAtalhoStartup()
            self.salvarConfigs()
        
        self.starWin_checkbox = tk.Checkbutton(
            self.checkBoxSettings_frame,
            variable=self.starWin_valor_check,
            command=verificar_estado_starWin,
            background=self._primaryColor, 
            foreground=self._primaryColor,
            cursor="hand2",
            activebackground=self._primaryColor
        )
        self.starWin_checkbox.grid(
            row=0,
            column=0,
            sticky="w"
        )
        self.labelCheckStartWin = tk.Label(
            self.checkBoxSettings_frame,
            text="Iniciar com windows",
            bg=self._primaryColor
        )
        self.labelCheckStartWin.grid(
            row=0,
            column=1,
            sticky="w"
        )
        
        #checkbox iniciar minimizado
        self.starMin_valor_check = tk.BooleanVar()
        
        def verificar_estado_starMin():
            if self.starMin_valor_check.get():
                self.config.settings["minimizar_para_tray"] = True
            else:
                self.config.settings["minimizar_para_tray"] = False
            self.salvarConfigs()
        
        self.starWin_checkbox = tk.Checkbutton(
            self.checkBoxSettings_frame,
            variable=self.starMin_valor_check,
            command=verificar_estado_starMin,
            background=self._primaryColor, 
            foreground=self._primaryColor,
            cursor="hand2",
            activebackground=self._primaryColor
        )
        self.starWin_checkbox.grid(
            row=1,
            column=0,
            sticky="w"
        )
        self.labelCheckStartWin = tk.Label(
            self.checkBoxSettings_frame,
            text="Iniciar minimizado",
            bg=self._primaryColor
        )
        self.labelCheckStartWin.grid(
            row=1,
            column=1,
            sticky="w"
        )
        
        #frame de último backup ou statísticas
        self.estatisticas_frame = tk.Frame(self.root, relief="solid")
        self.estatisticas_frame.grid(row=1, column=1, sticky="nsew", padx=20)
        self.estatisticas_frame.config(bg=self._secundaryColor)
        self.estatisticas_frame.columnconfigure(0, weight=1)
        
        #Frame dos inputs nome, origem e destino
        self.inputs_frame = tk.Frame(self.root, relief="ridge", bd=2)
        self.inputs_frame.grid(row=2, column=0,columnspan=2 ,sticky="ew", padx=20, pady=8, ipady=4)
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
            bg=self.btnColor,
            cursor="hand2"
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
            bg=self.btnColor,
            cursor="hand2"
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
            bg=self.btnColor,
            cursor="hand2"
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
            bg=self.btnColor,
            cursor="hand2"
        )
        self.btn_adicionar.grid(
            row=3,
            column=1,
            sticky="ew"
        )
        
        #Frame da lista de jogos cadastrados e botões de ação: Abrir save, Abrir backup, Fazer backup e Remover
        self.lista_jogos_frame = tk.Frame(self.root, relief="solid")
        self.lista_jogos_frame.grid(row=3, column=0,sticky="ew", padx=20, pady=4, columnspan=2)
        self.lista_jogos_frame.config(bg=self._primaryColor)
        self.lista_jogos_frame.columnconfigure(0, weight=1)
        self.lista_jogos_frame.columnconfigure(1, weight=0)
        
        self.label_listaJogos = tk.Label(
            self.lista_jogos_frame,
            text="Lista de jogos cadastrados",
            bg=self._primaryColor
        )
        self.label_listaJogos.grid(
            row=0,
            column=0,
            pady=4,
            sticky="w"
        )
        
        #Scrollbar da lista
        self.lista_jogos_scrollbar = ttk.Scrollbar(
            self.lista_jogos_frame, 
            orient="vertical", 
            style="Custom.Vertical.TScrollbar",
            cursor="hand2"
        )
        self.lista_jogos_scrollbar.grid(row=1, column=1, sticky="ns")
              
        #Lista de jogos em jogos.json
        self.lista = tk.Listbox(
            self.lista_jogos_frame,
            height=5,
            yscrollcommand=self.lista_jogos_scrollbar.set,
            # selectbackground=self._primaryColor,   # Cor de fundo quando selecionado
            selectforeground=self._primaryColor,
            cursor="hand2"
        )
        self.lista.grid(
            row=1,
            column=0,
            sticky="ew"
        )
        self.lista.config(bg=self._primaryColor)
        
        self.lista_jogos_scrollbar.config(command=self.lista.yview)
        
        self.btn_lista_jogos_frame = tk.Frame(self.root, relief="solid")
        self.btn_lista_jogos_frame.grid(row=4, column=0,sticky="ew", padx=20, pady=4, columnspan=2)
        self.btn_lista_jogos_frame.config(bg=self._primaryColor)
        self.btn_lista_jogos_frame.columnconfigure(0, weight=1)
        self.btn_lista_jogos_frame.columnconfigure(1, weight=1)
        
        #Botão que abri pasta do savegame de jogo selecionado na lista
        self.btn_abrir_origem = tk.Button(
            self.btn_lista_jogos_frame,
            text="Abrir save",
            command=self.abrirOrigem,
            pady=2,
            padx=6,
            compound="left",
            anchor="center",
            bg=self.btnColor,
            cursor="hand2"
        )
        self.btn_abrir_origem.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=5,
            padx=2
        )
        
        #Botão de forçar backup de jogo selecionado na lista
        self.btn_backup_now = tk.Button(
            self.btn_lista_jogos_frame,
            text="Fazer backup",
            command=self.fazerBackup,
            pady=2,
            padx=6,
            compound="left",
            anchor="center",
            bg=self.btnColor,
            cursor="hand2"
        )
        self.btn_backup_now.grid(
            row=0,
            column=1,
            sticky="ew",
            pady=5,
            padx=2
        )
        
        #Botão que abri pasta do backup do jogo selecionado na lista
        self.btn_abrir_destino = tk.Button(
            self.btn_lista_jogos_frame,
            text="Abrir backup",
            command=self.abrirDestino,
            pady=2,
            padx=6,
            compound="left",
            anchor="center",
            bg=self.btnColor,
            cursor="hand2"
        )
        self.btn_abrir_destino.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=5,
            padx=2
        )
        
        #Botão de remover jogo selecionado do jogos.json
        self.btn_remover = tk.Button(
            self.btn_lista_jogos_frame,
            text="Remover",
            command=self.remover,
            pady=2,
            padx=6,
            compound="left",
            anchor="center",
            bg=self.btnColor,
            cursor="hand2"
        )
        self.btn_remover.grid(
            row=1,
            column=1,
            sticky="ew",
            pady=5,
            padx=2
        )      
        
        #Botão de restaurar backup mais recente
        self.btn_restaurar = tk.Button(
            self.btn_lista_jogos_frame,
            text="Restaurar último backup",
            command=self.restaurar,
            pady=2,
            padx=6,
            compound="left",
            anchor="center",
            bg=self.btnColor,
            cursor="hand2"
        )
        self.btn_restaurar.grid(
            row=2,
            column=0,
            sticky="ew",
            columnspan=2,
            pady=5,
            padx=2
        )
        
        if self.iniciarMinimizado:
            self.root.after(
                100,
                self.fecharJanela
            )
            
        self.atualizarLista()
    
    def atualizaInterfaceMonitor(self):
        self.label_monitor.config(text=f"Monitor: {'Ligado' if self.monitorando else 'Desligado'}")
        self.starWin_valor_check.set(self.config.settings["iniciar_com_windows"])
        self.starMin_valor_check.set(self.config.settings["minimizar_para_tray"])
        
        if self.monitorando:
            self.btn_iniciar.config(
                state="disabled",
                cursor="arrow"
            )
            self.btn_parar.config(
                state="normal",
                cursor="hand2"
            )
        else:
            self.btn_parar.config(
                state="disabled",
                cursor="arrow"
            )
            self.btn_iniciar.config(
                state="normal",
                cursor="hand2"
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
        self.config.settings["iniciar_monitoramento"] = True
        self.salvarConfigs()
        self.atualizaInterfaceMonitor()        
        self.loopMonitor()
        
    #Função do botão parar monitoramento
    def parar(self):
        if not self.monitorando:
            return
        
        self.monitorando = False
        nt.notification("Monitor encerrado","Backup automático parado").show()
        self.label_status.config(text="Status: Parado")
        self.atualizaInterfaceMonitor()
        self.config.settings["iniciar_monitoramento"] = False
        self.salvarConfigs()
    
    def abrirConfig(self):
        os.startfile(self.config.settingPath)
    
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
    
    def restaurar(self):
        jogo = self.verificaJogoLista()
        response = messagebox.askyesno("Restaurar backup", f"Deseja restaurar o backup do último save de {jogo.nome_exibicao}?")
        
        if response:
            bk.restaurarBackup(jogo)
    
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

        self.root.after(self.config.intervalo_monitor_ms, self.loopMonitor)

    def executar(self):        
        self.atualizaInterfaceMonitor()
        
        if self.monitorando:
            self.loopMonitor()
        
        self.root.mainloop()
        
        
    #Funções para configurar bandeja
    def fecharJanela(self):
        self.esconderJanela()
        if self.tray.icon is None or not self.tray.icon.visible:
            self.tray.iniciar()

    def mostrarJanela(self):
        self.root.deiconify()

    def esconderJanela(self):
        self.root.withdraw()
    
    #funções de configurações do programa
    
    def salvarConfigs(self):
        self.config.salvarConfig(self.config.settings)