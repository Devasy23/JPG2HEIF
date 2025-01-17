from setuptools import setup, find_packages

setup(
    name="jpg2heif",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "Pillow",
        "pillow_heif",
        "click",
    ],
    entry_points={
        "console_scripts": [
            "jpg2heif=app:cli",
        ],
    },
    author="Devasy23",
    author_email="devasy23@example.com",
    description="A tool to convert JPG images to HEIF format",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Devasy23/JPG2HEIF",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
