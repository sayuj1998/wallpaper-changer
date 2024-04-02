# find the wallpaper file
# os.walk the files in that folder
# randomize it using random module
# make it an hour by default
# have optional cmd line argument that will ask how often this script should run (minutes)
# use subprocess to use schtasks which should run this script depending on user input on cmd line
# file called README.md that explains what this script is and how to use it

import os, sys, random, time, ctypes

USED_FILE_PATH = os.path.join("~", "used_wallpapers.txt")

# Function to change wallpaper on Windows
def change_wallpaper(file_path):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, file_path, 3)

# Function to read used wallpapers from file
def parse_used_files():
    used_wallpapers = set()
    if os.path.exists(USED_FILE_PATH):
        with open(USED_FILE_PATH) as file:
            for line in file:
                used_wallpapers.add(line.strip())
    return used_wallpapers

# Function to get the directory from the command-line
def get_directory(directory_path):
    if not os.path.isdir(directory_path):
        print("Invalid directory path.")
        return set()

    file_names = set(os.listdir(directory_path))
    return file_names

def main(directory_path):
    minutes = int(input("Set wallpaper change time in minutes: "))
    seconds = minutes * 60

    while True:
        random_wallpaper = random.choice(os.listdir(directory_path))
        change_wallpaper(os.path.join(directory_path, random_wallpaper))

        print("Wallpaper changed. Waiting for", minutes, "minute(s).")
        time.sleep(seconds)

    # Check if the directory path is provided
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("How to use: python wallpaper.py <path_to_directory>")
        sys.exit(1)

    main(sys.argv[1])
