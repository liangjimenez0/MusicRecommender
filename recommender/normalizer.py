from sklearn.preprocessing import MinMaxScaler

def normalize_features(df, columns):
    # Ensure columns exist in df and no spaces are in column names
    df.columns = df.columns.str.strip()  # Strip any leading/trailing spaces from column names
    
    # Check if all specified columns are in the dataframe
    missing_columns = [col for col in columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing columns for normalization: {missing_columns}")

    scaler = MinMaxScaler()
    # Fit and transform only the columns you need
    df[columns] = scaler.fit_transform(df[columns])
    
    return df, scaler

