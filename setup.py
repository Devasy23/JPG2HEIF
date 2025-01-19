from setuptools import setup, find_packages

# Read the version from the VERSION file
with open('VERSION') as version_file:
    version = version_file.read().strip()

setup(
    name='jpg2heif',
    version=version,
    packages=find_packages(),
    install_requires=[
        'Pillow',
        'pillow-heif',
        'streamlit'
    ],
    entry_points={
        'console_scripts': [
            'jpg2heif=converter:main',
        ],
    },
    author='Devasy Patel',
    author_email='patel.devasy.23@gmail.com',
    description='A package to convert JPG images to HEIF format',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Devasy23/JPG2HEIF',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
