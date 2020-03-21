import setuptools

with open("README", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="physualize", # Replace with your own username
    scripts=['bin/physualize'],
    version="0.0.2",
    author="Raman Khurana",
    author_email="ramankhurana1986@gmail.com",
    description="a small package to visualise the distributions which are common in HEP (and in general) distribution.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ExoPie/physualize",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
