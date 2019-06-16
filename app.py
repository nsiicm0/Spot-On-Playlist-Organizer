import os
import sys
import logging
from datetime import datetime

from spoton.utils import Spoton_Util
from spoton.extract import Spoton_Extract

class Spoton_Controller:

    def __init__(self):
        self.config = Spoton_Util().load_config()
        self.logger = logging.getLogger('spoton.Controller')

    def run(self):
        """
        Controller run function.

        All the magic happens here.

        Args:
            none

        Returns:
            none
        """
        self.logger.info('Started application')
        Spoton_Extract()
        self.logger.info('Finished application')

def _setup_logging():
        """
        Sets up loggging functionality for the app.

        Args:
            none
        
        Returns:
            none
        """
        conf = Spoton_Util().load_config()
        root = logging.getLogger('spoton')
        logFormatter = logging.Formatter("%(asctime)s [%(name)s] [%(levelname)-5.5s]  %(message)s")
        root.setLevel(os.environ.get("LOGLEVEL", conf['app']['logging']['level']))
        if conf['app']['logging']['console']:
            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(consoleHandler)
            consoleHandler.setLevel(logging.WARNING)
            root.addHandler(consoleHandler)
        if conf['app']['logging']['file']:
            fileHandler = logging.FileHandler('{}/{}.log'.format(conf['app']['logging']['logpath'], datetime.now().strftime('%Y%m%d%H%M%S')))
            fileHandler.setFormatter(logFormatter)
            fileHandler.setLevel(logging.DEBUG)
            root.addHandler(fileHandler)
        root.propagate = False

if __name__ == '__main__':
    _setup_logging()
    Spoton_Controller().run()