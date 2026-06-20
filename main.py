#modules
import psutil
import os
import time
import msvcrt

#models
from models.monitor import Monitor
#core
import core.notifications as nt

#Variáveis globais
PROCESSO = psutil.Process(os.getpid())
INTERVALO = 1


nt.notification("Monitor iniciado","Monitorando jogos").show()

monitor = Monitor()

while True:

    estado = monitor.executar()
    
    print(estado["status"])
    print("Monitorando...")
    print("Pressione 'F' para encerrar programa.")
    
    memoria = (
        PROCESSO.memory_info().rss
        / 1024
        / 1024
    )

    print(
        f"Uso RAM: {memoria:.2f} MB"
    )
    
    # Verifica se alguma tecla foi apertada
    if msvcrt.kbhit():
        tecla = msvcrt.getch()
        if tecla.lower() == b'f':
            print("\nEncerrando monitoramento...")
            nt.notification("Monitor encerrado","Backup automático parado").show()
            break

    time.sleep(INTERVALO)
    print("\033c", end="")
