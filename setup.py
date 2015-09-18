from setuptools import setup


setup(
    name='pyinapp',
    version='0.1.1',
    packages=['pyinapp'],
    install_requires=['rsa', 'requests'],
    description="InApp purchase validation API wrappers",
    keywords='inapp store purchase googleplay appstore market',
    author='Ivan Mukhin',
    author_email='muhin.ivan@gmail.com',
    url='https://github.com/keeprocking/pyinapp',
    long_description=open('README.rst').read(),
    license='MIT'
)
