import re
import subprocess
import shutil
from ftplib import FTP
from utils import *

# Set up folder locations
folders = {
    "background_images": "background_images",
    "downloaded_images": "downloaded_images",
    "combined_images": "combined_images"
}

for folder in folders.values():
    os.makedirs(folder, exist_ok=True)

# Set the FTP server URL and connect to it
ftp_server_url = "ftp.bom.gov.au"
ftp_directory = "/anon/gen/radar/"
ftp_transparencies_directory = "/anon/gen/radar_transparencies"

# Connect to the FTP server and change the directory
ftp = FTP(ftp_server_url)
ftp.login()
print("Connected to ftp.bom.gov.au")

# Download radar images
ftp.cwd(ftp_directory)

# List the files in the directory and filter only the .png files
file_list = []
ftp.retrlines("LIST", file_list.append)

# Use a regular expression to filter the desired files
desired_files_pattern = r"IDR633\.T\.\d{12}\.png"
png_files = [f.split()[-1] for f in file_list if f.endswith(".png") and re.match(desired_files_pattern, f.split()[-1])]

# Download the images and save them as individual files
for index, png_file in enumerate(png_files):
    img_data = bytearray()
    ftp.retrbinary(f"RETR {png_file}", img_data.extend)

    # Save the image to the output folder
    img_filename = os.path.join(folders["downloaded_images"], f"image{index + 1}.png")
    with open(img_filename, "wb") as img_file:
        img_file.write(img_data)

    print(f"Downloaded image {index + 1}: {png_file}")

# Download transparency images
ftp.cwd(ftp_transparencies_directory)

# List the files and filter only the .png files
file_list = []
ftp.retrlines("LIST", file_list.append)

# Specify the files you want to download
desired_background_files = [
    "IDR633.background.png",
    "IDR633.topography.png",
    "IDR633.locations.png",
    "IDR633.range.png",
]

# Filter the file list to only include the desired files
transparency_files = [f.split()[-1] for f in file_list if f.endswith(".png") and f.split()[-1] in desired_background_files]

# Download the transparency images and save them as individual files
for transparency_file in transparency_files:
    img_data = bytearray()
    ftp.retrbinary(f"RETR {transparency_file}", img_data.extend)

    # Save the image to the output folder
    img_filename = os.path.join(folders["background_images"], transparency_file)
    with open(img_filename, "wb") as img_file:
        img_file.write(img_data)

    print(f"Downloaded transparency image: {transparency_file}")

ftp.quit()

# Combine and save background images
background_image_filenames = [os.path.join(folders["background_images"], f) for f in desired_background_files]
background_image = combine_images(background_image_filenames)
background_image_filename = os.path.join(folders["combined_images"], "combined_background.png")
background_image.save(background_image_filename)

# Create a GIF with transparent images placed on top of the background image
transparent_image_filenames = [os.path.join(folders["downloaded_images"], f) for f in os.listdir(folders["downloaded_images"]) if f.endswith(".png")]
transparent_image_filenames.sort(key=sort_key)

sequence_images = create_gif_sequence_images(transparent_image_filenames, background_image)
durations = [250] * (len(sequence_images) - 1) + [1000]

# Save the GIF in the combined_images folder
gif_filename = os.path.join("output.gif")
sequence_images[0].save(gif_filename, save_all=True, append_images=sequence_images[1:], duration=durations, loop=0)

print(f"Combined background image saved as: {background_image_filename}")
print(f"Combined GIF saved as: {gif_filename}")

#Delete folders
for folder in folders.values():
    shutil.rmtree(folder)

# Run the GIF in mpv and wait for it to finish
subprocess.run(["mpv", "--loop=inf", gif_filename])