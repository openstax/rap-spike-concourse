from setuptools import find_packages, setup
import os

HERE = os.path.abspath(os.path.dirname(__file__))

requirements = ["requests"]


def read_readme():
    with open(os.path.join(HERE, 'README.md')) as f:
        return f.read()


setup(
    name="content-event-resource",
    version='0.1.0',
    description='Concourse CI resource for Content Event Service',
    long_description=read_readme(),
    url='',
    author='m1yag1',
    license='AGPLv3.0',
    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest'
        ]
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'check = src.check:main',
            'in = src.in_:main',
            'out = src.out:main',
        ]
    }
)

