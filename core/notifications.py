from winotify import Notification

#Função geral de notificação do windows
def notification(titulo : str,mensagem : str):
    return Notification(
        app_id="Game Save Backup",
        title=titulo,
        msg=mensagem
    )