# Spot-On-Playlist-Organizer

## About

Everybody who uses Spotify has come across playlists. Playlists are the way to store various tracks in a single list. Lists usually tend to get cluttered over time. So do also Spotify playlists. Ever been on a morning commute, rocking your favorite songs and then suddenly the next song queuing up just blew your tune because it just does not quite fit? Spot-On-Playlist-Organizer solves this problem by decluttering playlists and reorganizing a given playlist into multiple smaller ones. It takes various features of your tracks into account to group them.

## How does it work?

The application is quite simple. It follows the following steps which are common for an ETL (Extract-Transform-Load) process:

1. Upon running this application, we will extract the track data (for a playlist you previously specified) directly from Spotify.
2. The track data will be transformed and passed onto a clustering algorithm.
3. The tracks will then be stored into new playlists defined by the previously retrieved clusters.

Note: No real validation for correctness of the clusters can be made. This has various reasons:

* No ground truth can be provided to the system. (We don't think you would actually have ground truth on how the playlists should be organized :-)).
* Good playlists and music is a subjective topic, so it may be a good playlist for one but a bad playlist for another.

How do you make good playlists then? We simply use the silhouette score of the clusters to judge the quality of the clusters.

## How to get started?

1. Clone this repository.
2. Run ```python setup.py install```
3. Copy config.yml.tmpl to config.yml and adjust the placeholders.
4. Run app.py using the following command: ``` python app.py ```
5. Enjoy your freshly created playlists.

### Packages required

```
requests>=2.3.0,
six>=1.10.0,
spotipy>=2.4.4,
spotify-token>=0.1.0,
pandas>=0.23.4,
numpy>=1.15.4,
scikit-learn>=0.20.1
```

## Configuration explained

Below you can see an explanation of the config file. You need to specify everything in the ```auth``` and ```spotify``` section.

```yaml

auth:                                           # --- Authentication section
    username: YOUR_USERNAME_GOES_HERE           # Username of Spotify goes here
    password: YOUR_PASSWORD_GOES_HERE           # Password of Spotify goes here
spotify:                                        # --- Spotify section
    playlist: PLAYLIST_TO_ANALYZE_GOES_HERE     # Define the playlist to work with here
    username: YOUR_USERNAME_GOES_HERE           # Username to which playlist belongs, should be your own username
    output:                                     # --- Spotify output section
        prefix: PREFIX_GOES_HERE                # Define a prefix which will be used to tag the generated playlists
app:                                            # --- App section
    logging:                                    # --- App logging section
        level: DEBUG                            # Specify logging level. You see everything happening in the application using DEBUG.
        file: true                              # Specify whether logging should be stored to file. If set to false logging is effectively disabled.
        logpath: log                            # Specify where to store the logs. Default is the 'log' folder.
    data:                                       # --- App data section
        path: data                              # Path where to read and write data (in our case we use pickles)
    transformation:                             # --- App transformation section
        use_standard_scaler: false              # Use a standard scaler or use the manually defined transformation rules. Recommended: false
    clustering:                                 # --- App clustering section
        sophisticated: true                     # Use a sophisticated clustering algorithm. Recommended: true (true = AffinityPropagation, false = kMeans)
        unsophisticated_cluster_count: 2        # Define how many clusters should be used when using kMeans. Recommended: 2

```

## Structure

```

- data                                          # Default data folder
- log                                           # Default log folder
- spoton                                        # Application code folder
| - extract.py                                  # Script that holds the extraction logic
| - transform.py                                # Script that holds the transformation rules and clustering
| - load.py                                     # Script that loads the results back to Spotify
| - utils.py                                    # Utils class that holds function to authenticate with Spotify and provides an interface to the config.
- app.py                                        # Application script - run this to run the code.
- config.yml.tmpl                               # The template for a new config file. Create your own config file called "config.yml".
- data_exploration.[ipynb,html]                 # Iphython notebook which holds analysis of the problem.
- README.md                                     # This readme
- setup.py                                      # Setup script

```

## Discussion

My extended insight can be found on Medium. <<Link will follow>>
