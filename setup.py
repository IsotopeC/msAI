
import setuptools

with open("README.md", "r") as readme_file:
    readme_description = readme_file.read()

setuptools.setup(
    name="msAI",
    version="0.1.1.dev1",
    author="Calvin Peters",
    author_email="calvin.isotope@gmail.com",
    description="Tools for creating AI models for mass spectrometry data",
    long_description=readme_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IsotopeC/msAI",
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3",
                 "Operating System :: OS Independent",],
    keywords='AI models mass spectrometry data',
    install_requires=['numpy', 'pandas'],
    python_requires='>3.4'
)

