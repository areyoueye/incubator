from setuptools import setup

setup(
    name='incubator',
    packages=['incubator'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_restful',
        'flask_sqlalchemy',
    ],
)

