from setuptools import find_packages, setup


setup(
    name='teachertools',
    version='0.0.1',
    author='Academis',
    url='https://github.com/lenarother/academis-teachertools-api',
    packages=find_packages('src', exclude=['tests']),
    package_dir={'': 'src'},
    include_package_data=True,
    tests_require=[],
    install_requires=[],
    dependency_links=[],
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
)
