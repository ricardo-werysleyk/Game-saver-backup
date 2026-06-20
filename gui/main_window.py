import tkinter as tk
from models.monitor import Monitor
from models.jogo import Jogo
import core.notifications as nt


class App:

    def __init__(self, monitor):

        self.monitor = Monitor()

        self.root = tk.Tk()

        self.root.title("Game Save Backup")

        self.root.geometry("500x250")

        self.monitorando = False

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
            text="RAM: -- MB"
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
        
        self.btn_remover = tk.Button(
            self.root,
            text="Remover jogo",
            command=self.remover
        )

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

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

        # self.btn_config.grid(
        #     row=4,
        #     column=0,
        #     columnspan=2,
        #     sticky="ew",
        #     padx=10
        # )
        
        # self.btn_remover.grid(
        #     row=4,
        #     column=1,
        #     columnspan=2,
        #     sticky="ew",
        #     padx=10
        # )

    def atualizaLabelMonitor(self):
        self.label_monitor.config(text=f"Monitor: {'Ligado' if self.monitorando else 'Desligado'}")

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
    
    def remover(self):
        self.monitor.removerJogo("ValheIM")
        
    def atualizarInterface(self, estado):
        self.label_status.config(
            text=estado["status"]
        )

        # jogo = estado["jogo"]

        # self.label_jogo.config(
        #     text=f"Jogo: {jogo.nome_exibicao}"
        # )

        # self.label_backup.config(
        #     text=(
        #         f"Backup: {jogo.destino}"
        #         if jogo.destino
        #         else "-"
        #     )
        # )
        
    def loopMonitor(self):
        if not self.monitorando:
            return

        estado = self.monitor.executar()

        self.atualizarInterface(
            estado
        )

        self.root.after(
            500,
            self.loopMonitor
        )

    def executar(self):
        self.root.mainloop()