from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'
    def ready(self):
        import checkout.signals
        from .signals import create_ott
        from .signals import create_ott_signal
        create_ott_signal.connect(create_ott)
