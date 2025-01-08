from setuptools import setup, find_packages

setup(
    name="scripture-ai-agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'openai',
        'python-dotenv',
        'requests',
        'beautifulsoup4',
    ]
)