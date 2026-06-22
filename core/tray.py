import pystray
import threading
from PIL import Image

class Tray:

    def __init__(self, app):
        self.app = app
        self.icon = None

    def iniciar(self):
        imagem = Image.open("assets/main.png")

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

        # self.icon.run()
        threading.Thread(
            target=self.icon.run,
            daemon=True
        ).start()

    def abrir(self):
        self.app.mostrarJanela()
        self.icon.stop()
        
    def iniciarMonitor(self):
        self.app.iniciar()
    
    def pararMonitor(self):
        self.app.parar()

    def sair(self):
        self.icon.stop()
        self.app.root.after(
            0,
            self.app.root.destroy
        )