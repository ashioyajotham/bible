from setuptools import setup, find_packages
import os

# Read the contents of README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="biblia",
    version="0.3.5",
    description="Bible Study Assistant for Christian Education and Research",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Victor Jotham Ashioya",
    author_email="victorashioya960@gmail.com",
    url="https://github.com/ashioyajotham/bible",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "requests>=2.30.0",
        "python-dotenv>=1.0.0",
        "google-generativeai>=0.3.0",
        "colorama>=0.4.6",
        "transformers>=4.30.0",
        "torch>=2.0.0",
        "accelerate>=0.20.0",
        "rich>=12.0.0",
    ],
    entry_points={
        'console_scripts': [
            'bible=main:main',  # Command to run the application
        ],
    },
    package_data={
        "": ["*.json", "*.yml", "*.md"],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Religion",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Religion",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    keywords="bible, ai, research, spirituality, education, assistant",
)
