<h1> MovieMetaTagger (Natural Language Processing Project) </h1>
        <p><strong>Overview:</strong> This is a NLP project, where we try to generate tags for a given movie,, after extracting details about the movvie using its IMDb ID <br>
        The project uses BeautifulSoup for web--scraping and uses LangChain to manage the interaction with the OpenAI API for generating and cleaning tags.</p>
<h5> Approach for the Project</h5>
<p> For this project, we made three major classes: </p>

<br>
  <li> <b> DataExtractor Class </b> </li>
  <li> This class is used to extract the data about the movie, using the IMDb ID of the movie, during the initialization of an object of this class, there are two things required:<br>
        1. The TMDb API key
        2. The OMDb API key
  Once the object is initialized for the Class, we will then use the <b><i>extract_data</i></b> function of this class, to get the details of the movie, using the IMDb ID.<br>
  The function will return a dictionary containing the following details of the movie: <br>
  <i>'IMDb ID', 'Title', 'Plot Synopsis (IMDb)', 'Movie Summary (TMDb)', 'About Movie (Wikipedia)', 'Plot Summary (OMDb)', 'Director', 'Cast', 'Genres', 'Keywords'</i>
  <br><br>
  The class extracts data from multiple sources:<br>
  - IMDb: Plot synopsis and basic information.<br>
  - TMDb: Movie summary, genres, cast, and keywords.<br>
  - OMDb: Plot summary.<br>>
  - Wikipedia: Detailed plot summary using Wikidata. </li>
<hr>
<li> <b> TagGenerator Class </b> </li>
  <li> This class is used to generate the tags for the movie, based on the details that were extracted by the previous class. There are two things that, this class essentially does:<br>
        1. It generates tags based on the movie details extracted.
        2. It then cleans the generated tags, i.e., it removes repeated tags, removes irrelevant tags etc.

During the initialization of an object of this class, there are three things required:<br>
1. The API key for OpenAI<br>
2. The model that we are going to use (in our case, I have set it to <b><i>GPT-4</i></b> by default, this can be changed)<br>
3. The temperature value (this is used to control the randomness of the generation) (in our case, I have set it to <b><i>0</i></b> by default, as we want our model to be deterministic, and produce less random outputs, but this can too be changed)<br>

Once the object is initialized for the Class, we will then use the <b><i>generate_tags</i></b> function of this class, to generate tags based on the movie details.<br>

The function will return a list containing the tags for the movie. <br>
The class uses LangChain to manage the interaction with the OpenAI API for generating and cleaning tags.<br>

- tags_generator_template: This is the prompt template, that is used for generating the tags.
- tags_cleaner_template: This is the prompt template, that is used for cleaning the generated tags. </li>
<hr>
<li> <b> TagScorer Class </b> </li>
  <li> This class is used to score the tags for the movie, based on based on their relevance to the movie details.<br>
        During the initialization of an object of this class, there is only one thing required:<br>
        1. The API key for OpenAI <br>
        This time, I did not add the model name and the temperature, because I assumed it will be the same as for the previous class.<br>
        <i> Incase the parameters (model name and temperature) is changed in the TagGenerator Class, then make sure to change it here too</i>

Once the object is initialized for the Class, we will then use the <b><i>score_tags</i></b> function of this class, to score the tags, based on the movie details<br>

The function will return a list containing the scored tags for the movie. <br>
The class also uses LangChain to manage the interaction with the OpenAI API for scoring the tags.<br>

- tags_scoring_template: This is the prompt template, that is used for scoring the tags. </li>
<h6> Keep in mind, that the scores of the tags will in general be pretty high, as the previous class has made sure only the 'relevant' tags of the movies will remain in the tags. <br>
Hence, as the tags will seem pretty relevant based on the movie details, therefore the scores will automatically be pretty high.</h6>


