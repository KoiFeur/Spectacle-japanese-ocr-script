
# import time module, Observer, FileSystemEventHandler
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import PIL.Image
from manga_ocr import MangaOcr
 
class OnMyWatch:
    # Set the directory on watch
    watchDirectory = "/tmp/"
 
    def __init__(self):
        self.observer = Observer()
 
    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive = True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")
 
        self.observer.join()
 
 
class Handler(FileSystemEventHandler):
 
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
 
        elif event.event_type == 'created':
            # Event is created, you can process it now
            #print("Watchdog received created event - % s." % event.src_path)
            pass
        elif event.event_type == 'modified':
            # Event is modified, you can process it now
            #print("Watchdog received modified event - % s." % event.src_path)
            if "Spectacle" in event.src_path and not ("lockfile" in event.src_path):
                with open("jpn.txt", "r+") as f:
                    try:
                        data = f.read()
                        img = PIL.Image.open(event.src_path)
                        mocr = MangaOcr()
                        text = mocr(img)
                        if text not in data:
                            data = data + text + "\n"
                            f.write(text + "\n")
                        print(data)
                    except:
                        print("not an image")


if __name__ == '__main__':
    watch = OnMyWatch()
    watch.run()

