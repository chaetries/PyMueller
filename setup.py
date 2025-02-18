from setuptools import setup, find_packages

setup(
    name="pymueller",  # The name of your package
    version="0.1.2",   # Your current version
    description="Tools and functions for 4x4 Mueller matrices",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Chae",
    author_email="a40075@outlook.com",
    packages=find_packages(),  # Automatically finds all packages in the directory
    install_requires=[
        "numpy",  # Ensure you list dependencies here
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
