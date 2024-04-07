import os, sys, random, time, ctypes
from typing import Set
from pathlib import Path

USED_FILE_PATH = Path(os.path.expanduser(os.path.join("~",".used_wallpapers.txt")))
ALLOWED_EXTENSIONS = {".png",".jpeg",".gif",".jpg",".apng",".avif",".bmp",".svg",".webp",".tiff",".ai",".psd",".heif"}

def change_wallpaper(file_path:str):
    """Function to change wallpaper on Windows"""
    print(f"Changing wallpaper: {file_path}")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, file_path, 3)

def get_wallpapers(root:Path) -> Set[Path]:
    """Go to directory get all the files names"""
    if root.exists():
        wallpapers = {item for item in root.iterdir() if item.suffix in ALLOWED_EXTENSIONS}
        return wallpapers
    return set()

def get_used_wallpapers() -> Set[Path]:
    """Reading the cache"""
    if USED_FILE_PATH.exists():
        return {Path(i) for i in USED_FILE_PATH.read_text().splitlines()}
    return set()

def get_directory(directory_path):
    """Get the directory from the command-line"""
    if not os.path.isdir(directory_path):
        print("Invalid directory path.")
        return set()

    file_names = set(os.listdir(directory_path))
    return file_names

def append_to_used_wallpapers(path:str):
    """Appending path to the file"""
    with USED_FILE_PATH.open("a") as file:
        print(path, file=file)

def clear_used_wallpapers():
    USED_FILE_PATH.open("w").close()

def main(directory_path:Path):
    minutes = float(input("Set wallpaper change time in minutes: "))
    seconds = minutes * 60

    while True:
        wallpapers = get_wallpapers(directory_path)
        used_wallpapers = get_used_wallpapers()
        unique_wallpapers = wallpapers - used_wallpapers

        if len(unique_wallpapers) == 0:
            clear_used_wallpapers()
            unique_wallpapers = wallpapers
            print("Used wallpaper cleared")

        new_wallpaper = random.choice(list(unique_wallpapers))
        change_wallpaper(str(new_wallpaper))
        append_to_used_wallpapers(str(new_wallpaper))

        print(f"Wallpaper changed. Waiting for {minutes} minute(s).")
        time.sleep(seconds)

if __name__ == "__main__":
    '''Check if the directory path is provided'''
    if len(sys.argv) < 2:
        print("How to use: python wallpaper.py <path_to_directory>")
        sys.exit(1)

    directory_path = sys.argv[1]
    main(Path(directory_path))