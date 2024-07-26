from setuptools import setup, find_packages

setup(
    name="karaca",
    version="0.1.0",
    description="Turkish Natural Language Processing (NLP) Library",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="KaracaAI",
    author_email="karacaai@protonmail.com",
    url="https://github.com/KaracaAI/KaracaNLP",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'tensorflow',
        'transformers',
        'nltk'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    license='Apache 2.0',
    python_requires='>=3.6',
)
