from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in swissmedhealth/__init__.py
from swissmedhealth import __version__ as version

setup(
	name="swissmedhealth",
	version=version,
	description="Customizations for app.swissmedhealth.com",
	author="KAINOTOMO PH LTD",
	author_email="info@kainotomo.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
