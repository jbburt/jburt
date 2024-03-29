from setuptools import find_packages
from setuptools import setup

with open("README.md", "r") as f:
    readme = f.read()

install_reqs = [
    "numpy",
    "torch",
    "pandas",
    "openai",
    "scipy",
    "matplotlib",
    "openai",
    "pyarrow",
    "black",
    "tiktoken",
    "langchain",
]

setup(
    name="jburt",
    version="0.3.0",
    author="Josh Burt",
    author_email="joshuaburtphd@gmail.com",
    include_package_data=True,
    description="Personal library.",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=install_reqs,
    python_requires=">=3",
    classifiers=[
        "Programming Language :: Python :: 3.10",
    ],
)
