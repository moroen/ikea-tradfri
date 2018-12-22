from setuptools import setup, find_packages

setup(
    name = 'ikea-tradfri',
    version = '0.0.1',
    url = 'https://github.com/moroen/ikea-tradfri.git',
    author = 'moroen',
    author_email = 'moroen@gmail.com',
    description = 'Controlling IKEA-Tradfri',
    packages = find_packages(),
    setup_requires = ['cython'],
    install_requires = ['cython', 'pytradfri[async]', 'appdirs'],
    scripts = ['tradfri.py'],
)