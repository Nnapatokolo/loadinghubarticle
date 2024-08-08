from PIL import Image
import os

def resize_image(input_path, output_dir, size, suffixes):
    os.makedirs(output_dir, exist_ok=True)
    with Image.open(input_path) as img:
        resized_img = img.resize(size, Image.LANCZOS)
        for suffix in suffixes:
            output_path = os.path.join(output_dir, suffix)
            resized_img.save(output_path)
            print(f"Image resized to {size} and saved to {output_path}")

