from setuptools import setup, find_packages

setup(
    name="tatum-sdk",
    version="0.1.0",
    author="Mojtaba Sohrabi",
    author_email="dev.mojtabasohrabi@gmail.com",
    description="A Python SDK for Tatum blockchain API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mojtabasohrabi/Tatum-python-SDK",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=22.0",
            "isort>=5.0",
            "flake8>=3.9",
        ],
    },
)