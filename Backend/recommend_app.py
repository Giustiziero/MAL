from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
from query_sim_mat import get_similar_animes, get_index_dict
from search_bar_recs import get_suggestions  # Import the new function from database module

app = Flask(__name__)
CORS(app)

# Load your similarity DataFrame (assuming it's stored as a CSV file locally)
# similarity_df = pd.read_csv('./Temp_data/cosine_sim_mat.csv', index_col=0)
index_dict = get_index_dict()

@app.route('/get_similar_animes', methods=['GET'])
def get_similar_animes_endpoint():
    anime_name = request.args.get('anime_name')
    top_n = request.args.get('top_n', default=25, type=int)

    if not anime_name:
        return jsonify({'error': 'Anime name is required'}), 400

    try:
        similar_animes = get_similar_animes(anime_name, index_dict, top_n)
        # Convert the Series to a list of tuples
        similar_animes_list = list(similar_animes.items())
        return jsonify(similar_animes_list)
    except KeyError:
        return jsonify({'error': 'Anime not found in the similarity matrix'}), 404

@app.route('/api/suggestions', methods=['GET'])
def get_suggestions_endpoint():
    query = request.args.get('query', '').lower()
    if not query:
        return jsonify(list(index_dict.keys()))

    suggestions = get_suggestions(query, index_dict)
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)
