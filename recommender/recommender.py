import numpy as np
import pandas as pd
from .similarity import get_recommendations

# Define the function to recommend songs based on a given song name
def recommend_with_data(df, scaler, audio_features, song_name, top_n=10):
    # Ensure unique entries in the dataset by dropping duplicates
    df = df.drop_duplicates(subset=['track_name', 'artists'])

    # Try to find the song in the dataset
    song_data = df[df['track_name'].str.lower() == song_name.lower()]
    if not song_data.empty:
        try:
            song_vector = scaler.transform(song_data[audio_features].values)
        except ValueError as e:
            print(f"Scaler transformation error: {e}")
            return None

        # Get recommendations based on the song vector
        return get_recommendations(df, song_vector, audio_features, top_n)