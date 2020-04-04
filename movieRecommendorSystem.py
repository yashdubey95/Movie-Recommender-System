# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 21:40:12 2020

@author: yashd
"""

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import SnowballStemmer

def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        #Check if director exists. If not, return empty string
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''

def create_soup(x):
    return ' '.join(x['Genre']) + ' ' +' '.join(x['Director']) + ' ' + ' '.join(x['Writers']) + ' ' + x['Stars'] + ' ' + ' '.join(x['Plot_Keywords'])


def get_recommendations(title, cosine_sim):
    # Get the index of the movie that matches the title
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:31]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]
    
    qualified = metadata.iloc[movie_indices]
    
    m = metadata['Reviewer_count'].quantile(0.60)
    
    final_recommendations = qualified[(qualified['Reviewer_count'] >= m)]
    
    final_recommendations = final_recommendations.sort_values('Reviewer_count', ascending=False).head(10)
    
    # Return the top 10 most similar movies
    print(final_recommendations[['Movie_name','IMDB_Rating']])



if __name__ == '__main__':
    metadata = pd.read_csv('dataset.csv', low_memory=False)

    dataset = metadata[['Rank','Movie_name','Genre','Director','Writers', 'Stars', 'Plot_Keywords']]
    
    features = ['Genre','Director','Writers', 'Stars', 'Plot_Keywords']
    
    stemmer = SnowballStemmer('english')
    
    dataset['Plot_Keywords'] = dataset['Plot_Keywords'].apply(lambda x: [stemmer.stem(i) for i in x])
    
    for feature in features:
        dataset[feature] = dataset[feature].apply(clean_data)
        
    dataset['Soup'] = dataset.apply(create_soup, axis = 1)
    
    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(dataset['Soup'])
    
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    
#    metadata = metadata.reset_index()
    indices = pd.Series(metadata.index, index=metadata['Movie_name']).drop_duplicates()
    
    get_recommendations('The Dark Knight Rises',cosine_sim)
    