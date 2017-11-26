
from setuptools import setup, find_packages

setup(
    name='cadetapi',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-restful',
        'flask-marshmallow',
        'marshmallow-sqlalchemy'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
