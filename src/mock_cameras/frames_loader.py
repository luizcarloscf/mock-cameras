from video_loader import MultipleVideoLoader
from is_wire.core import Logger

import numpy as np
import threading
import queue
import time
import json


class FramesLoader:
    def __init__(self,
                 video_list: dict,
                 ground_truth: str,
                 gesture_id: int,
                 fps: float = 10.0):
        """Given a list a video, uses MultipleVideoLoader object to loaded all videos and
        sample at spefic fps on a diferent thread.

        Parameters
        ----------
        video_list: dict
            contais the path of all four video where the key identifies the ID of the camera.
        ground_truth: str
            spots of the gesture
        fps: float
            frequency of sample of the video.
        """
        self.log = Logger("VideoLoaderThread")

        if len(video_list) == 0:
            self.log.warn("You are trying to initialize with a empty list of videos")

        self.video_loader = MultipleVideoLoader(video_list)
        self.num_samples = self.video_loader.n_frames()
        self.truth = self.truth_vector(ground_truth, gesture_id)
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

    def truth_vector(self,
                     spots_file: str,
                     gesture_id: int) -> np.ndarray:
        """Generate a numpy vector one-dimensional. Where it is zero, it represents a non-gesture.
        Where there is a gesture id, it represents in that frame there is gesture. If a spots_file
        is a empty string, it will create a vector with no gesture map.

        Parameters
        ----------
        spots_file: str
            location of the json file with the spots.
        gesture_id: int
            identifier of the gesture.

        Returns
        -------
        :class: `numpy.ndarray`
            one-dimensional array mapping the location of the gesturion in the video.
        """
        try:
            spots = json.load(open(spots_file, 'r'))
        except Exception:
            spots["labels"] = []
        np_vector = np.zeros(self.num_samples)
        for label in spots["labels"]:
            np_vector[label['begin']:label['end']] = gesture_id
        return np_vector

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
                self.queue.put([self.count_sample - 1, self.truth[self.count_sample - 1], frames])
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
        """Returns what it is stored at the Queue by the target of this thread.

        Returns
        -------
        :class: `list`
            That is a list, where the first position is the frame_id, the second is
            the gesture flag indicate the gesture id, the third position is a dictionary
            containing frames from all cameras at same time
        """
        return self.queue.get()

    def release(self):
        """Finish the thread and release any frames on memory.
        """
        self.run = False
        self.thread.join()
        self.video_loader.release_memory()
