from setuptools import setup, find_packages

setup(
    name="akari-cli",
    version="1.6.0",
    description="Tu cliente de anime en español kawaii (｡•̀ᴗ-)✧",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.3",
        "click>=8.1.7",
        "rich>=13.7.0",
        "lxml>=5.1.0",
        "yt-dlp",
    ],
    entry_points={
        "console_scripts": [
            "akari=akari.main:cli",
        ],
    },
    python_requires=">=3.10",
)
