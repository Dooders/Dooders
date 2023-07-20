import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='Dooders',                          
    packages=setuptools.find_packages(exclude=['tests']),
    version='0.0.3',                                
    license='MIT',                                 
    description="""Dooders is an open-source research project focused on the 
    development of artificial intelligent agents in a simulated reality.""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Chris Mangum',
    author_email='csmangum@gmail.com',
    url='https://github.com/csmangum/Dooders',
    # list all packages that your package uses
    install_requires=['pandas'],
    # keywords=["pypi", "mikes_toolbox", "tutorial"], #descriptive meta-data
    classifiers=[                                   # https://pypi.org/classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    download_url="https://github.com/csmangum/Dooders/archive/refs/tags/v0.3.0.tar.gz"
)
