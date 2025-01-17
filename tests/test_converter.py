import pytest
from converter import jpg_to_heif_buffer
from PIL import Image
from io import BytesIO
import pillow_heif

# Register HEIF format with PIL
pillow_heif.register_heif_opener()

def test_jpg_to_heif_buffer():
    # Create a simple image for testing
    image = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()

    # Convert the image
    output_buffer = jpg_to_heif_buffer(img_byte_arr)

    # Check if the output is not empty
    assert output_buffer.getbuffer().nbytes > 0

    # Check if the output format is HEIF
    output_image = Image.open(output_buffer)
    assert output_image.format == 'HEIF'
