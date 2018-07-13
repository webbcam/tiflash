from setuptools import setup, find_packages
from setuptools.command.install import install
from tiflash.version import version_string

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

setup(  name='tiflash',
        version=version_string,
        description=DESC,
        long_description=long_description,
        #long_description_content_type='text/markdown',
        #url=URL,
        url=DOCS_URL,
        download_url=URL+'/tarball/'+version_string,
        author=AUTHOR,
        author_email=EMAIL,
        license='MIT',
        packages=find_packages(),
        cmdclass = { 'install' : CustomInstallCommand },
        python_requires=">=2.7.13, <4",
        entry_points = {
            'console_scripts':[
                'tiflash=tiflash.core.__main__:main',
            ],
        },
        include_package_data=True,
        zip_safe=False)
