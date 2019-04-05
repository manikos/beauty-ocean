from setuptools import setup, find_packages


with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "Click>=6.0",
    "python-digitalocean>=1.13",
    "colored>=1.3",
    "yaspin>=0.14",
    "sshpubkeys>=3.1",
    "inquirer>=2.4",
]

# setup_requirements = ["pytest-runner"]

setup(
    # Project information
    name="beauty_ocean",
    version="0.1.4",
    author="Nick Mavrakis",
    author_email="mavrakis.n@gmail.com",
    url="https://github.com/manikos/beauty-ocean",
    license="MIT license",

    # Description
    description="Exploit DigitalOcean API through the console.",
    long_description=f"{readme}\n\n{history}",
    long_description_content_type='text/x-rst',

    # Requirements
    python_requires='>=3.6',
    install_requires=requirements,
    # setup_requires=setup_requirements,
    extras_require={
        'test': [  # install these with: pip install beauty_ocean[test]
            "pytest>=3.8",
            "coverage>=4.5",
            "pytest-cov>=2.6",
            "tox>=3.3",
            "codecov>=2.0",
        ],
    },

    # Packaging
    packages=find_packages(include=["beauty_ocean", "beauty_ocean.*"]),
    include_package_data=True,
    zip_safe=False,

    # Tests
    test_suite="tests",

    # CLI
    entry_points={
        "console_scripts": ["droplet=beauty_ocean.cli:create_droplet_click"]
    },

    # Metadata
    keywords="cli digital-ocean DigitalOcean droplet inquirer",
    project_urls={
        'Documentation': 'https://beauty-ocean.readthedocs.io/en/latest/',
        'Tracker': 'https://github.com/manikos/beauty-ocean/issues/',
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Environment :: Console",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
