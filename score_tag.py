import openai
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from tqdm import tqdm

class TagScorer:
    def __init__(self, api_key):
        print("Initializing the Tag Scorer")
        os.environ['OPENAI_API_KEY'] = api_key
        openai.api_key = os.getenv('OPENAI_API_KEY')

        # Initialize the scoring template and model
        self.tags_scoring_template = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful assistant that will help to score metadata tags for movies."),
                (
                    "human",
                    """
                    We have generated metadata tags for movies, and now we need to score each tag based on how much sense it makes with the movie information shared with you. The movie details are found in the following columns:
                    Title: {title}
                    Plot Synopsis (IMDb): {plot_imdb}
                    Movie Summary (TMDb): {plot_tmdb}
                    About Movie (Wikipedia): {plot_wikipedia}
                    Plot Summary (OMDb): {plot_omdb}
                    Director: {director}
                    Cast: {cast}
                    Genres: {genres}
                    Keywords: {keywords}
                    Tags : {tags}

                    Each tag present in 'Tags' will be scored out of 10, with 10 being the highest score indicating that the tag is highly relevant and makes perfect sense with the movie details, and 1 being the lowest score indicating that the tag is not relevant at all.

                    Steps to Score the Tags:
                    1. Understanding the Context:
                    - Understand the context of the summaries in all the columns, including keywords, cast, director, etc.
                    2. Evaluate the Tag:
                    - Score each tag in the "tags" column based on how well it fits with the information understood from the various columns.
                    - Use your understanding and context to ensure that each tag is accurately scored.
                    3. Scoring Criteria:    
                    - 10: The tag is highly relevant and makes perfect sense with the movie.
                    - 8-9: The tag is mostly relevant and makes good sense with the movie.
                    - 6-7: The tag is somewhat relevant but may not cover key aspects of the movie.
                    - 4-5: The tag has limited relevance and does not fully align with the movie.
                    - 2-3: The tag is minimally relevant and mostly does not align with the movie.
                    - 1: The tag is not relevant at all and makes no sense with the movie.
                    
                    Expected Output:
                    Finally, once everything is done, then provide the tags and scores only, where each tag and score combination is comma separated. That is:
                    tag1 : score1, tag2 : score2, tag3 : score3 , ........... , tagN : scoreN

                    Example:
                    For the movie "The Duel" (2016), the tags and their scores could be:
                    
                    Western:10, Action:10, Duel:10, Revenge:9, Texas:8, Lawman:8, 1880s:7, Hero:6, Villain:6, Romantic Partners:5, Date Night:4, American:7, Surprise:6, English:10, Tension:8, Suspense:7, Father-Son Relationship:5, American West Culture:8, Original Screenplay:6, Woody Harrelson:10, Liam Hemsworth:10, Alice Braga:9
                    
                    Instructions:
                    1. Understand the context for each movie:
                    - Read and comprehend the information provided in the ‘Plot Synopsis (IMDb)’, ‘Movie Summary (TMDb)’, ‘About Movie (Wikipedia)’, and ‘Plot Summary (OMDb)’ and all the other columns.
                    2. Evaluate and score each tag:
                    - Score each tag in the "tags" column based on its relevance to the movie summaries.
                    3. Format the scores:
                    - Format the scores as 'tag: tag score', ensuring all tags are scored out of 10.
                    4. Ensure accuracy:
                    - Make sure the scores are accurate and based on the context provided by the movie details.
                    """
                )
            ]
        )

        self.llm = ChatOpenAI(temperature=0, model_name="gpt-4o")
        self.tags_scoring_model = self.tags_scoring_template | self.llm

    def score_tags(self, row):
        print("Scoring the tags generated")
        input_data = {
            'title': row['Title'],
            'plot_imdb': row['Plot Synopsis (IMDb)'],
            'plot_tmdb': row['Movie Summary (TMDb)'],
            'plot_wikipedia': row['About Movie (Wikipedia)'],
            'plot_omdb': row['Plot Summary (OMDb)'],
            'director': row['Director'],
            'cast': row['Cast'],
            'genres': row['Genres'],
            'keywords': row['Keywords'],
            'tags': row['tags']
        }
        with tqdm(total=1, desc=f"Scoring the tags for {row['Title']}", leave=False) as pbar_gen:
            scored_tags = self.tags_scoring_model.invoke(input_data).content
            pbar_gen.update(1)
        
        print("The tags have been scored!")
        return scored_tags
