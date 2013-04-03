from setuptools import setup, find_packages
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name="jondis",
      version="0.1",
      description="Redis pool for HA redis clusters",
      long_description=read('README.md'),
      author="Jon Haddad",
      author_email="jon@grapheffect.com",
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Environment :: Web Environment",
          "Environment :: Plugins",
          "License :: OSI Approved :: BSD License",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Software Development :: Libraries :: Python Modules",
          ],
      keywords="redis",
      install_requires=["redis"],
      url="https://github.com/StartTheShift/jondis",
      packages=find_packages(),
      include_package_data=True
      )
