from setuptools import setup, find_packages
from pathlib import Path

def read_requirements(filename: str):
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        return []

setup(
    name="bible",
    version="0.1.0",
    description="An autonomous Bible study and research agent with LLM integration",
    author="Scripture AI Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=read_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'bible=src.main:main',
        ],
    }
)