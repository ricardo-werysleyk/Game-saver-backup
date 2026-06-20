import tkinter as tk
from models.monitor import Monitor
from models.jogo import Jogo
import core.notifications as nt
from tkinter import filedialog
from tkinter import messagebox
import os


class App:

    def __init__(self, monitor):

        self.monitor = monitor

        self.root = tk.Tk()
        self.root.title("Game Save Backup")
        self.root.geometry("480x528")
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        
        self.inputs_frame = tk.Frame(self.root, relief="solid")
        self.inputs_frame.grid(row=4, column=0,columnspan=2 ,sticky="ew", padx=20, pady=20)
        self.inputs_frame.columnconfigure(0, weight=1)
        self.inputs_frame.columnconfigure(1, weight=8)
        self.inputs_frame.columnconfigure(2, weight=1)
        
        self.lista_jogos_frame = tk.Frame(self.root, relief="solid")
        self.lista_jogos_frame.grid(row=5, column=0,columnspan=2 ,sticky="ew", padx=20, pady=20)
        self.lista_jogos_frame.columnconfigure(0, weight=1)
        self.lista_jogos_frame.columnconfigure(1, weight=1)
        self.lista_jogos_frame.columnconfigure(2, weight=0)
        self.lista_jogos_scrollbar = tk.Scrollbar(self.lista_jogos_frame, orient="vertical")
        self.lista_jogos_scrollbar.grid(row=0, column=2, sticky="ns")

        self.monitorando = False
        
        self.entry_nome = tk.Entry(self.inputs_frame)
        self.entry_nome.insert(0, "[ Ex: Valheim.exe ]")

        self.entry_origem = tk.Entry(self.inputs_frame)
        self.entry_origem.insert(0, "[ Selecione pasta save ]")

        self.entry_destino = tk.Entry(self.inputs_frame)
        self.entry_destino.insert(0, "[ Selecione pasta backup ]")

        self.label_status = tk.Label(
            self.root,
            text="Status: Parado"
        )

        self.label_monitor = tk.Label(
            self.root,
            text="Monitor: Desligado"
        )

        self.label_ram = tk.Label(
            self.root,
            text="Uso RAM: -- MB"
        )

        self.btn_iniciar = tk.Button(
            self.root,
            text="Iniciar",
            command=self.iniciar
        )

        self.btn_parar = tk.Button(
            self.root,
            text="Parar",
            command=self.parar
        )

        self.btn_config = tk.Button(
            self.root,
            text="Configurações",
            command=self.config
        )
        
        self.label_nome_jogo_inputs_frame = tk.Label(
            self.inputs_frame,
            text="Nome:"
        )
        self.label_nome_jogo_inputs_frame.grid(
            row=0,
            column=0,
            pady=10
        )
                
        self.btn_exe = tk.Button(
            self.inputs_frame,
            text="📂",
            command=self.selecionarExecutavel
        )
        
        self.label_origem_jogo_inputs_frame = tk.Label(
            self.inputs_frame,
            text="Origem:"
        )
        self.label_origem_jogo_inputs_frame.grid(
            row=1,
            column=0,
            pady=10
        )

        self.btn_origem = tk.Button(
            self.inputs_frame,
            text="📂",
            command=lambda:
                self.selecionarDiretorio(
                    self.entry_origem
                )
        )
        
        self.label_destino_jogo_inputs_frame = tk.Label(
            self.inputs_frame,
            text="Destino:"
        )
        self.label_destino_jogo_inputs_frame.grid(
            row=2,
            column=0,
            pady=10
        )

        self.btn_destino = tk.Button(
            self.inputs_frame,
            text="📂",
            command=lambda:
                self.selecionarDiretorio(
                    self.entry_destino
                )
        )

        self.btn_adicionar = tk.Button(
            self.inputs_frame,
            text="Adicionar jogo",
            command=self.adicionar
        )

        self.lista = tk.Listbox(
            self.lista_jogos_frame,
            height=5,
            yscrollcommand=self.lista_jogos_scrollbar.set
        )
        self.lista_jogos_scrollbar.config(command=self.lista.yview)
        
        self.btn_remover = tk.Button(
            self.lista_jogos_frame,
            text="🗑 Remover",
            command=self.remover,
            pady=2,
            padx=6,
            compound="left",
            anchor="center"
        )
        
        self.btn_backup_now = tk.Button(
            self.lista_jogos_frame,
            text="💾 Fazer backup",
            command=self.fazerBackup,
            pady=2,
            padx=6,
            compound="left",
            anchor="center"
        )
        
        self.btn_abrir_origem = tk.Button(
            self.lista_jogos_frame,
            text="📂 Abrir save",
            command=self.abrirOrigem,
            pady=2,
            padx=6,
            compound="left",
            anchor="center"
        )
        self.btn_abrir_destino = tk.Button(
            self.lista_jogos_frame,
            text="📂 Abrir backup",
            command=self.abrirDestino,
            pady=2,
            padx=6,
            compound="left",
            anchor="center"
        )

        self.label_status.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=10
        )

        self.label_monitor.grid(
            row=1,
            column=0,
            columnspan=2
        )

        self.label_ram.grid(
            row=2,
            column=0,
            columnspan=2
        )

        self.btn_iniciar.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=10,
            pady=20
        )

        self.btn_parar.grid(
            row=3,
            column=1,
            sticky="ew",
            padx=10
        )

        self.entry_nome.grid(
            row=0,
            column=1,
            sticky="ew"
        )

        self.btn_exe.grid(
            row=0,
            column=2,
            sticky="w",
            padx=5
        )

        self.entry_origem.grid(
            row=1,
            column=1,
            sticky="ew"
        )

        self.btn_origem.grid(
            row=1,
            column=2,
            sticky="w",
            padx=5
        )

        self.entry_destino.grid(
            row=2,
            column=1,
            sticky="ew"
        )

        self.btn_destino.grid(
            row=2,
            column=2,
            sticky="w",
            padx=5
        )

        self.btn_adicionar.grid(
            row=3,
            column=1,
            sticky="ew"
        )

        self.lista.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=5
        )
        
        self.btn_abrir_origem.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=5,
            padx=2
        )
        
        self.btn_abrir_destino.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=5,
            padx=2
        )
        
        self.btn_backup_now.grid(
            row=2,
            column=1,
            sticky="ew",
            pady=5,
            padx=2
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

    def iniciar(self):        
        if self.monitorando:
            return
        
        nt.notification("Monitor iniciado","Monitorando jogos").show()
        self.monitorando = True
        self.atualizaLabelMonitor()
        self.loopMonitor()
        

    def parar(self):
        self.monitorando = False
        nt.notification("Monitor encerrado","Backup automático parado").show()
        self.label_status.config(text="Status: Parado")
        self.atualizaLabelMonitor()
    
    def config(self):
        self.monitor.salvarJogoNovo(Jogo("Valheim", "C:\\Valheim", "D:\\backups"))
        
    def atualizarInterface(self, estado):
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

            nome = os.path.basename(
                caminho
            )

            self.entry_nome.delete(
                0,
                tk.END
            )

            self.entry_nome.insert(
                0,
                nome
            )
            
    def selecionarDiretorio(self,campo):

        pasta = filedialog.askdirectory()

        if pasta:

            campo.delete(
                0,
                tk.END
            )

            campo.insert(
                0,
                pasta
            )
    
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
                self.entry_nome.insert(0, "[ Ex: Valheim.exe ]")
                self.entry_origem.insert(0, "[ Selecione pasta save ]")
                self.entry_destino.insert(0, "[ Selecione pasta backup ]")
                # self.entry_nome.delete(0, tk.END)
                # self.entry_origem.delete(0, tk.END)
                # self.entry_destino.delete(0, tk.END)
                 
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
    
    def atualizarLista(self):

        self.lista.delete(
            0,
            tk.END
        )

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

        self.atualizarInterface(
            estado
        )

        self.root.after(
            100,
            self.loopMonitor
        )

    def executar(self):
        self.atualizaLabelMonitor()
        self.root.mainloop()