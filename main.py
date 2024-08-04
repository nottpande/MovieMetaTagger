import pandas as pd
import os
from data_extractor import DataExtractor
from tag_generator import TagGenerator
from score_tag import TagScorer

# Initialize API keys
os.environ['OPENAI_API_KEY'] = 'open_api_key'
os.environ['TMDB_API_KEY'] = 'tmdb_api_key'
os.environ['OMDB_API_KEY'] = 'omdb_api_key'

openai_api_key = os.getenv('OPENAI_API_KEY')
tmdb_api_key = os.getenv('TMDB_API_KEY')
omdb_api_key = os.getenv('OMDB_API_KEY')

# Initialize classes
data_extractor = DataExtractor(tmdb_api_key, omdb_api_key)
tag_generator = TagGenerator(openai_api_key)
tag_scorer = TagScorer(openai_api_key)

def process_movie(imdb_id):
    movie_data = data_extractor.extract_data(imdb_id)
    print("\n")
    tags = tag_generator.generate_tags(movie_data)
    print("\n")
    movie_data['tags'] = tags
    scored_tags = tag_scorer.score_tags(movie_data)
    print("\n")
    movie_data['Tag Scores'] = scored_tags
    return movie_data

def process_movies(imdb_ids):
    results = []
    for imdb_id in imdb_ids:
        print("\n\n")
        print(f"Processing IMDb ID: {imdb_id}")
        movie_data = process_movie(imdb_id)
        results.append(movie_data)
        print("\n\n")
    df = pd.DataFrame(results)
    return df


imdb_ids = ["tt15398776","tt0816692","tt26047818","tt9466114","tt15671028"]   #['Oppenheimer','Interstellar','Anyone But You','The Idea of You','No Hard Feelings']
df_movies = process_movies(imdb_ids)
df_movies.to_csv('sample.csv')
print(df_movies)
