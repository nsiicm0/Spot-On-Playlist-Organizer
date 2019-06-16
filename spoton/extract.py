import logging
from .utils import Spoton_Util
import spotipy
import pandas as pd
import itertools
from datetime import datetime

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
        self.config = Spoton_Util.load_config()
        self.token = Spoton_Util.auth_spotify()
        self.logger.debug('Starting extraction')

    def _get_track(self, results):
        """ 
        Helper function to get track ids from api results

        Args:
            none
        
        Returns:
            Yields list of trackids
        """
        for item in results['items']:
            track = item['track']
            yield(track['id'])

    def extract(self):
        """ 
        Track metadata from spotify api.
        Results will be pickled and stored to disk.
        
        Args:
            none
        
        Returns:
            none
        """
        sp = spotipy.Spotify(auth=self.token)
        sp.trace = False
        
        # Query playlistid
        results = sp.current_user_playlists()
        playlistid = [x['id'] for x in results['items'] if x['name'] == self.config['spotify']['playlist']][0]
        self.logger.debug('Found playlist with the id {}'.format(playlistid))

        # Query tracks from playlist
        results = sp.user_playlist(self.config['spotify']['username'], playlistid, fields="tracks,next")
        tracks = results['tracks']
        track_ids = list(self._get_track(tracks))
        while tracks['next']:
            tracks = sp.next(tracks)
            track_ids.extend(list(self._get_track(tracks)))
        self.logger.debug('Retrieved {} tracks'.format(str(len(track_ids))))
        
        # Get track details
        start = 0
        end = 50
        trackinfo = []
        trackfeatures = []
        # we have to loop in chunks of 50 due to api limitation
        for i in range(0, len(track_ids), 50):
            _info = sp.tracks(track_ids[i:i+50])
            _features = sp.audio_features(track_ids[i:i+50])
            trackinfo.extend(_info['tracks'])
            trackfeatures.extend(_features)
        self.logger.debug('Fetched all track metadata.')
        pd_trackinfo = pd.DataFrame(trackinfo)
        pd_trackinfo.to_pickle('{}/trackinfo_{}.pkl'.format(self.config['app']['data']['path'],datetime.now().strftime('%Y%m%d%H%M'))) 
        pd_trackfeatures = pd.DataFrame(trackfeatures)
        pd_trackfeatures.to_pickle('{}/trackfeatures_{}.pkl'.format(self.config['app']['data']['path'],datetime.now().strftime('%Y%m%d%H%M')))
        self.logger.debug('Pickled all track metadata.') 
        self.logger.debug('Done extracting.') 