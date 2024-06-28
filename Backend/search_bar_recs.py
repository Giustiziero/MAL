import pandas as pd

def get_suggestions(query, index_dict):
    anime_list = list(index_dict.keys())
    # Filter the anime titles based on the query
    suggestions = [title for title in anime_list if query in title.lower()]
    return suggestions
