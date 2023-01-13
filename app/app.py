import pandas as pd
import streamlit as st
import pickle
import time

from utils import get_readme, display_cards
from engine import recommend_posts, recommend_words, create_cards, plot_pos

import plotly.express as px

# Read in the Data
# Dataframe with Job Postings Data
postings = pd.read_csv('./data/postings/postings.csv', index_col='id')
# Fitted Tf-IDF Vectorizer
with open('./assets/tvec.pkl', 'rb') as p_in:
    tvec = pickle.load(p_in)
# Vectorized Training data
with open('./assets/X_tvec.pkl', 'rb') as p_in:
    train_vectors = pickle.load(p_in)

# Sidebar for inputs and descriptions
with st.sidebar:
    """
    # Job Recommendation App
    ___
    This Recommender Engine generates job recomendations 
    and language to use if you apply to these positions.
    To begin, connect to GitHub:
    """
    start_engine = 0
    # Retrieve GitHub README.md files
    username = st.text_input(label="Enter GitHub Username: ", value='codewithkate')
    if st.button('Get Projects'):
        with st.spinner("Collecting your projects' README.md files..."):
            projects = get_readme(username, TOKEN)
            if projects != None:
                st.success('README.md files retrieved!')
            else:
                st.error('No project files found.', icon="🚨")
# Display Recommendations           
"""
## Your Best Matches
"""
my_bar = st.progress(0)
for percent_complete in range(100):
    # Vectorize Project Data
    user_vectors = tvec.transform(list(projects))

    # Generate output dataframe with recommendations
    recommendations = recommend_posts(train_vectors, user_vectors, df=postings)

    # Generate most frequently similar language by parts of speech
    common_words = recommend_words(output_df=recommendations)
    my_bar.progress(percent_complete + 1)


# Generate Recommendations
# Organize information to display about each recommend job
job_cards = create_cards(recommendations)
displays = display_cards(job_cards)
    
tab0, tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9,  = st.tabs(["1","2", "3", "4", "5", "6", "7", "8", "9", "10"])
# Display Job Recomendations as tabs
with tab0: 
    for insight in displays[0]:
        st.write(insight)
with tab1: 
    for insight in displays[1]:
        st.write(insight)
with tab2: 
    for insight in displays[2]:
        st.write(insight)
with tab3: 
    for insight in displays[3]:
        st.write(insight)
with tab4: 
    for insight in displays[4]:
        st.write(insight)
with tab5: 
    for insight in displays[5]:
        st.write(insight)
with tab6: 
    for insight in displays[6]:
        st.write(insight)
with tab7: 
    for insight in displays[7]:
        st.write(insight)
with tab8: 
    for insight in displays[8]:
        st.write(insight)
with tab9: 
    for insight in displays[9]:
        st.write(insight)

"""
## Language Recommendations for Applications
"""
# Create plots for parts of speech analysis
figures = plot_pos(common_words)
pos_tags = ['Adjectives', 'Nouns', 'Verbs']
for tag in pos_tags:
    st.plotly_chart(figures[tag])