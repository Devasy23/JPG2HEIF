import argparse
import os
from converter import jpg_to_heif_buffer

def convert_file(input_path, output_path):
    with open(input_path, 'rb') as f:
        image_data = f.read()
    output_buffer = jpg_to_heif_buffer(image_data)
    with open(output_path, 'wb') as f:
        f.write(output_buffer.getvalue())

def convert_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.jpeg')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.rsplit('.', 1)[0] + '.heic')
            convert_file(input_path, output_path)

def convert_zip(input_zip, output_zip):
    import zipfile
    with zipfile.ZipFile(input_zip, 'r') as zip_ref:
        zip_ref.extractall('temp_input')
    convert_folder('temp_input', 'temp_output')
    with zipfile.ZipFile(output_zip, 'w') as zip_ref:
        for foldername, subfolders, filenames in os.walk('temp_output'):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                zip_ref.write(file_path, os.path.relpath(file_path, 'temp_output'))
    import shutil
    shutil.rmtree('temp_input')
    shutil.rmtree('temp_output')

def main():
    parser = argparse.ArgumentParser(description="Convert JPG to HEIF/HEIC")
    parser.add_argument('mode', choices=['file', 'folder', 'zip'], help="Conversion mode")
    parser.add_argument('input', help="Input file/folder/zip")
    parser.add_argument('output', help="Output file/folder/zip")
    args = parser.parse_args()

    if args.mode == 'file':
        convert_file(args.input, args.output)
    elif args.mode == 'folder':
        convert_folder(args.input, args.output)
    elif args.mode == 'zip':
        convert_zip(args.input, args.output)

if __name__ == "__main__":
    main()
