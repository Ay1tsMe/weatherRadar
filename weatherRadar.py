import argparse
import os
import importlib
from utils import *

def main(cities):
    file_dir = os.path.dirname(os.path.abspath(__file__))

    for city in cities:
        module_name = city.lower()
        filename = os.path.join(file_dir, module_name + ".py")
        

        if os.path.isfile(filename):
            importlib.import_module(module_name)
        else:
            print(f"No file found for {city}. Make sure {module_name}.py exists in the same directory as weatherRadar.py")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Creates a .gif of a weather radar for an Australian city.")
    parser.add_argument("cities", nargs='*', help="The name of the city for which to execute the Python file.", choices=["perth", "sydney", "melbourne", "brisbane", "adelaide", "darwin", "hobart", "canberra"], type=str.lower)
    args = parser.parse_args()

    main(args.cities)