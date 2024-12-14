import os

import setuptools

PROJECT_NAME = "LLM based recommendation"
PROJECT_DESCRIPTION = " https://github.com/ChahidAbderrazak/LLM-medical-treatment"
PROJECT_URL = "https://github.com/ChahidAbderrazak/LLM-medical-treatment"
VERSION = "1.0.0"
AUTHOR_USER_NAME = "Abderrazak Chahid"
AUTHOR_EMAIL = "abderrazak.chahid@gmail.com"


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setuptools.setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description=(PROJECT_DESCRIPTION),
    long_description=read("README.md"),
    license="MIT",
    url=PROJECT_URL,
    extras_require={
        "test": ["pytest"],
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)


# classifiers:
# Development Status:: 1 - Planning
# Development Status:: 2 - Pre-Alpha
# Development Status:: 3 - Alpha
# Development Status:: 4 - Beta
# Development Status:: 5 - Production/Stable
# Development Status:: 6 - Mature
# Development Status:: 7 - Inactive
