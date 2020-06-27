
import setuptools

setuptools.setup(
    name="warpseq",
    version="0.1",
    author="Michael DeHaan",
    author_email="michael@michaeldehaan.net",
    description="text-based MIDI sequencer",
    long_description="text-based MIDI sequencer",
    long_description_content_type="text/plain",
    url="https://classforge.io",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=[
        "classforge>=0.92",
    ]
)
