import io
import re

from pkg_resources import parse_requirements
from setuptools import find_packages, setup

# ease installation during development
vcs = re.compile(r"(git|svn|hg|bzr)\+")
try:
    with open("requirements.txt") as fp:
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
    io.open("__init__.py", encoding="utf_8_sig").read(),
)
if match is None:
    raise SystemExit("Version number not found.")
__version__ = match.group(1)

setup(
    name="guacamol_baselines",
    version=__version__,
    author="Benevolent AI",
    packages=find_packages(),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "guacamol"
        "matplotlib"
        "torch"
        "joblib"
        "numpy"
        "tqdm"
        "cython"
        "nltk"
        "flake8"
    ],
    extras_require={"vcs": VCS_REQUIREMENTS}
)
