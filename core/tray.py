import pystray
import os
from PIL import Image
import core.arquive_handling as arquive

class Tray:

    def __init__(self, app):
        self.app = app
        self.icon = None

    def iniciar(self):
        imagem = Image.open(
                arquive.resource_path(
                "assets/main.png"
            )
        )

        self.icon = pystray.Icon(
            "GameSaveBackup",
            imagem,
            menu=pystray.Menu(
                pystray.MenuItem("Abrir", self.abrir),
                pystray.MenuItem("Iniciar monitor", self.iniciarMonitor),
                pystray.MenuItem("Parar monitor", self.pararMonitor),
                pystray.MenuItem("Sair", self.sair)
            )
        )

        self.icon.run_detached()

    def abrir(self):
        self.app.mostrarJanela()
        self.icon.visible = False
        
    def iniciarMonitor(self):
        self.app.iniciar()
    
    def pararMonitor(self):
        self.app.parar()

    def sair(self):
        self.icon.stop()
        # self.app.monitorando = False
        # self.app.root.quit()
        # self.app.root.destroy()
        self.app.root.after(0, self.app.root.destroy)
        os._exit(0)