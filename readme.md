# README

This project solves the issue of retrieving URLs for trending repositories. Initially, I faced a problem where the URLs were being split with the name `%2f`, leading to incorrect URLs being scraped. These URLs were formatted like `/login?return_to=%2Fmlflow%2Fmlflow`.

After obtaining the correct URLs, I attempted to locate the `pyproject.toml` and `requirements.txt` files within the repositories. However, I found that the way packages were listed in the `pyproject.toml` varied across repositories, which made it difficult to identify a consistent pattern.

To address this, I used OpenAI to assist in identifying the packages and then applied a frequency counter to identify the top 10 most frequently used packages across the repositories.

**Final Output:**

Top 10 most frequently used packages:
- setuptools: 8
- pre-commit: 6
- jinja2: 6
- pytest: 6
- requests: 6
- packaging: 6
- pytest-cov: 5
- pydantic: 5
- pytest-mock: 5
- numpy: 5