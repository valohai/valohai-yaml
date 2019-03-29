import ast
import os
import re
import setuptools

with open(os.path.join(os.path.dirname(__file__), 'valohai_yaml', '__init__.py')) as infp:
    version = ast.literal_eval(re.search('__version__ = (.+?)$', infp.read(), re.M).group(1))

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
        version=version,
        url='https://github.com/valohai/valohai-yaml',
        author='Valohai',
        author_email='info@valohai.com',
        maintainer='Aarni Koskela',
        maintainer_email='akx@iki.fi',
        license='MIT',
        install_requires=['jsonschema', 'PyYAML'],
        tests_require=dev_dependencies,
        extras_require={'dev': dev_dependencies},
        packages=setuptools.find_packages('.', exclude=('*tests*',)),
        include_package_data=True,
        entry_points={
            'console_scripts': [
                'valohai-yaml = valohai_yaml.__main__:main',
            ],
        },
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Topic :: Software Development :: Libraries',
        ]
    )
