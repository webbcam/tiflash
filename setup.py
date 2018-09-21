from setuptools import setup, find_packages
from setuptools.command.install import install
import os

DESC = "Unofficial python module for flashing TI devices."
URL = "https://github.com/webbcam/tiflash"
DOCS_URL = "https://tiflash.readthedocs.io"

AUTHOR = "Cameron Webb"
EMAIL = "webbjcam@gmail.com"

class CustomInstallCommand(install):
    def run(self):
        # Do Custom installation stuff here
        install.run(self)

with open('README.rst') as f:
    long_description = f.read()

# Get version string from tiflash/version.py
_here = os.path.dirname(__file__)
# defines version_string
exec(open(os.path.join(_here, "tiflash", "version.py")).read())

setup(  name='tiflash',
        version=version_string, #@UndefinedVariable
        description=DESC,
        long_description=long_description,
        url=DOCS_URL,
        download_url=URL+'/tarball/'+version_string,
        author=AUTHOR,
        author_email=EMAIL,
        license='MIT',
        install_requires=[
            'pyserial>=3.4;platform_system != "Windows"'
        ],
        packages=find_packages(),
        cmdclass = { 'install' : CustomInstallCommand },
        python_requires=">=2.7.13, <=3.7",
        entry_points = {
            'console_scripts':[
                'tiflash=tiflash.core.__main__:main',
            ],
        },
        include_package_data=True,
        zip_safe=False,
        classifiers = [
            "Development Status :: 4 - Beta",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Topic :: Software Development :: Embedded Systems",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Software Development :: Testing",
            "Intended Audience :: Developers"
        ],
        project_urls = {
            'Documentation': DOCS_URL,
            'Source': URL,
        }

    )
