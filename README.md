# JPG to HEIF Converter

This project allows you to freely convert JPG images to HEIF format. HEIF (High Efficiency Image Format) is a more efficient image format in terms of storage and quality compared to traditional formats like JPG.

## Why HEIF?

HEIF, as the name suggests, is a high-efficiency image format. Not only does it offer smaller file sizes compared to JPG, but it also provides better image quality. This makes it an excellent choice for anyone looking to save storage space without compromising on image quality.

## Getting Started

To get started with this project, follow the steps below:

1. Clone the repository:
    ```bash
    git clone https://github.com/Devasy23/JPG2HEIF
    ```


2. Create a virtual environment:
    ```bash
    python3 -m venv venv
    ```

3. Activate the virtual environment:
    - On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    - On Unix or MacOS:
        ```bash
        source venv/bin/activate
        ```

5. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To convert a JPG image to HEIF, use the following command:

```bash
streamlit run app.py
```
or using the [link](https://jpgtoheifconverter.streamlit.app/)

### CLI Tools

You can also use the CLI tools to convert files, folders, and zip archives:

- Convert a single file:
    ```bash
    jpg2heif convert <input_image> <output_image>
    ```

- Convert a folder:
    ```bash
    jpg2heif convert_folder <input_folder> <output_folder>
    ```

- Convert a zip archive:
    ```bash
    jpg2heif convert_zip <input_zip> <output_folder>
    ```

## Running Tests

To run the tests, use the following command:

```bash
pytest
```

## Installing from PyPI

You can install the package from PyPI using the following command:

```bash
pip install jpg2heif
```

## Images:
![image](https://github.com/Devasy23/JPG2HEIF/assets/110348311/f1c281bb-a828-4085-ba48-f8cddd6af802)
![image](https://github.com/Devasy23/JPG2HEIF/assets/110348311/9fd50cc0-d519-4bdb-90b3-1f3848498906)
