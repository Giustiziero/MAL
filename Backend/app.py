from flask import Flask, request, jsonify, render_template
import pandas as pd
from flask_cors import CORS
from anime_recommender_service import AnimeRecommenderService
from search_bar_recs import get_suggestions  # Import the new function from database module
import logging 
from Utils.MAL_connection.MAL_API_fetcher import MAL_API_Fetcher
from database_handler import DatabaseHandler
from Utils.MAL_connection.MAL_API_Connector import MAL_API_Connector

app = Flask(__name__)
CORS(app)

# Configure logging ded
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("file just ran")
# Load your similarity DataFrame (assuming it's stored as a CSV file locally)
# similarity_df = pd.read_csv('./Temp_data/cosine_sim_mat.csv', index_col=0)
try: 
    connector = MAL_API_Connector(None)
    fetcher = MAL_API_Fetcher(connector)
except Exception as e:
    fetcher = None
    logger.warning(f"Failed to start fetcher: {e.message}")

try: 
    db_handler = DatabaseHandler('MalRecCosmos')
except Exception as e:
    logger.warning(f"Failed to start db_handler: {e.message}")
    db_handler = None
    
anime_service = AnimeRecommenderService(db_handler, fetcher)

try: 
   index_dict = anime_service.get_index_dict()
   logger.info("Just ran get_index")
except Exception as e:
   logger.info("Failed to run get_index")
   logger.warning(str(e))

@app.route('/')
def index():
   logger.info('Request for index page received')
   return render_template('index.html')

@app.route('/get_similar_animes', methods=['GET'])
def get_similar_animes_endpoint():
    logger.info("get similar anime received")
    anime_name = request.args.get('anime_name')
    top_n = request.args.get('top_n', default=25, type=int)

    if not anime_name:
        return jsonify({'error': 'Anime name is required'}), 400

    try:
        similar_animes = anime_service.get_similar_animes(anime_name, index_dict, top_n)
        # Convert the Series to a list of tuples
        similar_animes_list = list(similar_animes.items())
        return jsonify(similar_animes_list)
    except KeyError:
        return jsonify({'error': 'Anime not found in the similarity matrix'}), 404

@app.route('/api/suggestions', methods=['GET'])
def get_suggestions_endpoint():
    logger.info("get suggestions received")
    query = request.args.get('query', '').lower()
    if not query:
        return jsonify(list(index_dict.keys()))

    suggestions = get_suggestions(query, index_dict)
    return jsonify(suggestions)

@app.route('/api/anime_details', methods=['GET'])
def get_specific_anime_details():
    """
    API endpoint to get anime details.
    Accepts a query parameter 'fields' to filter the response fields.
    """
    anime_name = request.args.get('anime_name')
    fields = request.args.get('fields', '').split(',')  # Get fields as a list
    
    if not anime_name:
        return jsonify({"error": "anime_name is required"}), 400
    
    try: 
        anime_details = anime_service.get_anime_details(anime_name)
    except Exception as e:
        logger.warning(f"Error: {e.message}")
        return jsonify({"error": "Specific details about {anime_name} can be found at myanimelist.net"}), 404

    # If specific fields are requested, filter the anime details
    if fields and fields != ['']:  # Ensure it's not an empty list
        anime_details = {field: anime_details.get(field) for field in fields if field in anime_details}
    
    return jsonify(anime_details), 200

if __name__ == '__main__': 
    app.run()
    # try:
    #     app.run(host='0.0.0.0')
    # except Exception as e:
    #     logger.exception("Failed to start the application")

