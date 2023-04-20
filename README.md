# Weather Radar Animation

This Python script downloads radar images of weather conditions in Perth (Plans to incorporate all capital cities of Australia) and combines them with a set of background images to create an animated GIF. It also plays the GIF in mpv and deletes the GIF after playback.

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
1. Run the script using the following command:
```
python perth.py
```
The script will download radar images from the Bureau of Meteorology website and save them in the downloaded_images folder. It will then combine the radar images with a set of background images and save the combined images as a GIF in the combined_images folder. (Plans to make the directories temporary so that don't save to storage.)

The animated GIF will be played using mpv, a media player that can be installed on most Linux distributions. If you don't want to use mpv or youw ant to use some other way to view to the output, just change this line:
```python
subprocess.run(["mpv", "--loop=inf", gif_output_path])
```

## Notes
The animated GIF duration is set to 300ms per frame, but you can adjust it in the script. 
```python
combined_images[0].save(
    gif_output_path,
    save_all=True,
    append_images=combined_images[1:],
    duration=300, # Edit this variable.
    loop=0,
)
```
## License
This script is licensed under the MIT License. See the LICENSE file for more information.