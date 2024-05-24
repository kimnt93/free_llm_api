from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='free_llm_api',
    version='0.1',
    packages=find_packages(),
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        free_llm_api=free_llm_api.cli:cli
    ''',
)
