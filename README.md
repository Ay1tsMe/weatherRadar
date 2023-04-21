# Weather Radar

This Python script downloads radar images of weather conditions for Australian capital cities and combines them with a set of background images to create an animated GIF. It also plays the GIF in mpv.

**NOTE: I have realised scraping bom.gov.au is prohibited. In the meantime, I am working on changing the code to access their resources from their ftp server.**

## Example Output
![Example](https://0x0.st/H85L.gif)

## Requirements
```bash
Python 3.x
requests library
bs4 library
Pillow library
imageio library
mpv media player (optional)
```
## Installation
1. Clone this repository and open the directory.
```bash
git clone github.com/Ay1tsMe/weatherRadar
cd weatherRadar
```

2. Install the required libraries using pip:
```bash
pip install -r requirements.txt
```
3. (**Optional**: if you want to run the output in mpv.) Install mpv. Refer to [this page](https://mpv.io/installation/) for installation instructions for your operating system.

## Usage
1. Run the script using the following command (replace sydney with city of choice):
```bash
python weatherRadar.py sydney
```
For more information on how to use the script:
```bash
python weatherRadar.py -h
```

The script will download radar images from the Bureau of Meteorology website and save them in the downloaded_images folder. It will then combine the radar images with a set of background images and save the combined images as a GIF in the combined_images folder. **(Plans to make the directories temporary so that don't save to storage.)**

The animated GIF will be played using mpv, a media player that can be installed on most Linux distributions. If you don't want to use mpv or you want to use some other tool to view to the output, just change this line in the `city.py`:
```python
subprocess.run(["mpv", "--loop=inf", gif_output_path])
```

## Notes
The animated GIF duration is set to 300ms per frame, but you can adjust it in the script. 
```python
durations = [300] * len(combined_images) # Adjust this line.
durations[-1] = 1000 # Adjust this line for duration of last frame.
```
## License
This script is licensed under the MIT License. See the LICENSE file for more information.
