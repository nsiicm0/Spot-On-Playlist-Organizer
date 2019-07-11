import logging
import itertools
import numpy as np
import pandas as pd
from .utils import Spoton_Util
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA  
from sklearn.preprocessing import StandardScaler

module_logger  = logging.getLogger('spoton.transform')

class Spoton_Transform():
    """
    Spoton_Transform() class. 

    This class is used to transform the data previously extracted from the spotify developer api.

    Usage: Use in code
        Spoton_Transform().transform()

    """

    def __init__(self, timestamp):
        self.logger = logging.getLogger('spoton.transform.Transformer')
        self.config = Spoton_Util.load_config()
        self.logger.debug('Starting transformation')
        self.timestamp = timestamp
        self.df = None

    def transform(self):
        """ 
        Main entrypoint to start transformation.
        
        Args:
            none
        
        Returns:
            none
        """
        self._prepare()
        self._cluster()
        self._store()
        self.logger.debug('Transformation is done...')

    def _prepare(self):
        self.logger.debug('Starting to prepare the data...')
        # Loading the data
        pd_trackinfo = pd.read_pickle('{}/trackinfo_{}.pkl'.format(self.config['app']['data']['path'],self.timestamp)) 
        pd_trackfeatures = pd.read_pickle('{}/trackfeatures_{}.pkl'.format(self.config['app']['data']['path'],self.timestamp))

        # Cleaning
        columns_to_drop = ['album', 'artists', 'available_markets', 'disc_number', 
                   'duration_ms', 'external_ids', 'external_urls', 'href',
                   'is_local', 'name', 'preview_url', 'track_number', 'type',
                   'uri']
        pd_trackinfo.drop(columns_to_drop, axis=1, inplace=True) 
        pd_trackinfo.drop_duplicates(inplace=True)

        columns_to_drop = ['analysis_url', 'track_href', 'type', 'uri']
        pd_trackfeatures.drop(columns_to_drop, axis=1, inplace=True) 
        pd_trackfeatures.drop_duplicates(inplace=True)

        df = pd.merge(pd_trackinfo, pd_trackfeatures, on='id', suffixes=('_trackinfo','_trackfeatures'), how='inner')

        # Normalization
        if self.config['app']['transformation']['use_standard_scaler']:
            cluster_features = ['explicit', 'popularity', 'acousticness', 'danceability',
                'duration_ms', 'energy', 'instrumentalness', 'key', 'liveness', 
                'loudness', 'speechiness', 'tempo', 'valence']
            df_cluster = df[cluster_features]
            ids = df[['id']]
            X = np.array(df_cluster)
            scaler = StandardScaler()
            scaler.fit(X)
            X = scaler.transform(X)
            df_clean = pd.DataFrame(X, columns=cluster_features)
            self.df = pd.concat([df_clean, ids], axis=1)
        else:
            df['explicit_clean'] = df['explicit'].astype(float)

            df['popularity_'] = df['popularity'].map(lambda x: x/100)
            df['popularity_clean'] = (df['popularity_']-df['popularity_'].min())/(df['popularity_'].max()-df['popularity_'].min())
            df.drop(['popularity_'], axis=1, inplace=True)

            df['acousticness_'] = df['acousticness'].map(lambda x: np.log(x))
            df['acousticness_clean'] = (df['acousticness_']-df['acousticness_'].min())/(df['acousticness_'].max()-df['acousticness_'].min())
            df.drop(['acousticness_'], axis=1, inplace=True)

            df['danceability_clean'] = (df['danceability']-df['danceability'].min())/(df['danceability'].max()-df['danceability'].min())

            df['duration_ms_clean'] = (df['duration_ms']-df['duration_ms'].min())/(df['duration_ms'].max()-df['duration_ms'].min())

            df['energy_clean'] = (df['energy']-df['energy'].min())/(df['energy'].max()-df['energy'].min())

            df['instrumentalness_'] = df['instrumentalness'].map(lambda x: 0.5 if x > 0.5 else x)
            df['instrumentalness_clean'] = (df['instrumentalness_']-df['instrumentalness_'].min())/(df['instrumentalness_'].max()-df['instrumentalness_'].min())
            df.drop(['instrumentalness_'], axis=1, inplace=True)

            df['key_clean'] = (df['key']-df['key'].min())/(df['key'].max()-df['key'].min())

            df['liveness_clean'] = (df['liveness']-df['liveness'].min())/(df['liveness'].max()-df['liveness'].min())

            df['loudness_clean'] = (df['loudness']-df['loudness'].min())/(df['loudness'].max()-df['loudness'].min())

            df.drop(['mode'], axis=1, inplace=True)

            df['speechiness_'] = df['speechiness'].map(lambda x: np.log(x))
            df['speechiness_clean'] = (df['speechiness_']-df['speechiness_'].min())/(df['speechiness_'].max()-df['speechiness_'].min())
            df.drop(['speechiness_'], axis=1, inplace=True)

            df['tempo_clean'] = (df['tempo']-df['tempo'].min())/(df['tempo'].max()-df['tempo'].min())

            df.drop(['time_signature'], axis=1, inplace=True)

            df['valence_clean'] = (df['valence']-df['valence'].min())/(df['valence'].max()-df['valence'].min())

            columns_for_processing = [x for x in list(df.columns) if 'clean' in x]
            columns_for_processing.append('id')
            df_clean = df[columns_for_processing].copy()
            df_clean.rename(columns=lambda x: x.replace('_clean', ''), inplace=True)
            self.df = df_clean

    def _cluster(self):
        self.logger.debug('Starting to cluster the data...')
        pca = PCA()
        X = pca.fit_transform(self.df.loc[:, ~self.df.columns.isin(['id'])])
        kmeans = KMeans(n_clusters=2,init='k-means++', random_state=1337).fit(X)
        prediction = pd.DataFrame(np.array(kmeans.predict(X)), columns=['label'])
        self.df = pd.concat([self.df, prediction], axis=1)

    def _store(self):
        self.logger.debug('Starting to store the data...')
        cluster_exportable = ((
            self.df[['id','label']]
        ).assign(label=lambda _df: _df['label'].replace(np.nan, 1337))
        ).assign(label=lambda _df: _df['label'].map({0:'Archive Playlist 1', 1: 'Archive Playlist 2', 1337: 'Archive Playlist 1337'}))
        cluster_exportable.to_pickle('{}/clusters_{}.pkl'.format(self.config['app']['data']['path'],self.timestamp)) 
