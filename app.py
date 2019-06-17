import os
import sys
import logging
import argparse
from datetime import datetime

from spoton.utils import Spoton_Util
from spoton.extract import Spoton_Extract

class Spoton_Controller:

    def __init__(self, arguments):
        self.config = Spoton_Util.load_config()
        self.logger = logging.getLogger('spoton.Controller')
        self.arguments = arguments

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
        if not self.arguments.no_extraction:
            Spoton_Extract().extract()
        
        self.logger.info('Finished application')

def _setup_logging():
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
        return root

if __name__ == '__main__':
    parser = argparse.ArgumentParser( description="Optimize your Spotify playlists",
        epilog="Example usage: python app.py --full",
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('--full', action='store_true',
                        default=False,
                        dest='full',
                        help='Runs the full pipeline (recommended when running for the first time).')

    parser.add_argument('--no-extraction', action='store_true',
                        default=False,
                        dest='no_extraction',
                        help='Skips extraction of data from the spotify api.')

    results = parser.parse_args()

    _setup_logging()
    logger = logging.getLogger('spoton.Bootstrap')
    
    if len(sys.argv) > 1:
        if results.full and results.no_extraction:
            logger.info("Arguments invalid. Run app.py --help for help!")
        else:
            Spoton_Controller(results).run()
    else:
        logger.info("No arguments provided! Run app.py --help for help!")