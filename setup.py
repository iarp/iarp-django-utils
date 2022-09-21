from setuptools import setup, find_packages

setup(
    name='iarp_django_utils',
    version='0.0.9',
    description='A personal collection of common django utilities used in various projects',
    url='https://bitbucket.org/iarp/iarp-django-utils/',
    author='IARP',
    author_email='iarp.opensource@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['example']),
    install_requires=[
        'django',
    ],
    dependency_links=[
        # Make sure to include the `#egg` portion so the `install_requires` recognizes the package
        'git+https://iarp@bitbucket.org/iarp/iarp-python-utils.git#egg=iarp_utils'
    ],
    zip_safe=False
)
