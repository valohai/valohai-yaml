import setuptools

dev_dependencies = [
    'flake8',
    'isort',
    'pydocstyle',
    'pytest-cov',
]

if __name__ == '__main__':
    setuptools.setup(
        name='valohai-yaml',
        description='Valohai.yaml validation and parsing',
        version='0.2',
        url='https://github.com/valohai/valohai-yaml',
        author='Valohai',
        maintainer='Aarni Koskela',
        maintainer_email='akx@iki.fi',
        license='MIT',
        install_requires=['jsonschema', 'PyYAML', 'six'],
        tests_require=dev_dependencies,
        extras_require={'dev': dev_dependencies},
        packages=setuptools.find_packages('.', exclude=('*tests*',)),
        include_package_data=True,
        entry_points={
            'console_scripts': [
                'valohai-yaml = valohai_yaml.__main__:main',
            ],
        },
    )
