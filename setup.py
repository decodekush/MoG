from setuptools import setup, find_packages

setup(
    name="emq",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.7.0",
        "crewai>=0.28.8",
        "crewai-tools>=0.1.6",
        "langchain-google-genai>=1.0.0",
        "playwright>=1.40.0",
        "beautifulsoup4>=4.12.2",
        "google-api-python-client>=2.100.0",
        "google-auth-httplib2>=0.1.1",
        "google-auth-oauthlib>=1.1.0",
        "python-dotenv>=1.0.0",
        "textual>=0.47.1"
    ],
    entry_points={
        "console_scripts": [
            "emq=src.cli:app",
        ],
    },
)
