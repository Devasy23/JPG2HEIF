import os
import zipfile
import pytest
from app import jpg_to_heif, convert_folder_to_heif, convert_zip_to_heif

def test_single_file_conversion():
    input_image = "tests/test_images/test.jpg"
    output_image = "tests/test_images/test.heic"
    heif_file = jpg_to_heif(input_image)
    heif_file.save(output_image, format="HEIF")
    assert os.path.exists(output_image)
    os.remove(output_image)

def test_folder_conversion():
    input_folder = "tests/test_images"
    output_folder = "tests/output_images"
    convert_folder_to_heif(input_folder, output_folder)
    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            output_path = os.path.join(output_folder, filename.rsplit(".", 1)[0] + ".heic")
            assert os.path.exists(output_path)
            os.remove(output_path)
    os.rmdir(output_folder)

def test_zip_conversion():
    input_zip = "tests/test_images.zip"
    output_folder = "tests/output_images"
    with zipfile.ZipFile(input_zip, 'w') as zipf:
        for root, _, files in os.walk("tests/test_images"):
            for file in files:
                zipf.write(os.path.join(root, file), file)
    convert_zip_to_heif(input_zip, output_folder)
    for filename in os.listdir("tests/test_images"):
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            output_path = os.path.join(output_folder, filename.rsplit(".", 1)[0] + ".heic")
            assert os.path.exists(output_path)
            os.remove(output_path)
    os.rmdir(output_folder)
    os.remove(input_zip)
