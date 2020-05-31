from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name="reverb_hermes",
    version="0.0.1",
    license="GPL",
    packages=find_packages(),
    author="tjreverb",
    author_email="tjreverb@gmail.com",
    long_description=long_description,
    url="https://github.com/TJREVERB/HERMES.git",
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'hermes-simulate=src.main:main'
        ]
    }
)
