import io
import re
import os

from pkg_resources import parse_requirements
from setuptools import find_packages, setup

# ease installation during development
vcs = re.compile(r"(git|svn|hg|bzr)\+")
try:
    with open("dockers/requirements.txt") as fp:
        VCS_REQUIREMENTS = [
            str(requirement)
            for requirement in parse_requirements(fp)
            if vcs.search(str(requirement))
        ]
except FileNotFoundError:
    # requires verbose flags
    print("requirements.txt not found.")
    VCS_REQUIREMENTS = []

match = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
    io.open("guacamol_baselines/__init__.py", encoding="utf_8_sig").read(),
)
if match is None:
    raise SystemExit("Version number not found.")
__version__ = match.group(1)

setup(
    name="guacamol_baselines",
    version=__version__,
    author="PaccMann Team",
    description="Baseline model implementations for guacamol benchmark adapted for PaccMann",
    packages=find_packages(),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PaccMann/guacamol_baselines.git",
    extras_require={"vcs": VCS_REQUIREMENTS},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "guacamol",
        "matplotlib",
        "torch",
        "joblib",
        "numpy",
        "tqdm",
        "cython",
        "nltk",
        "flake8",
    ],
)

# some baselines require the guacamol dataset to run
os.system("bash fetch_guacamol_dataset.sh")
