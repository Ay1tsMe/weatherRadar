import os
import requests
from PIL import Image

# Function to combine multiple images with different dimensions
def combine_images(image_filenames):
    max_size = (0, 0)
    for filename in image_filenames:
        with Image.open(filename) as img:
            size = img.size
            max_size = (max(max_size[0], size[0]), max(max_size[1], size[1]))

    # Create a new blank image with the maximum size
    combined_image = Image.new("RGBA", max_size)

    # Paste each image onto the blank image
    for filename in image_filenames:
        with Image.open(filename).convert("RGBA") as img:
            combined_image.paste(img, (0, 0), img)

    return combined_image

# Custom sorting function to sort filenames based on the numeric part
def sort_key(filename):
    numeric_part = int(''.join(filter(str.isdigit, filename)))
    return numeric_part

def create_gif_sequence_images(transparent_image_filenames, background_image):
    sequence_images = []

    for filename in transparent_image_filenames:
        with Image.open(filename).convert("RGBA") as img:
            combined_frame = Image.new("RGBA", background_image.size)
            combined_frame.paste(background_image, (0, 0))
            combined_frame.paste(img, (0, 0), img)
            sequence_images.append(combined_frame)

    return sequence_images