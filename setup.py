import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='Dooders',                           # should match the package folder
    packages=setuptools.find_packages(exclude=['tests']),                     # should match the package folder
    version='0.0.3',                                # important for updates
    license='MIT',                                  # should match your chosen license
    description='Testing installation of Package',
    long_description=long_description,              # loads your README.md
    long_description_content_type="text/markdown",  # README.md is of type 'markdown'
    author='Chris Mangum',
    author_email='csmangum@gmail.com',
    url='https://github.com/csmangum/Dooders', 
    install_requires=['pandas'],                  # list all packages that your package uses
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
    
    download_url="https://github.com/csmangum/Dooders/archive/refs/tags/v0.3.0.tar.gz",
)