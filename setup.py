
"""msAI build script for setuptools.

"""


import setuptools


with open("README.rst", "r") as readme_file:
    readme_description = readme_file.read()

setuptools.setup(
    name="msAI",
    version="1.3.1.dev0",
    author="Calvin Peters",
    author_email="calvin.isotope@gmail.com",
    description="Tools to create AI models for mass spectrometry data",
    long_description=readme_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/IsotopeC/msAI",
    packages=setuptools.find_packages(exclude=['docs', 'tests', 'logs']),
    classifiers=["Programming Language :: Python :: 3",
                 "Operating System :: OS Independent",
                 "Topic :: Scientific/Engineering :: Artificial Intelligence",
                 "Topic :: Scientific/Engineering :: Bio-Informatics",
                 "Topic :: Scientific/Engineering :: Chemistry",
                 "Topic :: Scientific/Engineering :: Mathematics",
                 "Topic :: Scientific/Engineering :: Visualization"],
    keywords='AI models mass spectrometry MS data mzML spectrum ion chromatogram TIC '
             'extracted-ion EIC XIC machine learning artificial intelligence deep neural network',
    install_requires=['numpy', 'pandas', 'tensorflow', 'pymzml'],
    python_requires='>3.6'
)
