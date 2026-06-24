from winotify import Notification
import core.arquive_handling as arquive

#Função geral de notificação do windows
def notification(titulo : str,mensagem : str):
    return Notification(
        app_id="Game Save Backup",
        title=titulo,
        msg=mensagem,
        icon=arquive.resource_path("assets/main.png")
    )