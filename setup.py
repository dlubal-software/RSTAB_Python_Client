from setuptools import find_packages
from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent
readme = (here/"README.md").read_text(encoding="utf-8")

setup(
    name='RSTAB',
    version='1.05.0',
    description='Python Framework for RSTAB9 Web Services',
    long_description=readme,
    long_description_content_type = "text/markdown",
    url="https://github.com/Dlubal-Software/RSTAB_Python_Client",
    author="Dlubal Software",
    author_email="info@dlubal.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10"
    ],
    packages=find_packages(),
    package_dir={"RSTAB":"RSTAB"},
    include_package_data=True,
    install_requires=["requests", "six", "suds-py3", "xmltodict", "pytest", "mock", "setuptools"],
    zip_safe = False
)
