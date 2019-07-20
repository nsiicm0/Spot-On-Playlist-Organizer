import os
import sys
import logging
import argparse
from datetime import datetime

from spoton.load import Spoton_Load
from spoton.utils import Spoton_Util
from spoton.extract import Spoton_Extract
from spoton.transform import Spoton_Transform

class Spoton_Controller:

    def __init__(self, arguments):
        self.config = Spoton_Util.load_config()
        self.logger = logging.getLogger('spoton.Controller')
        self.arguments = arguments

    def run(self, timestamp):
        """
        Controller run function.

        All the magic happens here.

        Args:
            none

        Returns:
            none
        """
        self.logger.info('Started application')
        if not self.arguments.no_extraction:
            Spoton_Extract(timestamp).extract()

        if not self.arguments.no_transformation:
            Spoton_Transform(timestamp).transform()

        if not self.arguments.no_loading:
            Spoton_Load(timestamp).load()
        
        self.logger.info('Finished application')

def _setup_logging(timestamp):
        """
        Sets up loggging functionality for the app.

        Args:
            none
        
        Returns:
            none
        """
        conf = Spoton_Util.load_config()
        root = logging.getLogger('spoton')
        logFormatter = logging.Formatter("%(asctime)s [%(name)s] [%(levelname)-5.5s]  %(message)s")
        root.setLevel(os.environ.get("LOGLEVEL", conf['app']['logging']['level']))
        if conf['app']['logging']['file']:
            fileHandler = logging.FileHandler('{}/{}.log'.format(conf['app']['logging']['logpath'], timestamp))
            fileHandler.setFormatter(logFormatter)
            fileHandler.setLevel(logging.DEBUG)
            root.addHandler(fileHandler)
        root.propagate = False
        return root

if __name__ == '__main__':
    parser = argparse.ArgumentParser( description="Optimize your Spotify playlists",
        epilog="Example usage (recommended if run for the first time): python app.py",
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('--no-extraction', action='store_true',
                        default=False,
                        dest='no_extraction',
                        help='Skips extraction of data from the spotify api.')

    parser.add_argument('--no-transformation', action='store_true',
                        default=False,
                        dest='no_transformation',
                        help='Skips transformation of extracted data from the spotify api.')

    parser.add_argument('--no-loading', action='store_true',
                        default=False,
                        dest='no_loading',
                        help='Skips loading of extracted and transformed data from the spotify api.')

    results = parser.parse_args()
    global_timestamp = datetime.now().strftime('%Y%m%d%H%M')
    _setup_logging(global_timestamp)
    logger = logging.getLogger('spoton.Bootstrap')
    
    logger.debug("Run parameters: {}".format(results))
    logger.debug("Global timestamp: {}".format(global_timestamp))
    Spoton_Controller(results).run(global_timestamp)