import requests
from bs4 import BeautifulSoup
from wikidata.client import Client

class DataExtractor:
    def __init__(self, tmdb_api_key, omdb_api_key):
        print("Initializing the Data Extractor")
        self.tmdb_api_key = tmdb_api_key
        self.omdb_api_key = omdb_api_key
        self.WIKIPEDIA_API_URL = 'https://en.wikipedia.org/w/api.php'  

    def get_tmdb_data(self, imdb_id):
        try:
            print("Getting data from TMDb")
            url = f'https://api.themoviedb.org/3/find/{imdb_id}?api_key={self.tmdb_api_key}&external_source=imdb_id'
            response = requests.get(url)
            data = response.json()
            if data['movie_results']:
                movie_id = data['movie_results'][0]['id']
                details_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={self.tmdb_api_key}'
                credits_url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={self.tmdb_api_key}'
                keywords_url = f'https://api.themoviedb.org/3/movie/{movie_id}/keywords?api_key={self.tmdb_api_key}'

                details_response = requests.get(details_url).json()
                credits_response = requests.get(credits_url).json()
                keywords_response = requests.get(keywords_url).json()

                title = details_response.get('title', '')
                tmdb_summary = details_response.get('overview', '')
                genres = ', '.join([genre['name'] for genre in details_response.get('genres', [])])
                cast = ', '.join([cast_member['name'] for cast_member in credits_response.get('cast', [])[:5]])  # Top 5 cast members
                director = ', '.join([crew_member['name'] for crew_member in credits_response.get('crew', []) if crew_member['job'] == 'Director'])
                keywords = ', '.join([keyword['name'] for keyword in keywords_response.get('keywords', [])])

                print("Data Extracted from TMDb successfully!")
                return title, tmdb_summary, genres, cast, director, keywords
        except Exception as e:
            print(f"Error fetching TMDb data: {e}")
        return None, None, None, None, None, None

    def get_imdb_plot_synopsis(self, imdb_id):
        try:
            print("Getting data from IMDb")
            url = f"https://www.imdb.com/title/{imdb_id}/plotsummary/?ref_=tt_stry_pl#synopsis"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                return None

            soup = BeautifulSoup(response.text, 'lxml')
            summary_div = soup.find('div', {'data-testid': 'sub-section-synopsis'})
            if not summary_div:
                return None

            inner_divs = summary_div.find_all('div', {'class': 'ipc-html-content-inner-div', 'role': 'presentation'})
            for div in inner_divs:
                text = div.get_text(strip=True)
                if text:
                    print("Data Extracted from IMDb successfully!")
                    return text
        except Exception as e:
            print(f"Error fetching IMDb plot synopsis: {e}")
        return None

    def get_wikipedia_plot_summary(self, imdb_id):
        try:
            client = Client()
            external_ids_url = f'https://api.themoviedb.org/3/movie/{imdb_id}/external_ids?api_key={self.tmdb_api_key}'
            response_external_ids = requests.get(external_ids_url).json()
            wikidata_id = response_external_ids.get('wikidata_id')

            if not wikidata_id:
                return None

            entity = client.get(wikidata_id, load=True)
            movie_data = entity.data
            wikipedia_url = movie_data['sitelinks']['enwiki']['url']
            page_title = wikipedia_url.split('/')[-1]

            print("Getting data from Wikipedia")
            params = {
                'action': 'query',
                'titles': page_title,
                'prop': 'extracts',
                'format': 'json',
                'exintro': True,
                'explaintext': True,
            }
            response = requests.get(self.WIKIPEDIA_API_URL, params=params).json()
            page = list(response['query']['pages'].values())[0]

            if 'extract' in page:
                extract = page['extract']
                plot_summary = extract.split('\n')[0]
                print("Data Extracted from Wikipedia successfully!")
                return plot_summary.strip()
        except Exception as e:
            print(f"Error fetching Wikipedia plot summary: {e}")
        return None

    def get_omdb_summary(self, imdb_id):
        try:
            print("Getting data from OMDb")
            url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={self.omdb_api_key}"
            response = requests.get(url)
            data = response.json()

            if data['Response'] == 'True':
                print("Data Extracted from OMDb successfully!")
                return data.get('Plot', '')
            else:
                print(f"Error: {data['Error']}")
        except Exception as e:
            print(f"Error fetching OMDb data: {e}")
        return None

    def extract_data(self, imdb_id):
        print("Extracting movie data")
        title, tmdb_summary, genres, cast, director, keywords = self.get_tmdb_data(imdb_id)
        imdb_plot_synopsis = self.get_imdb_plot_synopsis(imdb_id)
        wikipedia_plot_summary = self.get_wikipedia_plot_summary(imdb_id)
        omdb_summary = self.get_omdb_summary(imdb_id)
        print("Movie data extraction complete!")

        return {
            'IMDb ID': imdb_id,
            'Title': title,
            'Plot Synopsis (IMDb)': imdb_plot_synopsis,
            'Movie Summary (TMDb)': tmdb_summary,
            'About Movie (Wikipedia)': wikipedia_plot_summary,
            'Plot Summary (OMDb)': omdb_summary,
            'Director': director,
            'Cast': cast,
            'Genres': genres,
            'Keywords': keywords
        }