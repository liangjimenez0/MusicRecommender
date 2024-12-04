import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from recommender import data_loader, normalizer, recommender
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import base64

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# Load and prepare data
dataset_url = "hf://datasets/maharshipandya/spotify-tracks-dataset/dataset.csv"
df = data_loader.load_dataset(dataset_url)

# Drop unnecessary index column if not needed
df = df.drop(columns=['Unnamed: 0'])

# Handle missing values by dropping or filling them
df = df.dropna(subset=['artists', 'album_name', 'track_name'])

# Ensure unique entries in the dataset by dropping duplicates
df = df.drop_duplicates(subset=['track_name', 'artists'])

# Define audio features to be used
audio_features = [
    'danceability', 'energy', 'loudness', 'speechiness', 
    'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'
]

# Check if all required audio features are present in the DataFrame
missing_features = [feature for feature in audio_features if feature not in df.columns]
if missing_features:
    raise ValueError(f"Missing required audio features: {missing_features}")

# Normalize features
df, scaler = normalizer.normalize_features(df, audio_features)

@app.route('/search', methods=['GET'])
def search_songs():
    query = request.args.get('query', '').lower()
    if not query:
        return jsonify({"songs": []}), 200

    # Filter songs by track_name containing the query string and limit to top 10
    matching_songs = df[df['track_name'].str.lower().str.contains(query)].head(10)
    
    # Convert to list of dictionaries for JSON response
    songs_list = matching_songs[['track_id', 'track_name', 'artists']].to_dict(orient='records')
    
    return jsonify({"songs": songs_list})

@app.route('/recommend', methods=['GET'])
def recommend():
    song_name = request.args.get('song')
    if not song_name:
        return jsonify({"error": "Song name is required"}), 400

    # Find the song details from the dataset
    song_details = df[df['track_name'].str.lower() == song_name.lower()]
    if song_details.empty:
        return jsonify({"error": "Song not found in the dataset"}), 404

    # Get the artist(s) for the searched song
    searched_artist = song_details.iloc[0]['artists']
    searched_track_name = song_details.iloc[0]['track_name']

    # Get recommendations
    recommendations = recommender.recommend_with_data(df, scaler, audio_features, song_name, top_n=20)  # Fetch more than 10 initially to account for filtering
    if recommendations is None or recommendations.empty:
        return jsonify({"error": "No recommendations found"}), 404

    # Filter out the same song and artist
    recommendations = recommendations[
        ~((recommendations['track_name'].str.lower() == searched_track_name.lower()) &
          (recommendations['artists'].str.lower() == searched_artist.lower()))
    ]

    # Limit to the top 10 results after filtering
    recommendations = recommendations.head(10)

    try:
        # Format artists for JSON response
        recommendations['artists'] = recommendations['artists'].apply(
            lambda x: ', '.join(x.split(';')) if isinstance(x, str) else x
        )
        json_data = recommendations[['track_name', 'artists']].to_dict(orient='records')
    except Exception as e:
        return jsonify({"error": f"Failed to prepare recommendations: {str(e)}"}), 500

    return jsonify({"recommendations": json_data})


if __name__ == '__main__':
    app.run(debug=True)