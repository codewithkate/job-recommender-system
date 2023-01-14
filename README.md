# Overview
Kate Crawford | GA Capstone | January 2023

This is an unsupervised learning process with a recommendation system and deployed application that I developed for General Assembly's Data Science Capstone. You can view the slides I used during the live presentation in the presentation-slides.pdf.

To run the app, you will need to create your a token and use the username from the same account. It is recommended that all notebooks be ran in order from 01 to 04 in order to reproduce my results and test out additional data. You can retrieve the data and vector spaces used in this project through [Google Drive](https://drive.google.com/drive/folders/175Ao-k5lTlRp8Jr07gHohmMC0nghITZ5?usp=sharing).

## Repository Structure
```
project-3
|__ app
|   |__app.py
|   |__engine.py
|   |__utils.py
|__ assets
|   |__tvec.pkl
|   |__X_tvec.pkl
|__ data
|   |__postings
|   |  |__postings_indeed.csv
|   |  |__postings_jobspiker.csv
|   |  |__postings_mendeley.csv
|   |__test-README.text
|__ notebooks
|   |__01_Wrangling.ipynb
|   |__02_NLP.ipynb
|   |__03_Mining.ipynb
|   |__04_Recommender.ipynb
|__ presentation-slides.pdf
|__ README.md
```

# Executive Summary:
## Goal
  The goal of this project was to see if a model could distinguish between different technical areas based on project content. This engine measures these results by returning job recommendations. As someone actively engaged in the technical interviewing process, I observed the wide variety of job descriptions that overlap with job titles that create a wide range of possibilities. As a best practice, job seekers tailor their resume language and highlight different projects for each application. This is not only time exhaustive, but also a difficult task to maintain at a high quality when trying to 'cast a net' over an ever-evolving job market. This project intends to explore an approach to helping job seekers, like myself.
## Data Collection
  This recommendation system was to be constructed using publicly available data from a variety of job search sources, like Indeed and Dice. In the effort to retrieve job postings for this project, I was exposed to the legal implications of web scraping and the restrictions around accessing data collected from users. Some of the most recent court decisions surrounding this privacy issue were spearheaded by companies that provide services for human relations and operate job recommendation systems on scales much larger than this personal project. 
   Working within these constraints, I looked to job market research projects and data science communities, like data.world and Kaggle to collect data. Some datasets still contained HTML tags from scraping and others only included a small set of features used in another employment study. The first challenge was to find related features to narrow down my source list. Concatenating the job title to the job description allowed me to focus my efforts towards natural language process as the basis of this recommender engine. However, I also kept other useful information for the a job seeking user, like location. You may also find soem values containing company names and job board sites nearly 10k out of the over 47k rows.
## Metrics
  In an effort to let the data guide my process, I explored ideas to find target values that could be used in Supervised Learning models. Although job title was one of the common values across all datasets, there were thousands of unique combinations for a single position. This was due to the level being included in the title and the word order. I looked further into the job descriptions, but I found that the structure of the descriptions were only shared if they came from the same source. 
  Working under time constraints, I chose to move forward using Unsupervised Learning methods. For exploratory data analysis, I used several cluster models from Sci-kit Learn:
  - KMeans to find optimal cluster sized with the elbow method and silhouette plots,
  - DBSCAN with tuned epsilon values and silhouette coefficients using euclidian and cosine distances,
  - and, Latent Dirichlet Allocation with component tuning and plots of the top terms in each subsequent topic.
## Findings
   The final recommender engine was fueled using pairwise with cosine distances. The output were two datasets. The first was a collection of 10 job postings. Job descriptions were then taken from this dataset and tokenized to create a frequency distribution that allowed for the most similar terms between the train and test data to be returned. The test data I used were README files from the portfolio projects I produced in General Assembly's Data Science Immersive Program.
  The recommender requires two text-based vector spaces to calculate distances. The text data used in the 04_Recommender.ipynb notebook was another NLP project where the topic was legal versus relationship advice. The recommendations that this project's engine produced were mostly legal counsel positions, minus a technical recruiter role and a business intelligence analyst in a legal department. The model was not given any data to distinguish the fact that I do not hold a Juris Doctorate to qualify for legal counsel positions it produced, but it did a great job of aligning my portfolio topic to these job description contents. 
  Using the application I built for this project, I tested a corpus containing all the portfolio projects scraped from my GitHub repositories using the Beautiful Soup, Octokit, and Requests libraries and a unique access token. With more information, the system was able to infer that my projects were related to data science and recommended positions related to data science. The parts of speech that were output provided insight into why the system came to this conclusion. Some adjectives the systems used to describe the closeness of the test to the train were 'analytical, statistical, and mathematic.' However, there were words, like internal and strong, that I could make better sense of if I were to rework the model to take context into account. 
## Conclusion and Recommendations
  Overall, the model achieved the goal of outputting job recommendations based on the content of a portfolio. Outputing location data provided more insights into where these jobs could be found. As a job seeker open to remote work, this is an important feature to be able to expand my search to jobs closely related to particular skill or interest as expressed through projects and into markets that may not have been considered in more traditional in-person contexts. However, too little data may result in the model only producing job results related to project topics. Further testing using more project data, like notebooks or progress reports, would be interesting to evaluate. The hope would be that the model would start to produce more niche positions and/or language related to skills and software. As previously mentioned, I would also explore more models that are used in recommender systems, like SVD.  
