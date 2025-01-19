import argparse
import os
from converter import jpg_to_heif_buffer
from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim
import pillow_heif

def convert_file(input_path, output_path, quality=90):
    with open(input_path, 'rb') as f:
        image_data = f.read()
    output_buffer = jpg_to_heif_buffer(image_data, quality=quality)
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

def benchmark_conversion(input_path):
    original_image = Image.open(input_path).convert('RGB')
    original_array = np.array(original_image)

    output_path = 'temp_output.heic'
    convert_file(input_path, output_path)

    heif_file = pillow_heif.read_heif(output_path)
    converted_image = Image.frombytes(
        heif_file.mode, 
        heif_file.size, 
        heif_file.data, 
        "raw", 
        heif_file.mode, 
        heif_file.stride
    )
    converted_array = np.array(converted_image)

    os.remove(output_path)

    ssim_index = ssim(original_array, converted_array, multichannel=True, win_size=3)
    print(f"SSIM index: {ssim_index:.4f}")

def compare_ssim(original_path, converted_paths):
    original_image = Image.open(original_path).convert('RGB')
    original_array = np.array(original_image)

    for converted_path in converted_paths:
        converted_image = Image.open(converted_path).convert('RGB')
        converted_array = np.array(converted_image)

        ssim_index = ssim(original_array, converted_array, multichannel=True, win_size=3)
        print(f"SSIM index for {converted_path}: {ssim_index:.4f}")

def main():
    parser = argparse.ArgumentParser(description="Convert JPG to HEIF/HEIC")
    parser.add_argument('mode', choices=['file', 'folder', 'zip'], help="Conversion mode")
    parser.add_argument('input', help="Input file/folder/zip")
    parser.add_argument('output', help="Output file/folder/zip")
    parser.add_argument('--benchmark', action='store_true', help="Benchmark the conversion algorithm")
    parser.add_argument('--compare', nargs='+', help="Compare SSIM index of other converted images with the original")
    parser.add_argument('--quality', type=int, default=90, help="Quality of the HEIF conversion (1-100)")
    args = parser.parse_args()

    if args.benchmark:
        benchmark_conversion(args.input)
    elif args.compare:
        compare_ssim(args.input, args.compare)
    else:
        if args.mode == 'file':
            convert_file(args.input, args.output, quality=args.quality)
        elif args.mode == 'folder':
            convert_folder(args.input, args.output)
        elif args.mode == 'zip':
            convert_zip(args.input, args.output)

if __name__ == "__main__":
    main()
