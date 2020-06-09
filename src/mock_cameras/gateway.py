from google.protobuf.empty_pb2 import Empty
from is_wire.rpc.context import Context
from is_msgs.common_pb2 import FieldSelector
from is_msgs.camera_pb2 import CameraConfig, CameraConfigFields


class CameraGateway(object):
    def __init__(self, fps: float = 10.0):
        """Create a mock camera gateway. The functions self.get_config and self.set_config receive
        the parameter ctx, because are used as callback funtions for a RPC channel.

        Parameters
        ----------
        fps: float
            sample frequency of images from video source.
        """
        self.fps = fps

    def get_config(self,
                   field_selector: FieldSelector, 
                   ctx: Context) -> CameraConfig:
        """Get the current sample frequency.
        
        Parameters
        ----------
        field_selector: is_msgs.common_pb2.FieldSelector
            Protobuf Object from is_msgs.common_pb2 selecting field SAMPLING_SETTINGS selected.
        ctx: is_wire.rpc.context.Context
            context that defines the request, reply agent.
     
        Returns
        -------
        :class: `is_msgs.camera_pb2.CameraConfig`
            Protobuf Object from is_msgs.camera_pb2 with field frequency filled.
        """
        fields = field_selector.fields
        camera_config = CameraConfig()
        if CameraConfigFields.Value("ALL") in fields or CameraConfigFields.Value(
                "SAMPLING_SETTINGS") in fields:
            camera_config.sampling.frequency.value = self.fps
        return camera_config

    def set_config(self, 
                   camera_config: CameraConfig, 
                   ctx: Context) -> Empty:
        """Set the current sample frequency.

        Parameters
        ----------
        camera_config: is_msgs.camera_pb2.CameraConfig
            CameraConfig Protobuf object with field Frequency filled.
        
        Returns
        -------
        :class: `google.protobuf.empty_pb2.Empty`
        """
        if camera_config.HasField("sampling"):
            if camera_config.sampling.HasField("frequency"):
                self.fps = camera_config.sampling.frequency.value
        return Empty()
