# Munging Open Data in 15 Python Tutorials

This will be a book of tutorials on munging open data with Python.

The objectives are to teach students about how data is structured in the wild, how it is communicated and can be accessed via APIs, and how to use Python tools for data munging and preparation.  There should be 15 tutorials for a 15 week course.  They will use "open data" sources because these are numerous, timely, and are likely to remain accessible at fairly stable APIs without necessitating API keys or passwords.

##Proposed Tutorials:

1. Introduce Python, iPython Notebook, and pandas.  Introduce data.gov.  Use requests.get to grab a nice simple CSV dataset. (BLS employment?)  Do summary statistics.  Add some calculated columns.  Dump it all out to a new CSV.

1. Introduce Python lists and dicts.  Introduce looping.  Get some relatively clean JSON data (like NOAA tides data).  Show how to access elements by index or key to, for example, print a sentence saying "At time ______, sea level at station _______ is _____ feet".  Now use looping to munge it into a data frame, and output to CSV.

1. Introduce 'length' and 'if/then' in Python.  Munge some JSON data with different types of cases; maybe complaints data with some resolved and some unresolved?  Or some with details and some with none?  Loop through the dataset and filter with if/then; think about how to turn hierarchical data into a tabular format, e.g. by doing counts and sums.

1. Get some XML data that's paginated and has an access rate limit (google maps?).  Show how we can loop to build up a series of URLs.  Create an iterative script and, for each iteration, extract some stuff from XML to add to a growing data frame.  Export as CSV.

1. Traverse an API with multiple endpoints; for example, a list of teams and a list of games, to compute wins/losses.  Loop within loop and do some calculations.  They need to be thinking about generating their own variables by this point.

1. Transform data into a different type of entity/structure; for example, munge an API of "transaction" data (like debits/credits) to produce a timeline of "snapshot" values.  Or take levels and compute diffs.  Eg. currency exchange rates?

1. Take spatial data, coordinates, and use the Google Maps API to transform it into distance and driving time.  Plot something on a map.  Maybe real-estate data: color code zip codes by home prices (hue) and driving distance from downtown (darkness).

1. Slice something by time *and* by other dimensions, to produce an animated plot.  Perhaps search engine data for "flu" or "bieber tickets" so we can see the phenomenon moving around the country?

1. Process some simple text data. Complaints, or reviews, maybe?  First, ram it through Google Translate.  Then do word counts, sentiment analysis, etc.  Make the data analyzeable.

1. Extract and load some JSON data into a MongoDB database in order to preserve its structure (and perhaps add some).  Use simple queries to show how you can filter by nested details.  Eg. produce an iso-temperature line and plot it on a US map?

1. Generate new structure; for example change of address data showing migration from state to state.  Store it in MongoDB.  Define a function to plot the map for a given "from" state.  (Introduce Python functions.)  Make sample plots.  Challenge user to write a "to" state function.

1. Find some data that ought to be sliced-and-diced.  Find an easy way to make it dimensional and load it into something like a relational database or cube or pivottable.  Show a way to make reports quickly customizeable *without* using SQL.  Pandas???

1. Extract "social network" data.  Maybe from an organizational chart: Congressmen connected to one another by committee membership?  Connections between federal agencies and private sector entities (Goldman Sachs!)?  Create a graph visualization.  Or connect topics on Wikipedia by overlap of authorship.

1. Do something like Jurney's preparation of e-mail data: first extract and structure the data, then create a Flask front-end that lets people navigate it by hyper-text to see who usually emails whom and what the messages included.  Use Hillary's emails, or Climategate.

1. Create a search engine database/index, perhaps using Hadoop + MapReduce.  Show how the index works, under the hood, and talk about the algorithm.

## What I haven't included (yet)

- regular expressions
- web scraping with BeautifulSoup
- munging of audio, images, or video
- ?
