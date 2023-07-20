import setuptools

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

    install_requires=['fastapi', 'numpy', 'pandas', 'pydantic', 'pytest', 'networkx'],
    
    keywords= [
    "Artificial Intelligence",
    "Simulation",
    "AI Agents",
    "Cognitive Agents",
    "Evolutionary Algorithms",
    "Emergent Behavior",
    "Open-Source",
    "Research Project",
    "Digital Environment",
    "Machine Learning",
    "Agent-Based Model",
    "Reinforcement Learning",
    "AI Environment",
    "Causal Control",
    "Energy Consumption",
    "Autonomous Agents",
    "AI Development",
    "Virtual Reality",
    "Simulated Reality",
    "AI Research",
    "Computational Intelligence",
    "Interactive Simulation",
    "AI Evolution",
    "Complex Systems",
    "Life Simulation"],

    classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Science/Research",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Operating System :: OS Independent"],

    download_url="https://github.com/csmangum/Dooders/archive/refs/tags/v0.3.0.tar.gz"
)
