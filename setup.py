# setup.py
from setuptools import setup, find_packages

setup(
    name="pymueller",
    version="0.1.1",
    description="Tools and functions for 4x4 Mueller matrices",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Chae",
    author_email="a40075@outlook.com",
    packages=find_packages(),  # Finds the muellerphys package
    install_requires=[
        "numpy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)