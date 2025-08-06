#!/usr/bin/env python3
"""
Setup script for Agentic GraphRAG A2A System
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="agentic-graphrag-a2a",
    version="0.1.0",
    author="Ultimate KG Project",
    description="A comprehensive multi-agent system integrating Google ADK agents with Cognee GraphRAG via A2A Protocol",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-asyncio>=0.24.0",
            "black>=24.0.0",
            "ruff>=0.6.0",
            "mypy>=1.11.0",
        ],
        "all": [
            "pytest>=8.0.0",
            "pytest-asyncio>=0.24.0", 
            "black>=24.0.0",
            "ruff>=0.6.0",
            "mypy>=1.11.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "agentic-graphrag=main:main",
        ],
    },
)