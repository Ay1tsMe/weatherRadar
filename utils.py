import os
import requests
from PIL import Image

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0"
}

# Download a single image using the given URL and save it to the specified folder
def download_image(url, output_folder):
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    filename = os.path.join(output_folder, os.path.basename(url))
    with open(filename, "wb") as image_file:
        image_file.write(response.content)
        
    return filename

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