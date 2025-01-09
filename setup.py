from setuptools import setup, find_packages

setup(
    name="bible",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        'requests>=2.31.0',
        'python-dotenv>=1.0.0',
        'google-generativeai>=0.3.0',
        'transformers>=4.36.0',
        'torch>=2.1.0',
        'huggingface-hub>=0.19.0'
    ]
)