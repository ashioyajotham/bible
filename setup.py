from setuptools import setup, find_packages

setup(
    name="bible",
    version="0.1.0",
    description="Bible Study AI Agent",
    package_dir={"": "src"},  # tell setuptools packages are under src/
    packages=find_packages(where="src"),  # look for packages under src/
    install_requires=[
        "requests",
        "python-dotenv",
        "google-generativeai",
        "colorama",
        "transformers",
        "torch",
        "accelerate"
    ],
    entry_points={
        'console_scripts': [
            'bible=main:main',  # simplified entry point since src is in path
        ],
    },
    package_data={
        "": ["*.json", "*.yml"],
    },
    include_package_data=True
)
