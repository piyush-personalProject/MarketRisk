"""Setup configuration for MarketRisk package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="marketrisk",
    version="1.0.0",
    author="Deepali Jain",
    description="A Black-Scholes Options Greeks Calculator that computes option prices and Greeks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/marketrisk",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial",
        "Intended Audience :: Financial and Insurance Industry",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "marketrisk=marketrisk.cli:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/marketrisk/issues",
        "Source": "https://github.com/yourusername/marketrisk",
    },
)

