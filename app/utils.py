import time
import requests
import pandas as pd

from bs4 import BeautifulSoup
from octokit import Octokit



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

def display_cards(job_cards):
    displays = []
    for card in job_cards.values():
        insights = []
        for insight in card:
            display_insight = ''
            for word in insight.split(' '):
                display_insight += word[0].upper() + word[1:] + ' '
            insights.append(f'{display_insight}\n')
        displays.append(insights)
    return displays