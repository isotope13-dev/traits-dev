def select(X, index):
    if hasattr(X, "iloc"):
        return X.iloc[index]
