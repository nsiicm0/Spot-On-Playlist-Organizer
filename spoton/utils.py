import os
import yaml
import logging

module_logger  = logging.getLogger('spoton.util')

class Spoton_Util():
    """
    The static util class for the spoton app.
    Usage: Use in code
        Spoton_Util().load_config()

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
        logger = logging.getLogger('spoton.util.Config')
        configfile = 'config.yml'
        logger.debug('Reading config from {}'.format(configfile))
        with open(configfile) as config:
            return yaml.safe_load(config)