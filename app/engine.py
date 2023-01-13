# Import Libraries
import pandas as pd
import numpy as np
import spacy
import cleantext

# Preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk import word_tokenize
import cleantext

# Similarities & Distances
from sklearn.metrics import pairwise
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

# Visualizations
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "plotly_mimetype"


def recommend_posts(train_vectors, user_vectors, df):
    # Find cosine distances between input and training data
    dists = pairwise.cosine_distances(train_vectors, user_vectors)

    # Organize distances between train and corpus in dataframe
    dists_df = pd.DataFrame(dists, index=df.index)

    # Create dataframe for top job matches
    # Limit to 10 jobs for faster processing
    results_df = pd.DataFrame(dists_df[0].sort_values()[1:11])

    # Merge results with job postings on shared indices for job title and description
    output_df = results_df.merge(df, left_index=True, right_index=True)
    return output_df


def recommend_words(output_df):  
    # Plot top 20 most similar words
    fdist = dict(FreqDist(word.lower() for word in word_tokenize(output_df['pos_docs'].sum())))
    common_words = pd.DataFrame(fdist.values(), columns=['Frequency'], index=fdist.keys())
    
    # Get Parts of Speech tags for most similar words 
    tokens = [word_tokenize(word) for word in fdist.keys()]
    common_words['pos_tags'] = [nltk.pos_tag(token, tagset = "universal")[0][1] for idx, token in enumerate(tokens)]
    
    return common_words

def create_cards(recommendations):
    rec_columns = ['job_title', 'city', 'state']
    output = {}
    
    for index in range(len(recommendations)):
        insights = []
        # Return information about recommended job
        for column in rec_columns:
            # if there is no information go to the next columns
            if pd.isnull(recommendations[column].iloc[index]) == True:
                continue
            # else add information to the list
            else:
                insights.append(recommendations[column].iloc[index])
                
        # Generate Link to LinkedIn        
        base_url = "https://www.linkedin.com/jobs/search/?"
        keywords = f"keywords={recommendations['job_title'][index].replace(' ','%20')}"
        # If there is a city and state given
        if pd.isnull(recommendations['city'][index]) == False and pd.isnull(recommendations['state'][index]) == False:
            location = f"location={recommendations['city'][index].replace(' ', '%20')}"
            insights.append(base_url + keywords + '&' + location)
        else: 
            insights.append(base_url + keywords)
            
        output[index] = insights
        
    return output
    
def plot_pos(common_words):    
    pos_tags = {'Adjectives':'ADJ', 'Nouns':'NOUN', 'Verbs':'VERB'}
    tag_plots = {}
    for name, tag in pos_tags.items():
        plot = common_words.loc[common_words['pos_tags'] == tag].sort_values('Frequency', ascending=False)[:10]
        fig = px.bar(plot, x='Frequency', y=plot.index, title=f"Relevant {name}")
        tag_plots[name] = fig
    return tag_plots