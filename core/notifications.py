from winotify import Notification

#Função geral de notificação do windows
def notification(titulo : str,mensagem : str):
    return Notification(
        app_id="Game Save Backup",
        title=titulo,
        msg=mensagem,
        icon=r"c:\Users\werys\Documents\Projetos Python\Game-saver-backup\assets\main.png"
    )