import requests
import base64
from collections import Counter
import openai
import ast
from openai import OpenAI
from parser import get_all_repos

# Your GitHub and OpenAI API keys
GITHUB_TOKEN = "github-token"
OPENAI_API_KEY = "open-ai-key"

# Authentication headers for GitHub API
headers = {
    "User-Agent": "Mozilla/5.0",
    "Authorization": f"token {GITHUB_TOKEN}",
}

# Function to process multiple repository URLs
def process_repositories(repo_urls):
    package_counter = Counter()

    for url in repo_urls:
        print(f"Processing repository: {url}")
        base_url = f"{url}/contents/"
        dependency_texts = find_dependency_files(base_url)
        unique_packages = set()

        for text in dependency_texts:
            packages = extract_packages_with_openai(text)
            unique_packages.update(packages)
        package_counter.update(unique_packages)

    # Get the 10 most common packages
    top_packages = package_counter.most_common(10)
    print("\nTop 10 most frequently used packages:")
    for package, count in top_packages:
        print(f"{package}: {count}")

# Function to find dependency files and extract their content
def find_dependency_files(base_url):
    dependency_texts = []
    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        contents = response.json()

        for item in contents:
            if item["type"] == "file" and item["name"] in ("requirements.txt", "pyproject.toml"):
                print(f"Dependency file found: {item['path']}")
                content = get_file_content(item["url"])
                if content:
                    dependency_texts.append(content)
    else:
        print(f"Failed to retrieve contents from {base_url}. Status code: {response.status_code}")

    return dependency_texts

# Function to fetch and decode the content of a file
def get_file_content(file_url):
    response = requests.get(file_url, headers=headers)

    if response.status_code == 200:
        content = response.json()
        file_content = content["content"]
        return base64.b64decode(file_content).decode("utf-8")
    else:
        print(f"Failed to retrieve file content from {file_url}. Status code: {response.status_code}")
        return None

# Function to extract packages using OpenAI's API
def extract_packages_with_openai(file_content):
    # OpenAI GPT request to extract package names
    prompt = f"""
Extract the package names (ignoring versions) from the following text:
{file_content}

Provide the list of package names in Python list format. Your response must pass ast.literal_eval().It should not include anything else than python list not even a single word not even ```python.
"""
    api_key = OPENAI_API_KEY
    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
           )
        package_list_string = response.choices[0].message.content.strip()
        print(package_list_string)
        package_list = ast.literal_eval(package_list_string)

        print(f"Extracted packages: {package_list}")
        return [pkg.strip() for pkg in package_list if pkg.strip()]
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return []

# Example usage


repo_urls = get_all_repos()
process_repositories(repo_urls)
