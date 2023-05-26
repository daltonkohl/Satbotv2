# Import the AppConfig class from the django.apps module
from django.apps import AppConfig

# Define a configuration class for the satbotTA app
class SatbottaConfig(AppConfig):
    # Define the default type of auto-generated fields in the models
    # Here it is set to BigAutoField, which is a 64-bit integer,
    # useful for models expecting very large number of instances.
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Specify the name of the application for which this configuration applies
    # Here the app is called 'satbotTA'
    name = 'satbotTA'