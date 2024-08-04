import openai
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import pandas as pd
from tqdm import tqdm

class TagGenerator:
    def __init__(self, openai_api_key, model_name="gpt-4o", temperature=0):
        print("Initializing the Tag Generator")
        os.environ['OPENAI_API_KEY'] = openai_api_key
        openai.api_key = os.getenv('OPENAI_API_KEY')

        self.llm = ChatOpenAI(temperature=temperature, model_name=model_name)
        
        self.tags_generator_template = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful assistant that generates metadata tags for movies."),
                ("human", 
                    '''
                        Generate concise, contextually relevant, and descriptive metadata tags to enhance the movie metadata for an OTT platform. Please generate detailed tags related to the movie using the following information:
                        Title: {title}
                        Plot Synopsis (IMDb): {plot_imdb}
                        Movie Summary (TMDb): {plot_tmdb}
                        About Movie (Wikipedia): {plot_wikipedia}
                        Plot Summary (OMDb): {plot_omdb}
                        Director: {director}
                        Cast: {cast}
                        Genres: {genres}
                        Keywords: {keywords}

                        The tags should cover the main context of the movie, providing concise information, optimizing search results, and improving the movie's reach. Ensure each tag accurately reflects the movie's content without categorization or distinction between types. Limit the tags to 100 tags.

                        Aspects to be covered:
                        1. Plot Details:
                            - 'Plot Synopsis (IMDb)'
                            - 'Movie Summary (TMDb)'
                            - 'About Movie (Wikipedia)'
                            - 'Plot Summary (OMDb)'
                            Use these to generate tags related to the plot, location, setting, type of protagonist and antagonist, relationships, target audience, occasion, crime type, investigation agency, ethnicity, type of faith, climax, emotions, family dynamics, cultural factors, phobias, and based on.
                            Instructions:
                            - Use the provided plot and story details to extract relevant tags.
                            - Leverage your own knowledge to generate additional contextually relevant tags.
                            - Identify key elements, themes, and concepts from the plot descriptions to ensure comprehensive coverage.

                        2. Direct Information:
                            - 'Director'
                            - 'Cast'
                            - 'Genres'
                            - 'Keywords'
                            Use these to generate tags for the director, cast, genres, and additional keywords.
                            Instructions:
                            - Use the provided information to generate accurate tags.
                            - Supplement with additional knowledge where applicable.

                        3. Additional Knowledge:
                            - Utilize your own knowledge to generate tags related to awards, cinematography style, music/composer, budget/box office, runtime, production studio, franchise, and release date, writer, distributor.
                            Instructions:
                            - Use your knowledge to generate tags for these aspects.
                            - Ensure tags are relevant and accurately reflect the movie's context.

                        Example:
                        Here is an example output format for the movie 'The Duel' (2016) starring Woody Harrelson and directed by Kieran Darcy-Smith:
                        Western, Action, Drama, Thriller, Revenge, Duel, Texas, Lawman, Outlaw, Murder, Series of disappearances, Cowboy, Sheriff, Ranger, Small western town, Bar shootout, Stabbing, Violence, Internal conflict, Selfish individualism, Common good, Unexplained deaths, Double barrel shotgun, Rifle, Revolver, 1880s, 19th Century, Hero, Villain, Lawman-Outlaw Rivalry, Romantic Partners, Husband-Wife Relationship, Father-Son Relationship, Villain as protagonist, Adults, Date Night, American, American West Culture, Heterosexual, Tension, Suspense, Original Screenplay, Kieran Darcy-Smith, Woody Harrelson, Liam Hemsworth, Alice Braga, Emory Cohen, Josh Whites, Benedict Samuel, Craig Eastman, Matt Cook, Atomic Entertainment, Mandeville Films, Mississippix Studios, 26 Films, Bron Capital Partners, Crystal Wealth, Lionsgate Premiere, 2016 movie, Watchable and decent Western movie, Surprise, English, Lawman investigating mysterious disappearances, Confrontation between lawman and outlaw, Psychological tension, Gritty realism, Frontier justice, Masculine identity, Power struggle, Survival, Justice and morality, Community vs. individualism, Heroic sacrifice, Moral ambiguity, Ethical dilemmas, Showdown, Desert landscape, Law enforcement, Gunfight, Tracking, Investigation, Cover-up, Corruption, Vengeance, Honor, Frontier life, Mentor-student relationship, Brotherhood, Loyalty, Betrayal, Redemption, Love triangle, Revenge-driven characters, Strong-willed woman, Cinematic vistas, Period-accurate costumes, Atmospheric tension, Harsh terrain, Dusty towns, Saloon confrontations, Emotional conflict, Fear and bravery, Grief, Determination, Ruthlessness, Inner demons, High-stakes conflict, Fast-paced action, Hand-to-hand combat, Strategic mind games, Physical endurance.
                        Notice how the tags describe the plot of the movie pretty well and we get an idea that the movie is a western-themed movie released in 2016 that has a lot of violence, murders, and people missing associated with it. There is a relationship between a father and a son, and a husband and wife in the movie who are romantically active. The possible reason for violence is internal conflicts. The main actors and actresses we can see in the movie are Woody Harrelson, Liam Hemsworth, and Alice Braga. Hence it covers a lot of aspects of the movie.
                        
                        Instructions:
                        - Ensure tags are contextually relevant and descriptive.
                        - Maintain a logical order of importance and relevance.
                        - Use the instructions effectively to cover all listed aspects.
                        - No tag must be repeated, i.e., all the tags must be unique
                        - Generate 100 unique tags for each movie.
                    '''
                )
            ]
        )

        self.tags_cleaner_template = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful assistant that will help to clean the metadata tags for movies."),
                ("human",
                    '''
                    Here are the tags for the movie:
                    tags : {tags}
                    
                    Clean and refine the list of metadata tags generated for movies to ensure they are unique, relevant, and descriptive. Follow these instructions to remove unwanted, repeated, and irrelevant tags:
                    1. Remove Duplicates:
                    - Identify and remove any repeated tags from the list.

                    2. Eliminate Irrelevant Tags:
                    - Review each tag and ensure it is relevant to the movie's content. Remove tags that do not accurately reflect the movie’s context or are not useful for enhancing metadata.
                    
                    3. Refine Tags:
                    - Ensure that each tag provides unique and meaningful information about the movie. Remove tags that are too broad or generic, and replace them with more specific and descriptive ones where possible.
                    
                    4. Organize and Categorize:
                    - Arrange the tags in a logical order based on their importance and relevance to the movie. Prioritize tags that give clear insights into the movie's plot, genre, characters, setting, and themes.
                    
                    Finally, once everything is done, then provide the tags only, where the tags are comma separated. That is:
                    tag1, tag2, tag3 , ........... , tagN
                    
                    Example: 
                        Input:
                        - Teenage Girl, Teenage Romance, Teenage Life, Teenage Drama, Teenage Angst, Teenage Rebellion, Teenage Problems, Teenage Anxiety, Teenage Fear, Teenage Survival, Teenage Independence, Teenage Adventure, Teenage Rebellion, Teenage Rebellion, Teenage Rebellion, Teenage Rebellion, Teenage Rebellion, Teenage Rebellion, Teenage Rebellion, Teenage Rebellion, Teenage Rebellion, Teenage Rebellion, Teenage Rebellion, Teenage Rebellion, Teenage Rebellion, Teenage Rebellion

                        Expected Output:
                        - Teenage Girl, Teenage Romance, Teenage Drama, Teenage Angst, Teenage Independence, Teenage Adventure, Teenage Survival, Teenage Rebellion

                        Things done in the example:
                        - Remove all duplicate instances of Teenage Rebellion.
                        - Verify if tags like Teenage Life, Teenage Romance, and Teenage Adventure are relevant. If any of these do not fit the movie’s context or are too broad, remove or refine them.
                        - Ensure that the remaining tags provide clear and distinct information about the movie.
                    
                    Instructions for the Tag Cleaner:
                    - Remove duplicate tags.
                    - Eliminate tags that are not relevant to the movie’s context.
                    - Ensure the remaining tags are unique, specific, and provide a clear description of the movie.
                    - Organize the tags based on their relevance and importance to the movie.
                    '''
                )
            ]
        )

        self.tags_generator = self.tags_generator_template | self.llm
        self.tags_cleaner = self.tags_cleaner_template | self.llm

    def generate_tags(self, movie_data):
        input_data = {
            'title': movie_data['Title'],
            'plot_imdb': movie_data['Plot Synopsis (IMDb)'],
            'plot_tmdb': movie_data['Movie Summary (TMDb)'],
            'plot_wikipedia': movie_data['About Movie (Wikipedia)'],
            'plot_omdb': movie_data['Plot Summary (OMDb)'],
            'director': movie_data['Director'],
            'cast': movie_data['Cast'],
            'genres': movie_data['Genres'],
            'keywords': movie_data['Keywords']
        }
        print("Generating and Cleaning tags based on the movie details extracted")
        with tqdm(total=1, desc=f"Generating tags for {movie_data['Title']}", leave=False) as pbar_gen:
            generated_tags = self.tags_generator.invoke(input_data).content
            pbar_gen.update(1)

        cleaning_input_data = {
            'tags': generated_tags
        }

        with tqdm(total=1, desc=f"Cleaning tags for {movie_data['Title']}", leave=False) as pbar_clean:
            cleaned_tags = self.tags_cleaner.invoke(cleaning_input_data).content
            pbar_clean.update(1)

        print("Tags Generated and Cleaned Successfully!")
        return cleaned_tags