from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='TextAssitant',
    version='0.1',
    packages=find_packages(),
    install_requires=required,
    entry_points={
        'console_scripts': [
            'chatbot = main:main'
        ]
    },
    author='Pablo Rilo',
    author_email='prilom@hotmail.com',
    description='Un chat bot para interactuar con archivos de texto y PDF en tu PC.',
    
   
)
