import pandas as pd

def get_similar_animes(anime_name, similarity_df, top_n=25):
    similar_animes = similarity_df[anime_name].sort_values(ascending=False)
    similar_animes = similar_animes.head(top_n + 1).iloc[1:]  # Exclude the anime itself
    similar_animes = (similar_animes * 100).round(1)
    return similar_animes
