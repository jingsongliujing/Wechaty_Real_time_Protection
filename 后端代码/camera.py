# camera.py

#!/usr/bin/env python
# -*- coding:utf-8 -*-

import cv2
import numpy as np
# import paddlehub as hub
    
class Camera(object):
    """ 通过opencv读取摄像头"""

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        #self.frames = get_frames2()

    def __del__(self):
        self.cap.close()
        
    def get_frame(self):
        flag, frame = self.cap.read()
        assert flag
        flag, jpg = cv2.imencode('.jpg', frame)
        assert flag
        return np.array(jpg).tostring()
        
    # def videotag(self):
    #     videotag = hub.Module(name="videotag_tsn_lstm")
