from setuptools import setup, find_packages

setup(
    name = 'ikeatradfri',
    version = '0.0.1',
    url = 'https://github.com/moroen/ikea-tradfri.git',
    author = 'moroen',
    author_email = 'moroen@gmail.com',
    description = 'Controlling IKEA-Tradfri',
    packages = ['ikeatradfri'],
    include_package_data=True,
    setup_requires = ['cython'],
    install_requires = ['cython', 'pytradfri[async]', 'appdirs', 'aiohttp'],
    scripts = ['tradfri'],
)