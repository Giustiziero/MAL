import pandas as pd

def get_suggestions(query, similarity_df):
    # Filter the anime titles based on the query
    suggestions = [title for title in similarity_df.columns if query in title.lower()]
    return suggestions
