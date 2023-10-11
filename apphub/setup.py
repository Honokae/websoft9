from setuptools import find_packages, setup

setup(
    name='apphub',
    version='0.2',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'apphub=cli.apphub_cli:cli',
        ],
    },
)
