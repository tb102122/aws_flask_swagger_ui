# Copyright 2022 Tobias Bruckert
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from setuptools import setup
from codecs import open
from os import path
import re

here = path.abspath(path.dirname(__file__))

# Read the version number from a source file.
# Why read it, and not import?
# see https://groups.google.com/d/topic/pypa-dev/0PkjVpcxTzQ/discussion


def find_version():
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    try:
        f = open(path.join(here, "aws_flask_swagger_ui/__init__.py"), "r", "latin1")
        version_file = f.read()
        f.close()
    except:
        raise RuntimeError("Unable to find version string.")

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# Get the long description from the README file
with open(path.join(here, "aws_flask_swagger_ui/README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="aws-flask-swagger-ui",
    version=find_version(),
    description="Swagger UI blueprint for Flask on AWS Lambda",
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False,
    # url="https://github.com/tb102122/",
    keywords="flask aws amazon lambda swagger",
    author="Tobias Bruckert",
    license="Apache License, Version 2.0",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
    ],
    packages=["aws_flask_swagger_ui"],
    install_requires=["Flask"],
    package_data={
        "aws_flask_swagger_ui": [
            "LICENSE",
            "README.md",
            "templates/*.html",
            "dist/VERSION",
            "dist/LICENSE",
            "dist/README.md",
            "dist/*.html",
            "dist/*.js",
            "dist/*.css",
            "dist/*.png",
            "dist/*.map",
        ]
    },
)
