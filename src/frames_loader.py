from video_loader import MultipleVideoLoader
from is_wire.core import Logger

import threading
import queue
import time


class FramesLoader:
    def __init__(self, video_list, fps=10.0):
        """Given a list a video, uses MultipleVideoLoader object to loaded all videos and
        sample at spefic fps on a diferent thread.
        Args:
            video_list (dict): contais the path of all four video where the key identifies
            the ID of the camera.
            fps (float): frequency of sample of the video.
        """
        self.log = Logger("VideoLoaderThread")

        if len(video_list) == 0:
            self.log.warn("You are trying to initialize with a empty list of videos")

        self.video_loader = MultipleVideoLoader(video_list)
        self.num_samples = self.video_loader.n_frames()
        self.count_sample = 0
        self.fps = fps
        info = {
            "total_samples": self.num_samples
        }
        self.log.info('{}', str(info).replace("'", '"'))
        self.run = True
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self._reader, daemon=True)
        self.thread.start()

    def _reader(self):
        """Sample the videos and store on a Queue object.
        This is the target of the thread.
        """
        while self.run:
            t_o = time.time()
            _ = self.video_loader.load_next()
            frames = self.video_loader[0]
            if frames is not None:
                self.count_sample += 1
                if not self.queue.empty():
                    try:
                        self.queue.get_nowait()
                    except queue.Empty:
                        pass
                self.queue.put([self.count_sample, frames])
                self.video_loader.release_memory()
            if self.count_sample == self.num_samples:
                self.run = False
                break
            t_f = time.time()
            took_s = t_f - t_o
            dt = (1 / self.fps) - took_s
            if dt > 0:
                time.sleep(dt)

    def read(self):
        """Returns what it is stored at the Queue.
        That is a list, where the first position is the frame_id and
        the second position is a dictionary containing frames from all cameras at same time
        """
        return self.queue.get()

    def release(self):
        """Finish the thread
        """
        self.run = False
        with self.queue.mutex:
            self.queue.queue.clear()
        self.thread.join()
        self.video_loader.release_memory()
        del self.video_loader
