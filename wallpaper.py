import os, sys, random, time, ctypes
from typing import Set
from pathlib import Path

ALLOWED_EXTENSIONS = {".png",".jpeg",".gif",".jpg",".apng",".avif",".bmp",".svg",".webp",".tiff",".ai",".psd",".heif"}

class UsedWallpaper:
    def __init__(self, used_file_path: str):
        self.used_file_path = Path(used_file_path)

    def get_used_wallpapers(self) -> Set[Path]:
        """Reading the cache"""
        if self.used_file_path.exists():
            return {Path(i) for i in self.used_file_path.read_text().splitlines()}
        return set()

    def append_to_used_wallpapers(self, path: str):
        """Appending path to the file"""
        with self.used_file_path.open("a") as file:
            print(path, file=file)

    def clear_used_wallpapers(self):
        """Clearing the used wallpapers"""
        self.used_file_path.open("w").close()


def main(directory_path: Path):
    try:
        minutes = float(input("Set wallpaper change time in minutes: "))
        seconds = minutes * 60
        used_wallpaper = UsedWallpaper(os.path.expanduser(os.path.join("~", ".used_wallpapers.txt")))

        while True:
            wallpapers = get_wallpapers(directory_path)
            used_wallpapers = used_wallpaper.get_used_wallpapers()
            unique_wallpapers = wallpapers - used_wallpapers

            if len(unique_wallpapers) == 0:
                used_wallpaper.clear_used_wallpapers()
                unique_wallpapers = wallpapers
                print("Used wallpaper cleared")

            new_wallpaper = random.choice(list(unique_wallpapers))
            change_wallpaper(str(new_wallpaper))
            used_wallpaper.append_to_used_wallpapers(str(new_wallpaper))

            print(f"Wallpaper changed. Waiting for {minutes} minute(s).")
            time.sleep(seconds)

    except Exception as e:
        print(f"An error occurred: {e}")


def change_wallpaper(file_path: str):
    """Function to change wallpaper on Windows"""
    print(f"Changing wallpaper: {file_path}")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, file_path, 3)


def get_wallpapers(root: Path) -> Set[Path]:
    """Go to directory get all the files names"""
    if root.exists():
        wallpapers = {item for item in root.iterdir() if item.suffix in ALLOWED_EXTENSIONS}
        return wallpapers
    return set()


if __name__ == "__main__":
    """Check if the directory path is provided"""
    if len(sys.argv) < 2:
        print("How to use: python wallpaper.py <path_to_directory>")
        sys.exit(1)

    directory_path = sys.argv[1]
    main(Path(directory_path))