from setuptools import setup, find_packages

setup(
    name="GraphVerse",
    version="0.01",
    packages=find_packages(),
    install_requires=[
        "networkx",
        "numpy",
        "torch",
    ],
    author="Parker Williams",
    author_email="parker.williams@gmail.com",
    description="A package for generating random graphs, performing rule-based random walks, and training a simple LLM",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ParkerWilliams/GraphVerse",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)