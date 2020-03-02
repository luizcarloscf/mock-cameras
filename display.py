import os
import cv2
import sys
import json
import time
import argparse
import numpy as np

from video_loader import MultipleVideoLoader


def place_images(output_image, images, x_offset=0, y_offset=0):
    w, h = images[0].shape[1], images[0].shape[0]
    output_image[0 + y_offset:h + y_offset, 0 + x_offset:w +
                 x_offset, :] = images[0]
    output_image[0 + y_offset:h + y_offset, w + x_offset:2 * w +
                 x_offset, :] = images[1]
    output_image[h + y_offset:2 * h + y_offset, 0 + x_offset:w +
                 x_offset, :] = images[2]
    output_image[h + y_offset:2 * h + y_offset, w + x_offset:2 * w +
                 x_offset, :] = images[3]
    return output_image


def load_options():

    op_file = sys.argv[1] if len(sys.argv) > 1 else 'options.json'
    with open(op_file, 'r') as f:
        op = json.load(f)
    return op


def main():

    options = load_options()

    for video in options['videos']:

        # id of the first sequence of videos
        person_id = video['person_id']
        gesture_id = video['gesture_id']

        # getting the ṕath of the 4 videos
        video_files = {
            cam_id: os.path.join(
                options['folder'],
                'p{:03d}g{:02d}c{:02d}.mp4'.format(person_id, gesture_id,
                                                   cam_id))
            for cam_id in [0, 1, 2, 3]
        }

        video_loader = MultipleVideoLoader(video_files)

        update_image = True

        it_frames = 0
        size = [2 * 728, 2 * 1288, 3]
        full_image = np.zeros(size, dtype=np.uint8)

        count_frames = 0

        while count_frames < video_loader.n_frames():

            n_loaded_frames = video_loader.load_next()

            frames = video_loader[it_frames]
            if frames is not None:
                frames_list = [frames[cam] for cam in sorted(frames.keys())]
                output = place_images(full_image, frames_list)

            # resize image
            resized = cv2.resize(output, (1288, 728),
                                 interpolation=cv2.INTER_AREA)

            cv2.imshow('Frame', resized)

            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

            video_loader.release_memory()
            count_frames += 1

        # Closes all the frames
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()