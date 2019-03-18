import os
import setuptools


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

_ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(_ROOT, 'README.md')) as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name="lswriteups",
    version="1.0",
    description="Easily Grabs writeups from CTFTime.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license='MIT',
    author="Mehtab Zafar",
    url="https://github.com/mzfr/lswriteups",
    install_requires=requirements,
    setup_requires=['setuptools>=38.6.0'],
    scripts=[
        'lswriteups/lswriteup'
    ],
    keywords='writeups',
)

