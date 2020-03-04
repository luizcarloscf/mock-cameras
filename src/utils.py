import cv2
import sys
import json
import numpy as np
from is_msgs.image_pb2 import Image


def load_options():
    """Loading options from a json file and return a DICTIONARY object.
    If no location file of options is passed, it searchs for 'options.json'"""
    op_file = sys.argv[1] if len(sys.argv) > 1 else 'etc/conf/options.json'
    with open(op_file, 'r') as f:
        op = json.load(f)
    return op


def to_np_image(input_image):
    """Given a Image (protobuf object), return the numpy image as 
    standard of OpenCV"""
    if isinstance(input_image, np.ndarray):
        output_image = input_image
    elif isinstance(input_image, Image):
        buffer = np.frombuffer(input_image.data, dtype=np.uint8)
        output_image = cv2.imdecode(buffer, flags=cv2.IMREAD_COLOR)
    else:
        output_image = np.array([], dtype=np.uint8)
    return output_image


def to_pb_image(input_image, encode_format='.jpeg', compression_level=0.8):
    """Given a numpy image, return the  as Image (protobuf object)
    standard of is-msgs"""
    if isinstance(input_image, np.ndarray):
        if encode_format == '.jpeg':
            params = [
                cv2.IMWRITE_JPEG_QUALITY,
                int(compression_level * (100 - 0) + 0)
            ]
        elif encode_format == '.png':
            params = [
                cv2.IMWRITE_PNG_COMPRESSION,
                int(compression_level * (9 - 0) + 0)
            ]
        else:
            return Image()
        cimage = cv2.imencode(ext=encode_format,
                              img=input_image,
                              params=params)
        return Image(data=cimage[1].tobytes())
    elif isinstance(input_image, Image):
        return input_image
    else:
        return Image()