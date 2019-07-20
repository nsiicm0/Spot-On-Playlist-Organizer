import logging
import spotipy
import numpy as np
import pandas as pd
from .utils import Spoton_Util
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA  
from sklearn.preprocessing import StandardScaler

module_logger  = logging.getLogger('spoton.load')

class Spoton_Load():
    """
    Spoton_Load() class. 

    This class is used to load the data into Spotify.

    Usage: Use in code
        Spoton_Load().load()

    """

    def __init__(self, timestamp):
        self.logger = logging.getLogger('spoton.load.Loader')
        self.config = Spoton_Util.load_config()
        self.token = Spoton_Util.auth_spotify()
        self.logger.debug('Start loading')
        self.timestamp = timestamp
        self.df = None
        self.spotify_playlist_info = {}

    def load(self):
        """ 
        Main entrypoint to start loading.
        In this process we will store the cluster results in Spotify.
        
        Args:
            none
        
        Returns:
            none
        """
        self.df = pd.read_pickle('{}/clusters_{}.pkl'.format(self.config['app']['data']['path'],self.timestamp)) 

        self._create_playlist()
        self._update_playlists()
        self.logger.debug('Loading is done...')

    def _create_playlist(self):
        """ 
        Creates the playlists in Spotify for later use.
        These playlists are being used to hold the cluster results.
        
        Args:
            none
        
        Returns:
            none
        """
        self.logger.debug('Starting to create new playlists...')
        sp = spotipy.Spotify(auth=self.token)
        sp.trace = False
        for playlist in list(self.df['label'].unique()):
            playlist_name = '{} {}'.format(playlist, self.timestamp)
            self.spotify_playlist_info[playlist_name] = sp.user_playlist_create(user=self.config['spotify']['username'], name=playlist_name, public=False)

    def _update_playlists(self):
        """ 
        Updating of previously created playlists.
        In this step we actually save the results onto Spotify.
        
        Args:
            none
        
        Returns:
            none
        """
        self.logger.debug('Starting to update the newly created playlists...')
        sp = spotipy.Spotify(auth=self.token)
        sp.trace = False
        for playlist in self.spotify_playlist_info.keys():
            track_ids = list(self.df.loc[self.df['label']==playlist.replace(' {}'.format(self.timestamp),'')]['id'])
            for i in range(0, len(track_ids), 50):
                results = sp.user_playlist_add_tracks(user=self.config['spotify']['username'], playlist_id=self.spotify_playlist_info[playlist]['id'], tracks=track_ids[i:i+50])
                self.logger.debug('Loaded chunk of 50 tracks into playlist {} with result: {}'.format(playlist, results))
