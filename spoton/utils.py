import os
import yaml

class Spoton_Util():
    """
    The static util class for the spoton app.
    Usage: Use in code
        Spoton_Util().load_config()

    optional arguments:
    -h, --help  show this help message and exit
    
    """

    @staticmethod
    def load_config():
        """ 
        Loads the config.yml file and exposes its content in an multi-dimensional array like structure.
        
        Args:
            none
        
        Returns:
            Multi-dimensional array
        """
        with open("config.yml") as config:
            return yaml.safe_load(config)