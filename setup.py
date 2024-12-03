from setuptools import setup, find_packages

setup(
    name='music_recommender',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'scikit-learn',
        'spotipy',
        'flask'
    ],
    description='A music recommendation system based on Spotify audio features.',
    author='Liang Jimenez',
    author_email='liang.jimenez@gmail.com',
    url='https://github.com/liangjimenez0/music-recommender',
)
