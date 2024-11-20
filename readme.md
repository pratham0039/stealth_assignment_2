# README

I have solved the problem of retrieving the URLs of trending repositories. Initially, I encountered an issue where the URLs were being split with the name `%2f`, which caused incorrect URLs to be scraped. The URLs were formatted more like `/login?return_to=%2Fmlflow%2Fmlflow`.

Once I retrieved the correct link, I attempted to locate the `pyproject.toml` and `requirements.txt` files within the repositories. However, I found that the way packages were added to `pyproject.toml` differed across repositories, making it difficult to identify a consistent pattern.

To overcome this, I utilized OpenAI to help identify the packages, then applied a frequency counter to return the top 10 most common packages used across the repositories.

The final output:
Top 10 most frequently used packages:
setuptools: 8
pre-commit: 6
jinja2: 6
pytest: 6
requests: 6
packaging: 6
pytest-cov: 5
pydantic: 5
pytest-mock: 5
numpy: 5