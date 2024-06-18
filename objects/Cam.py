import cv2
from pyzbar.pyzbar import decode
from PIL import Image
import math
import numpy as np
import time

class Control():
    def __init__(self):
        print("Control")
    
    def SendDistance(x,y):
        
        print("Distance x: ", x)
        print("Distance y: ", y)

        return

class CAM():
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
                print("No se puede abrir la camara")
                exit()
        
        ret,self.frame_0 = self.cap.read()

        self.height, self.width = self.frame_0.shape[:2]

    def CamFilter(self, frame):

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #frame = cv2.GaussianBlur(frame, (5, 5), 0)
        frame = cv2.bilateralFilter(frame,15,80,80)
        _,frame = cv2.threshold(frame, 100, 255, cv2.THRESH_BINARY)

        return frame
    
    def Draw(self):
        
        color_lines = (200,0,200)
        color_square = (255,0,0)
        
        self.frame_0 = self.DrawCross(self.frame_0, self.width, self.height, color_lines)
        self.frame_0 = self.DrawSquare(self.frame_0, self.width, self.height, color_square, 30)

        #print(height/2, width/2)
        return
    
    def DrawCross(self, frame, width, height, color_lines):
        cv2.line(frame, (int(width/2),0), (int(width/2),height),color_lines,3)
        cv2.line(frame, (0,int(height/2)), (width,int(height/2)),color_lines,3)

        return frame
    
    def DrawSquare(self, frame, width, height, color_square, w_square):
        '''
        frame       : image to work
        width       : camera width
        height      : camera height
        color_square: color
        w_square    : square width
        '''
        
        x1 = int(width - width/2 - w_square)
        y1 = int(height - height/2 - w_square)

        x2 = int(x1 + 2*(w_square))
        y2 = int(y1 + 2*(w_square))

        
        cv2.rectangle(frame, (x1, y1), (x2, y2), color_square, 4)

        return frame

