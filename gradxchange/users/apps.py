from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    
    def ready(self):
        import users.signals

# This class is a configuration class for the 'users' app in Django. It sets up the app and includes important initialization steps like importing signal handlers when Django starts up. The signal handlers defined in users.signals are prepared to be connected when the app is ready, ensuring they're only imported after Django has finished setting up.