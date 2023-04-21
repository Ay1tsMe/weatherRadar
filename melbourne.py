import re
import subprocess
from bs4 import BeautifulSoup
from utils import *

# URLs for the background images
background_image_urls = [
    "http://www.bom.gov.au/products/radar_transparencies/IDR.legend.0.png",
    "http://www.bom.gov.au/products/radar_transparencies/IDR023.background.png",
    "http://www.bom.gov.au/products/radar_transparencies/IDR023.topography.png",
    "http://www.bom.gov.au/products/radar_transparencies/IDR023.locations.png",
    "http://www.bom.gov.au/products/radar_transparencies/IDR023.range.png",
]

# Download the background images and save them to the "background_images" folder
background_image_folder = "background_images"
os.makedirs(background_image_folder, exist_ok=True)

background_image_filenames = [download_image(url, background_image_folder) for url in background_image_urls]

# Combine the background images into a single image
background = combine_images(background_image_filenames)

# Save the combined background image
combined_background_filename = os.path.join(background_image_folder, "combined_background.png")
background.save(combined_background_filename)


# Set the URL of the webpage containing the images
urlImages = "http://www.bom.gov.au/products/IDR023.loop.shtml"

# Set the output folder for downloaded images
output_folder = "downloaded_images"
os.makedirs(output_folder, exist_ok=True)

# Send an HTTP request to get the content of the webpage
responseImages = requests.get(urlImages, headers=headers)
responseImages.raise_for_status()

# Parse the HTML content using BeautifulSoup
soupImages = BeautifulSoup(responseImages.content, "html.parser")

# Find the script containing the image names
script_element = soupImages.find("script", string=re.compile(r"theImageNames\[\d\]"))

# Extract the image names using a regular expression
image_names = re.findall(r'/radar/IDR023\.T\.\d{12}\.png', script_element.string)

# Download the images and save them as individual files
for index, image_name in enumerate(image_names):
    img_src = f"http://www.bom.gov.au{image_name}"
    img_response = requests.get(img_src, headers=headers)
    img_response.raise_for_status()

    # Save the image to the output folder
    img_filename = os.path.join(output_folder, f"image{index + 1}.png")
    with open(img_filename, "wb") as img_file:
        img_file.write(img_response.content)

    print(f"Downloaded image {index + 1}: {img_src}")

# Set the output folder for the combined images
combined_output_folder = "combined_images"
os.makedirs(combined_output_folder, exist_ok=True)

# Load the combined background image
background = Image.open(combined_background_filename)

combined_images = []

# Iterate through the downloaded radar images, overlay them on the background, and save the combined images
for index in range(len(image_names)):
    radar_image_path = os.path.join(output_folder, f"image{index + 1}.png")
    radar_image = Image.open(radar_image_path).convert("RGBA")
    
    # Create a new blank image with the same size as the background
    combined_image = Image.new("RGBA", background.size)
    
    # Paste the background and radar image onto the new image
    combined_image.paste(background, (0, 0))
    combined_image.paste(radar_image, (0, 0), radar_image)
    
    # Convert the combined image to RGB mode and save it
    combined_image = combined_image.convert("RGB")
    combined_image_path = os.path.join(combined_output_folder, f"combined_image{index + 1}.png")
    combined_image.save(combined_image_path)
    
    combined_images.append(combined_image)

# Create a list of durations for each frame
durations = [300] * len(combined_images)
durations[-1] = 1000

# Save the combined images as a GIF
gif_output_path = os.path.join(combined_output_folder, "combined_images.gif")
combined_images[0].save(
    gif_output_path,
    save_all=True,
    append_images=combined_images[1:],
    duration=durations,
    loop=0,
)

print(f"Combined images saved as a GIF: {gif_output_path}")

# Run the GIF in mpv and wait for it to finish
subprocess.run(["mpv", "--loop=inf", gif_output_path])