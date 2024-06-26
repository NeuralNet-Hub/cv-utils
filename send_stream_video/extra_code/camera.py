import cv2
import zmq
import base64
import numpy as np

class VideoCamera(object):

        
    def get_frame(self, port):
        context = zmq.Context()
        footage_socket = context.socket(zmq.SUB)
        footage_socket.bind(f'tcp://*:{port}')
        footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))
        frame = footage_socket.recv_string()
        img = base64.b64decode(frame)
        npimg = np.fromstring(img, dtype=np.uint8)
        source = cv2.imdecode(npimg, 1)
        ret, jpeg = cv2.imencode('.jpg', source)
        return jpeg.tobytes()
