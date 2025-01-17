from PIL import Image
import pillow_heif
from io import BytesIO

def jpg_to_heif_buffer(image_data):
    image = Image.open(BytesIO(image_data))
    output_buffer = BytesIO()
    heif = pillow_heif.from_pillow(image)
    heif.save(output_buffer, format="HEIF")
    return output_buffer
