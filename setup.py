from setuptools import setup, find_packages

setup(
    name='chatbot',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'transformers',
        'torch'
    ],
    entry_points={
        'console_scripts': [
            'chatbot=app:main',
        ],
    },
    python_requires='>=3.6',
    author='Your Name',
    author_email='your.email@example.com',
    description='A simple AI chatbot implemented using Flask and a pre-trained language model from Hugging Face Transformers.',
    license='MIT',
    keywords='chatbot flask transformers huggingface',
    url='https://github.com/aryan1112003/Ai_ChatBot.git',
)
