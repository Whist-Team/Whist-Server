from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements/requirements.txt') as f:
    requirements = f.readlines()

setup(
    name='whist-server',
    version='0.1.1',
    author='Whist Team',
    description='Whist game server.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Whist-Team/Whist-Server',
    project_urls={
        'Bug Tracker': 'https://github.com/Whist-Team/Whist-Server/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords='game server whist',
    packages=find_packages(exclude=('tests*',)),
    namespace_pacakge=['whist'],
    entry_points={'console_scripts': ['whist-server=whist.server.cli:main']},
    python_requires='>=3.9',
    install_requires=requirements,
    extras_require={
        "testing": [
            "pytest==7.1.1",
            "pytest-cov==3.0.0",
            "pytest-asyncio==0.18.2"
        ]
    },
)
