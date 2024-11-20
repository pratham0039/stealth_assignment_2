import requests
from bs4 import BeautifulSoup

# URL to scrape (example: GitHub user profile or repositories)
url = 'https://github.com/trending/python?since=daily'  # Replace with the actual URL

# Your GitHub Personal Access Token (replace 'YOUR_TOKEN' with the actual token)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
      # Add your personal access token here
}

def get_all_repos():

    # Send a GET request to the URL with the headers for authentication
    response = requests.get(url, headers=headers)
    all_repos = []

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <article> tags with class "Box-row"
        articles = soup.find_all('article', class_='Box-row')

        # Loop through each article and find the first <a> tag, then extract the href
        for article in articles:
            a_tag = article.find('a')
            if a_tag and a_tag.get('href'):  # Ensure the <a> tag exists and has an href
                link = a_tag['href']
                try:
                
                    link1, link2 = link.split('%2F')[1], link.split('%2F')[2]
                except:
                    continue
                print(f'https://api.github.com/repos{"/"+link1 + "/" + link2}') 
                repo_link = f'https://api.github.com/repos{"/"+link1 + "/" + link2}' # Output the link (make sure it's a full URL)
                all_repos.append(repo_link)
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
    
    return all_repos
    


list_of_repo = get_all_repos()
print(list_of_repo)