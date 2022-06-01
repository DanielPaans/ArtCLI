from setuptools import setup

setup(
    name="artcli",
    version="2022.6.1",
    description="",
    author="Daniel Paans",
    author_email="Daniel@danielpaans.nl",
    url="",
    py_modules=['artcli'],
    entry_points={
        'console_scripts': [
            'artcli = artcli:main'
        ]
    },
)

