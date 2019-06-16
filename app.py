import os
import sys
import logging
from datetime import datetime

from spoton.utils import Spoton_Util

class Spoton_Controller:

    def __init__(self):
        self.config = Spoton_Util().load_config()
        self.logger = self._setup_logging()
    
    def _setup_logging(self):
        """
        Sets up loggging functionality for the controller.

        Args:
            none
        
        Returns:
            Configured logging object.
        """
        logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        root = logging.getLogger('spoton_controller')
        root.setLevel(os.environ.get("LOGLEVEL", self.config['app']['logging']['level']))
        if self.config['app']['logging']['file']:
            fileHandler = logging.FileHandler(
                '{0}/run_{1}.log'.format(self.config['app']['logging']['logpath'], datetime.now().strftime('%Y%m%d%H%M%S'))
            )
            fileHandler.setFormatter(logFormatter)
            fileHandler.setLevel(logging.DEBUG)
            root.addHandler(fileHandler)
        if self.config['app']['logging']['console']:
            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(consoleHandler)
            consoleHandler.setLevel(logging.INFO)
            root.addHandler(consoleHandler)
        return root

    def run(self):
        """
        Controller run function.

        All the magic happens here.

        Args:
            none

        Returns:
            none
        """
        self.logger.log(logging.DEBUG, 'It works!')

if __name__ == '__main__':
    Spoton_Controller().run()