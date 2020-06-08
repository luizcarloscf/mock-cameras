import os
import time
import json
import socket

from gateway import CameraGateway
from utils import load_options, to_pb_image
from frames_loader import FramesLoader

from is_msgs.camera_pb2 import CameraConfig
from google.protobuf.empty_pb2 import Empty
from is_msgs.common_pb2 import FieldSelector
from is_wire.core import Channel, Message, Logger
from is_wire.rpc import ServiceProvider, LogInterceptor


def main():

    service_name = "CameraGateway"
    log = Logger(service_name)
    options = load_options()
    camera = CameraGateway()

    publish_channel = Channel(options['broker_uri'])
    rpc_channel = Channel(options['broker_uri'])
    server = ServiceProvider(rpc_channel)
    logging = LogInterceptor()
    server.add_interceptor(logging)

    server.delegate(topic=service_name + ".*.GetConfig",
                    request_type=FieldSelector,
                    reply_type=CameraConfig,
                    function=camera.get_config)

    server.delegate(topic=service_name + ".*.SetConfig",
                    request_type=CameraConfig,
                    reply_type=Empty,
                    function=camera.set_config)

    while True:

        # iterate through videos listed
        for video in options['videos']:

            # id of the first sequence of videos
            person_id = video['person_id']
            gesture_id = video['gesture_id']

            # getting the path of the 4 videos
            video_files = {
                cam_id:
                os.path.join(options['folder'],
                             'p{:03d}g{:02d}c{:02d}.mp4'.format(person_id, gesture_id, cam_id))
                for cam_id in options["cameras_id"]
            }

            groundtruth_file = os.path.join(options['folder'] , 'p{:03d}g{:02d}_spots.json'.format(person_id, gesture_id))

            for iteration in range(video['iterations']):

                info = {
                    "person": person_id,
                    "gesture": gesture_id,
                    "iteration": iteration
                }
                log.info('{}', str(info).replace("'", '"'))

                # object that let get images from multiples videos files
                video_loader = FramesLoader(video_files, groundtruth_file, gesture_id)

                # iterate through all samples on video
                while True:

                    time_initial = time.time()

                    frame_id, gesture_flag, frames = video_loader.read()

                    for cam in sorted(frames.keys()):
                        pb_image = to_pb_image(frames[cam])
                        msg = Message(content=pb_image)
                        topic = 'CameraGateway.{}.Frame'.format(cam)
                        publish_channel.publish(msg, topic=topic)

                    # listen server for messages about change
                    try:
                        message = rpc_channel.consume(timeout=0)
                        if server.should_serve(message):
                            server.serve(message)
                    except socket.timeout:
                        pass

                    took_ms = (time.time() - time_initial) * 1000

                    dt = (1 / camera.fps) - (took_ms / 1000)
                    if dt > 0:
                        time.sleep(dt)
                        info = {
                            "sample": frame_id,
                            "gesture": gesture_flag,
                            "took_ms": took_ms,
                            "wait_ms": dt * 1000
                        }
                        log.info('{}', str(info).replace("'", '"'))

                    if frame_id >= (video_loader.num_samples - 1):
                        video_loader.release()
                        break

        if options['loop'] is False:
            break


if __name__ == "__main__":
    main()
