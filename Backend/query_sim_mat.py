# from flask import Flask, request, jsonify
# import pandas as pd
# import pdb
# from flask_cors import CORS


# app = Flask(__name__)
# CORS(app)

# # Load your similarity DataFrame (assuming it's stored as a CSV file locally)
# similarity_df = pd.read_csv('./Temp_data/cosine_sim_mat.csv', index_col=0)

# def get_similar_animes(anime_name, similarity_df, top_n=25):
#     similar_animes = similarity_df[anime_name].sort_values(ascending=False)
#     return similar_animes.head(top_n + 1).iloc[1:]  # Exclude the anime itself

# @app.route('/get_similar_animes', methods=['GET'])
# def get_similar_animes_endpoint():
#     anime_name = request.args.get('anime_name')
#     top_n = request.args.get('top_n', default=25, type=int)

#     if not anime_name:
#         return jsonify({'error': 'Anime name is required'}), 400

#     try:
#         similar_animes = get_similar_animes(anime_name, similarity_df, top_n)
#         similar_animes_dict = similar_animes.to_dict()
#         return jsonify(similar_animes_dict)
#     except KeyError:
#         return jsonify({'error': 'Anime not found in the similarity matrix'}), 404

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load your similarity DataFrame (assuming it's stored as a CSV file locally)
similarity_df = pd.read_csv('./Temp_data/cosine_sim_mat.csv', index_col=0)

def get_similar_animes(anime_name, similarity_df, top_n=25):
    similar_animes = similarity_df[anime_name].sort_values(ascending=False)
    similar_animes = similar_animes.head(top_n + 1).iloc[1:]  # Exclude the anime itself
    similar_animes = (similar_animes * 100).round(1)
    return similar_animes

@app.route('/get_similar_animes', methods=['GET'])
def get_similar_animes_endpoint():
    anime_name = request.args.get('anime_name')
    top_n = request.args.get('top_n', default=25, type=int)

    if not anime_name:
        return jsonify({'error': 'Anime name is required'}), 400

    try:
        similar_animes = get_similar_animes(anime_name, similarity_df, top_n)
        # Convert the Series to a list of tuples
        similar_animes_list = list(similar_animes.items())
        return jsonify(similar_animes_list)
    except KeyError:
        return jsonify({'error': 'Anime not found in the similarity matrix'}), 404

if __name__ == '__main__':
    app.run(debug=True)
