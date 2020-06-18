import cv2
import sys
import json
import numpy as np
from is_msgs.image_pb2 import Image


def load_options():
    """Loading options from a json file and return a dict object.
    If no location file of options is passed, it searchs for 'etc/conf/options.json'.
    
    Returns
    -------
    :class: `dict`
        dict with options loaded from a json file.    
    """
    op_file = sys.argv[1] if len(sys.argv) > 1 else 'etc/conf/options.json'
    with open(op_file, 'r') as f:
        op = json.load(f)
    assert isinstance(op['fps'], int)
    assert op['fps'] > 0 and op['fps'] <= 10
    return op


def to_np_image(input_image: Image) -> np.ndarray:
    """Converts a ProtoBuf Object Image to numpy array. 

    Parameters
    ----------
    input_image: is_msgs.image_pb2.Image
        Generate protocol message object from is_msgs that defines an image.
    
    Returns
    -------
    :class: `numpy.ndarray`
            image as a numpy array 
    """
    if isinstance(input_image, np.ndarray):
        output_image = input_image
    elif isinstance(input_image, Image):
        buffer = np.frombuffer(input_image.data, dtype=np.uint8)
        output_image = cv2.imdecode(buffer, flags=cv2.IMREAD_COLOR)
    else:
        output_image = np.array([], dtype=np.uint8)
    return output_image


def to_pb_image(input_image: np.ndarray,
                encode_format: str = '.jpeg', 
                compression_level: float = 0.8) -> Image:
    """Converts a numpy array image to ProtoBuf Message Object
    
    Parameters
    ----------
    input_image: numpy.ndarray
        numpy image in format BGR.
    encode_format: str 
        Define the encoding format from one of the following formats: '.jpeg' or '.png'.
    compression_level: float
        image compression.
    
    Returns
    -------
    :class: `is_msgs.image_pb2.Image`
        Protobuf object defining a image from is_msgs.
    """
    if isinstance(input_image, np.ndarray):
        if encode_format == '.jpeg':
            params = [cv2.IMWRITE_JPEG_QUALITY, int(compression_level * (100 - 0) + 0)]
        elif encode_format == '.png':
            params = [cv2.IMWRITE_PNG_COMPRESSION, int(compression_level * (9 - 0) + 0)]
        else:
            return Image()
        cimage = cv2.imencode(ext=encode_format, img=input_image, params=params)
        return Image(data=cimage[1].tobytes())
    elif isinstance(input_image, Image):
        return input_image
    else:
        return Image()
