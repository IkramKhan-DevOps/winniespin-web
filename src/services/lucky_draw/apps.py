from django.apps import AppConfig


class LuckyDrawConfig(AppConfig):
    name = 'src.services.lucky_draw'
    default_auto_config = 'django.db.models.BigAutoField'

    def ready(self):
        import src.services.lucky_draw.signals
