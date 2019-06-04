
import setuptools

with open("README.md", "r") as readme_file:
    readme_description = readme_file.read()

setuptools.setup(
    name="msAI",
    version="0.1.1.dev2",
    author="Calvin Peters",
    author_email="calvin.isotope@gmail.com",
    description="Tools for creating AI models for mass spectrometry data",
    long_description=readme_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IsotopeC/msAI",
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3",
                 "Operating System :: OS Independent",
                 "Topic :: Scientific/Engineering :: Artificial Intelligence",
                 "Topic :: Scientific/Engineering :: Bio-Informatics",
                 "Topic :: Scientific/Engineering :: Chemistry",
                 "Topic :: Scientific/Engineering :: Mathematics",
                 "Topic :: Scientific/Engineering :: Visualization"],
    keywords='AI models mass spectrometry MS data mzML spectrum ion chromatogram TIC '
             'extracted-ion EIC XIC machine learning artificial intelligence deep neural network',
    install_requires=['numpy', 'pandas', 'matplotlib', 'tensorflow', 'bokeh', 'pymzml'],
    python_requires='>3.4'
)

