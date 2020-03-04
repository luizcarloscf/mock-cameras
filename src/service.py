import os
import time
import socket

from gateway import CameraGateway
from utils import load_options, to_pb_image
from is_msgs.camera_pb2 import CameraConfig
from google.protobuf.empty_pb2 import Empty
from is_msgs.common_pb2 import FieldSelector
from video_loader import MultipleVideoLoader
from is_wire.core import Channel, Message, Logger
from is_wire.rpc import ServiceProvider, LogInterceptor


def main():

    camera = CameraGateway(fps=10)

    service_name = "CameraGateway"

    # loading options as dict
    options = load_options()

    # logging object
    log = Logger(service_name)

    # connect to the broker
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
                cam_id: os.path.join(
                    options['folder'],
                    'p{:03d}g{:02d}c{:02d}.mp4'.format(person_id, gesture_id,
                                                       cam_id))
                for cam_id in [0, 1, 2, 3]
            }

            # object that let get images from multiples videos files
            video_loader = MultipleVideoLoader(video_files)

            # number of samples (images) on each video file
            log.info("Number of samples: {}".format(video_loader.n_frames()))

            # iterate through all samples on video
            for sample in range(video_loader.n_frames()):

                try:
                    message = rpc_channel.consume(timeout=0)
                    if server.should_serve(message):
                        server.serve(message)
                except socket.timeout:
                    pass

                # getting 4 images
                _ = video_loader.load_next()
                frames = video_loader[0]

                time_initial = time.time()

                if frames is not None:
                    for cam in sorted(frames.keys()):

                        # convert image to Protobuf Image
                        pb_image = to_pb_image(frames[cam])

                        # publish image on topic
                        msg = Message(content=pb_image)
                        topic = 'CameraGateway.{}.Frame'.format(cam)
                        publish_channel.publish(msg, topic=topic)

                # release memory after get images
                video_loader.release_memory()

                took_ms = (time.time() - time_initial) * 1000

                dt = (1 / camera.fps) - (took_ms / 1000)
                if dt > 0:
                    log.info("Sample: {}, took_ms: {}, wait_ms: {}".format(
                        sample, took_ms, dt * 1000))
                    time.sleep(dt)

        if options['loop'] == False:
            break


if __name__ == "__main__":
    main()
