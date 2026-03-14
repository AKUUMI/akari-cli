from setuptools import setup, find_packages

setup(
    name="akari-cli",
    version="1.4.0",
    description="Tu cliente de anime en español 🕊️",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "click>=8.1.0",
        "rich>=13.0.0",
        "lxml>=4.9.0",
    ],
    entry_points={
        "console_scripts": [
            "akari=akari.main:cli",
        ],
    },
    python_requires=">=3.8",
)
