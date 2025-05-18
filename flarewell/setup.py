from setuptools import setup, find_packages

setup(
    name="flarewell",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        "click",
        "beautifulsoup4",
        "html2markdown",
        "pyyaml",
        "markdown",
        "requests",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "black",
            "isort",
            "flake8",
            "mypy",
        ],
    },
    entry_points={
        "console_scripts": [
            "flarewell=flarewell.cli:main",
        ],
    },
    python_requires=">=3.8",
    description="Convert MadCap Flare projects to Docusaurus-compatible Markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/flarewell",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Documentation",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
) 