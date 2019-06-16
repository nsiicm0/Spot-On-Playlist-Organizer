import logging

module_logger  = logging.getLogger('spoton.extract')

class Spoton_Extract():
    """
    Spoton_Extract() class. 

    This class is used to extract data from the spotify developer api.

    Usage: Use in code
        Spoton_Extract().extract()

    """

    def __init__(self):
        self.logger = logging.getLogger('spoton.extract.Extractor')
        self.logger.debug('Starting extraction')
        self.logger.debug('Done with extraction')
