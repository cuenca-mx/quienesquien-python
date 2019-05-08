import setuptools

requirements = [
    'requests'
]

with open('README.md', 'r') as f:
    long_description = f.read()


setuptools.setup(
    name='quienesquien',
    version='0.0.2',
    author='Cuenca',
    author_email='dev@cuenca.com',
    description='Cliente para listas quienesquien',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cuenca-mx/quienesquien-python',
    packages=setuptools.find_packages(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'vcrpy'],
    extras_require={
        'dev': [
            'pytest>=3',
            'pycodestyle'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
