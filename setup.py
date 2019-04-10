import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()


setuptools.setup(
    name='clabe',
    version='0.2.1',
    author='Cuenca',
    author_email='dev@cuenca.com',
    description='Cliente para listas quienesquien',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cuenca-mx/quienesquien-python',
    packages=setuptools.find_packages(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    extras_require={
        'dev': [
            'pytest>=3',
            'pycodestyle',
            'coverage'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)