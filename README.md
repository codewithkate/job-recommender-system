# Overview
Kate Crawford | GA Capstone | January 2023

This is an unsupervised learning process with a recommendation system and deployed application that I developed for General Assembly's Data Science Capstone. Feel free to [view the slides](presentation-slides.pdf) I used during the live presentation.

![App Preview](job-app.png)

## Code Snippet
One of the main features of this app is taking in user data to return best matches. The following code snippet gets up to six README files from the user's GitHub account. There is a GUI feature in the app that retrieves a username and access token as arguments for this function. I found a way to use GitHub's API with Python, Python's requests library, and HMTL code found from the target site to retrieve text data that was transformed into a vector space with the proper shape for pairwise distancing.

```python
def get_readme(username, TOKEN):
    n_repos = 0
    readmes = []
    
    repos = Octokit().repos.list_for_user(username=username)
    for repo in repos.json:
        project = repo["name"]

        token = TOKEN
        headers = {'Authorization': 'token ' + token}

        # url to request
        url = f"https://github.com/codewithkate/{project}"

        # make the request and return the json
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        # scrape raw text data from readme file on main branch
        readme = soup.find("div", {"class":"Box md js-code-block-container js-code-nav-container js-tagsearch-file Box--responsive"}).text.replace('\n', '')
        readmes.append(readme)
        
        # Increment repo counter until max 6 repos
        n_repos += 1
        if n_repos <= 6:
            break
            
        time.sleep(2)
        
    return ''.join(readmes)
```

To run the app, you will need to download the `app` folder, create a GitHub access token and use the username from the same account, and run `$python app.py` in the terminal. However, it is recommended that you test this out in using the notebook found in the project's [Google Drive](https://drive.google.com/drive/folders/175Ao-k5lTlRp8Jr07gHohmMC0nghITZ5?usp=sharing).

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
|   |__[01_Wrangling.ipynb][nb-01]
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
  This recommendation system was to be constructed using publicly available data from a variety of job search sources, like Indeed and Dice. In the effort to retrieve job postings for this project, I was exposed to the legal implications of web scraping and the restrictions around accessing data collected from users. Some of the [most recent](https://www.jdsupra.com/legalnews/linkedin-v-hiq-landmark-data-scraping-6423889/) court decisions surrounding this privacy issue were spearheaded by companies that provide services for human relations and operate job recommendation systems on scales much larger than this personal project. 
   Working within these constraints, I looked to job market research projects and data science communities, like [data.world](https://data.world/) and [Kaggle](https://www.kaggle.com/) to collect data. Some datasets still contained HTML tags from scraping and others only included a small set of features used in another employment study. The first challenge was to find related features to narrow down my source list. Concatenating the job title to the job description allowed me to focus my efforts towards natural language process as the basis of this recommender engine. However, I also kept other useful information for the a job seeking user, like location. You may also find soem values containing company names and job board sites nearly 10k out of the over 47k rows.
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
  Overall, the model achieved the goal of outputting job recommendations based on the content of a portfolio. Outputing location data provided more insights into where these jobs could be found. As a job seeker open to remote work, this is an important feature to be able to expand my search to jobs closely related to particular skill or interest as expressed through projects and into markets that may not have been considered in more traditional in-person contexts. However, too little data may result in the model only producing job results related to project topics. Further testing using more project data, like notebooks or progress reports, would be interesting to evaluate. The hope would be that the model would start to produce more niche positions and/or language related to skills and software. As previously mentioned, I would also explore more models and distance measurements that are used in recommender systems.  

<!--- LINKS & MATERIALS --->
<!--- NOTEBOOKS --->
[nb-01]: https://github.com/codewithkate/6-job-recommender/blob/main/notebooks/01_Wrangling.ipynb
