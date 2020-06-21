# Movie-Recommender-System

This repository contains the python implementation of a Content Based Movie Recommender System.

A recommender system at its core uses a statistical algorithm to predict or filter entities based on user's preferences or preferences between users that previously used that entity. The two main approaches for achieving this task are:-
  1. Content-based Filtering.
  2. Collaborative-Filtering

## Content-Based Filtering:
 
Content-based filtering uses a series of discrete attributes in an entity to gather information about that entity. This information along with the users preferences are used to calculate a matrix that calculates the similarity between two entities (like the cosine-similarity matrix) and returns predictions for the content that the user might be interested in.
In this case of content-based movie recommendation system we use the following attributes: keywords extracted from the movie plot, the genre, the director, the cast and the writers to create a cosine similarity matrix to predict the top 10 movies similar to a movie preferred by the user and using a popularity filter to predict top 10 movies similar to the input sorted by their reviews.

## Collaborative-Filtering:

Collaborative-filtering is based on historical data consisting of the user's past preferences and thus it does not need a lot of information about the entity. It is built upon the assumption that a group of users who had the same set of opinion on one thing in the past will likely have the same set of opinion for another in the future.
The user's preference is divided into two categories:-
  1. Explicit Rating: This rating most directly suggest how much a user liked a particular entity. For example, giving 4.5 stars out of 5 for a movie like "The Dark Knight Rises".
  2. Implicit Rating: This rating indirectly infers a lot of user's preferences like a page visit or if a user watched a movie entirely he/she might be interested in it.
This filtering approach suffers from a cold-start problem where a user might not be recommended a new entity if no one in its cluster has not reviewed on it, even though the user would have liked it.
 
 ## Files description:
 * imdb250WebScraping.py:
    python file resonsible to fetch the data from IMDB's Top 250 Movies webpage and creating the required dataset for the task.
    
 * movieRecommendorSystem.py:
    The main python file responsible for predicting the top-K movies based on the user's input. 
 
 * dataset.csv:
    CSV file containg the dataset created as an output from the imdb250WebScraping.py file
    
 ## Prerequisites:
 
Programming languages and libraries used:
  1. Python ==> 3.7.6
  2. nltk ==> 3.4.5
  3. bs4 ==> 4.8.2
  4. sklearn ==> 0.22.1
  
## Usage:
1. Run the imdb250WebScraping.py file to create the dataset:
   ```bash
   python imdb250WebScraping.py
   ```

2. Run the main movieRecommendorSystem.py to get the recommendations:
    ```bash
    python movieRecommendorSystem.py
    ```

## Output:
 ![alt text](https://github.com/yashdubey95/Movie-Recommender-System/blob/master/Output.PNG)
    
