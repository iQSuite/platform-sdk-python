from setuptools import setup, find_packages

setup(
    name="iqsuite",
    version="0.1.6",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "pydantic>=2.0.0"
    ],
    author="iQ Suite",
    author_email="support@iqsuite.ai",
    description="Python SDK for IQSuite API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/iQSuite/platform-sdk-python",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
)