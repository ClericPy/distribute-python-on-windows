from setuptools import setup, find_packages
import sys
import codecs
from distwin import __version__

"""
linux:
rm -rf "dist/*";rm -rf "build/*";python3 setup.py bdist_wheel;twine upload "dist/*;rm -rf "dist/*";rm -rf "build/*""
win32:
rm -rf dist;rm -rf build;python3 setup.py bdist_wheel;twine upload "dist/*";rm -rf dist;rm -rf build;rm -rf ichrome.egg-info
"""
if sys.version_info < (3, 6):
    sys.exit("pypinfo requires Python 3.6+")
py_version = sys.version_info
install_requires = ["shiv"]
with open("README.md", encoding="utf-8") as f:
    README = f.read()

setup(
    name="distwin",
    version=__version__,
    keywords=("distribute apps windows shiv"),
    description="Telling how to distribute python app on win32 platform. Read more: https://github.com/ClericPy/distribute-python-on-windows.",
    license="MIT License",
    install_requires=install_requires,
    long_description=README,
    long_description_content_type="text/markdown",
    py_modules=["distwin"],
    author="ClericPy",
    author_email="clericpy@gmail.com",
    url="https://github.com/ClericPy/distribute-python-on-windows",
    packages=find_packages(),
    platforms="any",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
