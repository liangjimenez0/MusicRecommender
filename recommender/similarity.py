from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Define the function to get recommendations based on a song vector
def get_recommendations(df, song_vector, columns, top_n=10):
    # Compute cosine similarity
    similarities = cosine_similarity(song_vector, df[columns].values)
    similar_indices = np.argsort(similarities[0])[::-1][:top_n]  # Sort and take top N
    
    return df.iloc[similar_indices]
