from setuptools import setup


with open("README.md") as f:
    long_description = f.read()


setup(
    name="lopc",
    version="1.0.0",
    description="Counts lines of Python code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Markku Leiniö",
    url="https://github.com/markkuleinio/lopc",
    python_requires=">=3.7",
    packages=["lopc"],
    entry_points={"console_scripts": ["lopc=lopc.lopc:main"]},
    license="MIT",
)
