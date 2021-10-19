import io
import re
import os
import subprocess
from pkg_resources import parse_requirements
from setuptools import find_packages, setup
from setuptools import setup, find_packages, Command
from setuptools.command.bdist_egg import bdist_egg as _bdist_egg
from setuptools.command.develop import develop as _develop
from distutils.command.build import build as _build

SETUP_DIR = os.path.dirname(os.path.abspath(__file__))


class setup_cosifer(Command):
    """
    Run installation to fetch guacamol datasets.
    """


    def initialize_options(self):
        """Set initialize options."""
        pass

    def finalize_options(self):
        """Set finalize options."""
        pass

    def run(self):
        """Run installation to fetch guacamol datasets."""
        try:
            subprocess.check_call(
                [os.path.join(SETUP_DIR, "fetch_guacamol_dataset.sh")]
            )
        except subprocess.CalledProcessError as error:
            raise EnvironmentError(
                f"Failed to fetch of guacamol datasets dependencies via {error.cmd}."
            )


class build(_build):
    """Build command."""

    sub_commands = [("setup_cosifer", None)] + _build.sub_commands


class bdist_egg(_bdist_egg):
    """Build bdist_egg."""

    def run(self):
        """Run build bdist_egg."""
        self.run_command("setup_cosifer")
        _bdist_egg.run(self)


class develop(_develop):
    """Build develop."""

    def run(self):
        """Run build develop."""
        setup_cosifer = self.distribution.get_command_obj("setup_cosifer")
        setup_cosifer.develop = True
        self.run_command("setup_cosifer")
        _develop.run(self)


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
    cmdclass={
        "bdist_egg": bdist_egg,
        "build": build,
        "setup_cosifer": setup_cosifer,
        "develop": develop,
    },
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
