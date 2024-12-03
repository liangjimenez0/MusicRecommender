import pandas as pd

# Define the function to load the dataset
def load_dataset(url):
    df = pd.read_csv(url)
    return df
