from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='whist-server',
    version='0.0.1',
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
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords='game server whist',
    packages=find_packages(exclude=('tests*',)),
    python_requires='>=3.9',
    install_requires=[
        'whist-core~=0.0.1'
    ]
)
