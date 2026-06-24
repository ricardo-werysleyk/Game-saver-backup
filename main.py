import os
import sys
#models
from models.monitor import Monitor
#GUI
from gui.main_window import App

def set_working_dir():

    if getattr(
        sys,
        "frozen",
        False
    ):

        os.chdir(
            os.path.dirname(
                sys.executable
            )
        )


set_working_dir()

monitor = Monitor()
gui = App(monitor=monitor)
gui.executar()