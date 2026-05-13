from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="promptforge",
    version="1.0.0",
    author="PromptForge Team",
    author_email="promptforge@example.com",
    description="Lightweight Terminal AI Prompt Manager & Optimizer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/promptforge/promptforge",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities",
        "Environment :: Console",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "promptforge=promptforge.cli:main",
        ],
    },
    package_data={
        "promptforge": [],
    },
    include_package_data=True,
    zip_safe=False,
)
