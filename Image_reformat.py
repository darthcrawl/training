from PIL import Image, ImageOps
import os
from collections import Counter

# Directories
input_dir = "images"
output_dir = "images_adjusted"

os.makedirs(output_dir, exist_ok=True)

# Helper function to get the dominant border color
def get_dominant_color(img, side):
    if side == "left":
        pixels = img.crop((0, 0, 1, img.height)).getdata()
    elif side == "right":
        pixels = img.crop((img.width - 1, 0, img.width, img.height)).getdata()
    elif side == "top":
        pixels = img.crop((0, 0, img.width, 1)).getdata()
    elif side == "bottom":
        pixels = img.crop((0, img.height - 1, img.width, img.height)).getdata()
    most_common = Counter(pixels).most_common(1)
    return most_common[0][0] if most_common else 255

# Process files
files = sorted(os.listdir(input_dir), key=lambda x: int(os.path.splitext(x)[0]))
for file in files:
    input_path = os.path.join(input_dir, file)
    output_path = os.path.join(output_dir, file)

    # Open the image
    img = Image.open(input_path).convert("RGB")  # Ensure all images are in RGB mode
    
    # Resize to 1200 on the longest side while keeping aspect ratio
    width, height = img.size
    if width > height:
        new_width = 1200
        new_height = int(height * (1200 / width))
    else:
        new_height = 1200
        new_width = int(width * (1200 / height))
    
    img = img.resize((new_width, new_height), Image.LANCZOS)
    
    # Default canvas color (white fallback)
    canvas_color = (255, 255, 255)  # White as fallback

    # Determine padding for the shorter dimension
    pad_left = pad_top = pad_right = pad_bottom = 0
    if new_width < 1200:
        padding = (1200 - new_width)
        pad_left = padding // 2
        pad_right = padding - pad_left
        canvas_color = get_dominant_color(img, "left")
    elif new_height < 1200:
        padding = (1200 - new_height)
        pad_top = padding // 2
        pad_bottom = padding - pad_top
        canvas_color = get_dominant_color(img, "top")

    # Add padding to make the image square
    img = ImageOps.expand(
        img,
        border=(pad_left, pad_top, pad_right, pad_bottom),
        fill=canvas_color,
    )
    
    # Save the resized and padded image
    img.save(output_path)

print("Processing complete! Resized and padded images are saved in:", output_dir)
