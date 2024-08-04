<h1> MovieMetaTagger (Natural Language Processing Project) </h1>
        <p><strong>Overview:</strong> This is a NLP project, where we try to generate tags for a given movie,, after extracting details about the movvie using its IMDb ID <br>
        The project uses BeautifulSoup for web--scraping and uses LangChain to manage the interaction with the OpenAI API for generating and cleaning tags.</p>
<h5> Approach for the Project</h5>
<p> For this project, we made three major classes: </p>
<OL>
  <li> <b> Data Extractor Class </b> </li>
  <li> This class is used to extract the data about the movie, using the IMDb ID of the movie, during the initialization of an object of this class, there are two things required:<br>
        1. The TMDb API key
        2. The OMDb API key
  Once the object is initialized for the Class, we will then use the <b><i>extract_data</i></b> function of this class, to get the details of the movie, using the IMDb ID.<br>
  The function will return a dictionary containing the following details of the movie: <br>
  <i>'IMDb ID', 'Title', 'Plot Synopsis (IMDb)', 'Movie Summary (TMDb)', 'About Movie (Wikipedia)', 'Plot Summary (OMDb)', 'Director', 'Cast', 'Genres', 'Keywords'</i>
  <br><br>
  The class extracts data from multiple sources:
  - **IMDb**: Plot synopsis and basic information.
  - **TMDb**: Movie summary, genres, cast, and keywords.
  - **OMDb**: Plot summary.
  - **Wikipedia**: Detailed plot summary using Wikidata. </li>
</OL>
<p> In both the cases, the scores were scaled up, between 0 to 10, using Min-Max Scaler, which was coded from scratch rather than using the sklearn library.</p>


<h6> The predictios made by both the approaches has been attached, and it was obsereved on different test datasets, that the Neural Network Approach seemed to perform better than the Cosine Similarity Approach. Not all the test predictions has been uploaded, only the ones in which each apporach was seen to be the most accurate, has been uploaded.</h6>


<h2> Conclusion drawn: </h2>
<p> The model, predicts a large part of the genre's right, hence scoring them accurately. But then there are a lot of things that need to be kept in mind:</p>
<ol>
  <li> The summary needs to be a proper summary of the movie. That means, it must not be a one liner, or must not tell something in general about the movie and must definitely not be ambiguous. The summary must cover the major plot of the movie, in order for the correct scoring of the genres.</li>
  <li> The model's prediction might not be 100% accurate, as it just provides the genre scores, based on the summary. The model does not know, if the given event is a real event that took place, if the movie is an animated movie or not, the movie is a short of not (unless specified in the summary), hence the prediction cannot be considered 100% accurate.</li>
  <li> The predictions of ChatGPT for the exact same movies has been also uploaded. There is a clear difference seen in the scoring between the two models. The reason I believe that is so, is because, ChatGPT is trained on tons of data, making it more well versed and knowledgeable compared to our model, hence if our model also gets more data, then its performance can definitly be increased.</li>
</ol>
