#models
from models.monitor import Monitor
#GUI
from gui.main_window import App

monitor = Monitor()
gui = App(monitor=monitor)
gui.executar()