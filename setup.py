"""Setup script for CodeLens"""

from setuptools import setup, find_packages
from app.config.constants import APP_VERSION, APP_NAME, APP_DESCRIPTION, APP_AUTHOR

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name=APP_NAME.lower(),
    version=APP_VERSION,
    author=APP_AUTHOR,
    author_email="team@codelens.dev",
    description=APP_DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/codelens/codelens",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "codelens=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["assets/themes/*.qss", "assets/icons/*"],
    },
)
