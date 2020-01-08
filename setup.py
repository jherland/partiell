from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="partiell",
    version="0.0.1",
    description="Partial function application with '...'",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jherland/partiell",
    author="Johan Herland",
    author_email="johan@herland.net",
    py_modules=["partiell"],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Python Software Foundation License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="functools partial ellipsis functional currying",
    python_requires=">=3.8",
    install_requires=[],
    extras_require={"dev": ["black", "check-manifest", "twine"]},
)
