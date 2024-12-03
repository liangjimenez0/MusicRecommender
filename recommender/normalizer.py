from sklearn.preprocessing import MinMaxScaler

# Define the function to normalize features
def normalize_features(df, columns):
    scaler = MinMaxScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df, scaler
