from setuptools import setup, find_packages

setup(
    name="bible",
    version="0.1.0",
    description="An autonomous Bible study and research agent with LLM integration",
    author="Scripture AI Team",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        'openai',
        'python-dotenv',
        'requests',
        'fastapi',
        'uvicorn',
        'pandas',
        'numpy',
        'tensorflow',
        'torch',
        'transformers',
        'beautifulsoup4'
    ],
    entry_points={
        'console_scripts': [
            'bible=bible.main:main',
        ],
    }
)