from setuptools import setup, find_packages

setup(
    name="circuit_simulator",
    version="0.1.0",
    author="Cameron Bains",
    author_email="cmbains12@gmail.com",
    description="draw and simulate electrical circuits",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cmbains12/circuit_simulator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "PyQt5",
        "numpy",
        "requests",
        "setuptools",
        "pandas"
    ],
    entry_points={
        'console_scripts': [
            'your_command=your_module:main_function',
        ],
    },
)