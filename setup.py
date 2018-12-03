import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="python-keypath-extractor",
    version="0.0.1",
    author="Jeffrey Morgan",
    description="Extract Python dictionary values with keypaths.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Data-Innovation-Research-Institute/python-keypath-extractor.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
