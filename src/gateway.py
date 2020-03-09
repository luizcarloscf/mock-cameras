from google.protobuf.empty_pb2 import Empty
from is_msgs.camera_pb2 import CameraConfig, CameraConfigFields


class CameraGateway(object):
    def __init__(self, fps=10.0):
        """Create a mock camera gateway. The functions self.get_config and self.set_config receive
        the parameter ctx, because are used as callback funtions for a RPC channel.
        Args:
            fps (float): sample frequency of images from video source.
        """
        self.fps = fps

    def get_config(self, field_selector, ctx):
        """Get the current sample frequency.
        Args:
            field_selector (FieldSelector):  Protobuf Object from is_msgs.common_pb2 selecting
            field SAMPLING_SETTINGS selected.
        Returns:
            camera_config (CameraConfig): Protobuf Object from is_msgs.camera_pb2 with field
            frequency filled.
        """
        fields = field_selector.fields
        camera_config = CameraConfig()
        if CameraConfigFields.Value("ALL") in fields or CameraConfigFields.Value(
                "SAMPLING_SETTINGS") in fields:
            camera_config.sampling.frequency.value = self.fps
        return camera_config

    def set_config(self, camera_config, ctx):
        """Set the current sample frequency.
        Args:
            camera_config: CameraConfig Protobuf object with field Frequency filled.
        Returns:
            Empty.
        """
        if camera_config.HasField("sampling"):
            if camera_config.sampling.HasField("frequency"):
                self.fps = camera_config.sampling.frequency.value
        return Empty()
