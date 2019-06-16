import os
import yaml
import logging
import spotify_token as st
import spotipy
import spotipy.util as util
import time

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
    
    @staticmethod
    def auth_spotify():
        """ 
        Get oauth token for spotify api.

        If a previously fetched token is still valid, it will retrieve it from cache.
        
        Args:
            none
        
        Returns:
            Token to be used for future requests against the api.
        """
        logger = logging.getLogger('spoton.util.Auth')
        conf = Spoton_Util().load_config()
        logger.debug('Authenticating with Spotify')
        if os.path.isfile('.auth'):
            with open('.auth', 'r') as f:
                exp = f.readline()
                tkn = f.readline()
                if float(exp) > time.time():
                    logger.debug('Got token {} from cache'.format(tkn))
                    return tkn
        data = st.start_session(conf['auth']['username'],conf['auth']['password'])
        access_token = data[0]
        expiration_date = data[1]
        with open('.auth', 'w') as f:
            f.write(str(expiration_date)+'\n')
            f.write(str(access_token))
        logger.debug('Got token {} which expires on {}'.format(access_token, expiration_date))
        return access_token

        