from os import scandir, rename
import os
from os.path import splitext, exists, join
import shutil
import sys
import time
import logging
#watchdog is what I use to access the files on the drive and see what changes have been made
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#replace <user> with your own computer user
source_dir = "/Users/<user>/Downloads"
# You are free to set your own paths and destination directories just by changing the variable name and your path
# in my case, I sent files from my downloads on my C drive to my E drive
dest_dir_sfx = r"E:/sfx"
dest_dir_rar = r"E:/rar"
dest_dir_documents = r"E:/documents"
dest_dir_images = r"E:/images"
dest_dir_executables = r"E:/executables"
dest_dir_videos = r"E:/videos"

#this is to create a unique name for a file that is downloaded so there are no duplicates (i.e untitled(1).jpg)
def makeUnique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1
        print(counter)
    return name
# This renames the file and moves it to where you want it to move    
def move(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = makeUnique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    shutil.move(entry, dest)
# This class scans the source directory (in this case my downloads folder) and looks at files that contain certain file types and calls the move function upon a change within the source directory
class MoveHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with os.scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                dest = source_dir
                if name.endswith('.wav') or name.endswith('.mp3'):
                    dest = dest_dir_sfx
                    move(dest, entry, name)
                    logging.info(f"Moved audio file: {name}")
                elif name.endswith('.rar') or name.endswith('.7zip') or name.endswith('.zip') or name.endswith('.7z'):
                    dest = dest_dir_rar
                    move(dest, entry, name)
                    logging.info(f"Moved zip file: {name}")
                elif name.endswith('.txt') or name.endswith('.pdf') or name.endswith('.docx') or name.endswith('.xlsx') or name.endswith('.pptx'):
                    dest = dest_dir_documents
                    move(dest, entry, name)
                    logging.info(f"Moved document file: {name}")
                elif name.endswith('.jpg') or name.endswith('.jpeg') or name.endswith('.png'):
                    dest = dest_dir_images
                    move(dest, entry, name)
                    logging.info(f"Moved image file: {name}")
                elif name.endswith('.exe'):
                    dest = dest_dir_executables
                    move(dest, entry, name)
                    logging.info(f"Moved executable file: {name}")
                elif name.endswith('.mp4') or name.endswith('.webm') or name.endswith('.mov'):
                    dest = dest_dir_videos
                    move(dest, entry, name)
                    logging.info(f"Moved video file: {name}")
    
#initializes the script (observer, move handler, and logging)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    logging.info(f'start watching directory {path!r}')
    event_handler = MoveHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
