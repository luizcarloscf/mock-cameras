from google.protobuf.empty_pb2 import Empty
from is_msgs.camera_pb2 import CameraConfig, CameraConfigFields


class CameraGateway(object):
    def __init__(self, fps=10):
        self.fps = fps

    def get_config(self, field_selector, ctx):
        fields = field_selector.fields
        camera_config = CameraConfig()

        if CameraConfigFields.Value("ALL") in fields or \
            CameraConfigFields.Value("SAMPLING_SETTINGS") in fields:
            camera_config.sampling.frequency.value = self.fps

        return camera_config

    def set_config(self, camera_config, ctx):

        if camera_config.HasField("sampling"):
            if camera_config.sampling.HasField("frequency"):
                self.fps = camera_config.sampling.frequency.value

        return Empty()