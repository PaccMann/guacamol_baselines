import io
import re
import os
import sys
import subprocess
import shutil
from pkg_resources import parse_requirements
from setuptools import find_packages, setup
from setuptools import setup, find_packages, Command
from setuptools.command.bdist_egg import bdist_egg as _bdist_egg
from setuptools.command.develop import develop as _develop
from distutils.command.build import build as _build
from multiprocessing import cpu_count

SETUP_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSES = cpu_count()
PROCESSES = str(PROCESSES - 1) if (PROCESSES > 1) else '1'

class fetch_guacamol_datasets(Command):
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
            build_directory = os.path.join(SETUP_DIR, 'data')
            os.makedirs(build_directory, exist_ok=True)
            subprocess.check_call(
                [
                    os.path.join(SETUP_DIR, 'fetch_guacamol_dataset.sh'),
                    SETUP_DIR, build_directory, sys.executable, PROCESSES
                ]
            )
            package_directory = os.path.join(SETUP_DIR, 'guacamol_baselines', 'data')
            built_files = [
                os.path.join(build_directory, entry)
                for entry in os.listdir(build_directory)
            ]
            for module_file in built_files:
                shutil.copy(
                    module_file,
                    package_directory
                )
            try:
                if self.develop:
                    pass
                else:
                    raise AttributeError
            except AttributeError:
                print('Cleaning up')
                shutil.rmtree(build_directory, ignore_errors=True)
        except subprocess.CalledProcessError as error:
            raise EnvironmentError(
                f"Failed to fetch of guacamol datasets dependencies via {error.cmd}."
            )


class build(_build):
    """Build command."""

    sub_commands = [("fetch_guacamol_datasets", None)] + _build.sub_commands


class bdist_egg(_bdist_egg):
    """Build bdist_egg."""

    def run(self):
        """Run build bdist_egg."""
        self.run_command("fetch_guacamol_datasets")
        _bdist_egg.run(self)


class develop(_develop):
    """Build develop."""

    def run(self):
        """Run build develop."""
        setup_cosifer = self.distribution.get_command_obj("fetch_guacamol_datasets")
        setup_cosifer.develop = True
        self.run_command("fetch_guacamol_datasets")
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
        "fetch_guacamol_datasets": fetch_guacamol_datasets,
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
