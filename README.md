# Weather Radar

This Python script downloads radar images of weather conditions for Australian capital cities and combines them with a set of background images to create an animated GIF. It also plays the GIF in imv.

## Example Output
![Example](https://0x0.st/H85L.gif)

## Requirements
```bash
Python 3.x
requests library
Pillow library
imv (if you don't have imv, change last line in each `city.py` file with the program of choice)
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

## Usage
1. Run the script using the following command (replace sydney with city of choice):
```bash
python weatherRadar.py sydney
```
For more information on how to use the script:
```bash
python weatherRadar.py -h
```

The script will download radar images from the Bureau of Meteorology FTP server and save them in the downloaded_images folder. It will then combine the radar images with a set of background images and save the combined images as `output.gif` (Folders are temporary and are removed after program has executed)

The animated GIF will be played using imv, an image viewer that can be installed on most Linux distributions. If you don't want to use imv or you want to use some other tool to view to the output, just change this line in the `city.py`:
```python
subprocess.run(["imv", gif_filename])
```

## Notes
The animated GIF duration is set to 300ms per frame, but you can adjust it in the script. 
```python
durations = [250] * (len(sequence_images) - 1) + [1000]

durations = [250] # Change this value for the frame duration
[1000] # Change this value for the last frame duration
```
## License
This script is licensed under the MIT License. See the LICENSE file for more information.
