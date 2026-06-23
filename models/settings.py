from dataclasses import dataclass
import core.arquive_handling as arquive

@dataclass(slots=True)
class Settings:
    settings = arquive.carregarSettingsJson()
    iniciar_com_windows: bool = settings["iniciar_com_windows"]
    iniciar_monitoramento: bool = settings["iniciar_monitoramento"]
    minimizar_para_tray: bool = settings["minimizar_para_tray"]
    intervalo_monitor_ms: int = settings["intervalo_monitor_ms"]
    total_backups: int = settings["total_backups"]
    settingPath = arquive.SETTINGS_PATH
    
    def salvarConfig(self, config):
        arquive.salvarSettingsJson(config)
    
    