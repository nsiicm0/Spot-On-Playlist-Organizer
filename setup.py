from setuptools import setup

setup(
    name='spoton',
    version='0.0.1',
    description='A spotify playlist organizer',
    author="nsiicm0",
    author_email="nsiicm0@gmail.com",
    install_requires=[
        'requests>=2.3.0',
        'six>=1.10.0',
        'spotipy>=2.4.4'
    ],
    packages=['spoton'])