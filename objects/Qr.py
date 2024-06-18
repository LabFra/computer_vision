from objects.Cam import *

class QrMain(CAM):
    def __init__(self):
        super().__init__()
        
        self.points_ant = 0
        self.p0 = None
        self.p1 = None
        self.p2 = None
        self.p3 = None
        self.p4 = None
        
        while np.any(self.points_ant == 0): 
            time.sleep(0.3)
            print("Buscando Qr....")
            ret,self.frame_0 = self.cap.read()

            self.width_qr = None
            self.height_qr = None

            
            self.frame = self.CamFilter(self.frame_0)
            self.old_frame = self.CamFilter(self.frame_0)
            
            self.qr_rect = self.QrObtainCoords()

            if self.qr_rect:
                # Convertir las coordenadas del QR a puntos iniciales para el seguimiento
                #self.points_ant.append(center)
                #self.points_ant.append(self.qr_rect[0])
                #print(self.qr_rect)
                #print(self.points_ant)
                #self.points_ant = np.array(self.qr_rect, dtype=np.float32)
                
                #print(self.points_ant)
                # self.points_ant = self.points_ant.reshape(-1, 1, 2)
                #np.append(self.points_ant,self.qr_rect)
                #print(self.points_ant[0])

                #self.points_ant = np.array([[self.points_ant[0][0][0] + ,]])
                # Definir la región del QR a seguir (usar la caja del QR como ROI inicial)
                self.roi = cv2.boundingRect(self.points_ant)
        
        # Configurar parámetros para Lucas-Kanade
        self.lk_params = dict(winSize=(15, 15), maxLevel=3, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    def QrObtainCoords(self):
        # Decodificar el código QR
        decoded_objects = decode(self.frame)
    
        # Extraer las coordenadas del código QR si se detecta
      
        if decoded_objects:
            qr_data = decoded_objects[0]

            (x, y, self.width_qr, self.height_qr) = decoded_objects[0].rect
            #self.points_ant = np.array([x,y])
            rect = qr_data.polygon
            rect = [tuple(point) for point in rect]
            (self.p1,self.p2,self.p3,self.p4) = rect
            print(rect)

            #center = np.array([self.width_qr/2 + x, self.height_qr/2 + y])
            self.p0 = (self.width_qr/2 + x, self.height_qr/2 + y)
            points = (self.p0, self.p1, self.p2, self.p3, self.p4)

            print(self.p1)

            # points_ant es una matriz de puntos
            self.points_ant = np.array([points], dtype=np.float32)
            print(self.points_ant)
            self.points_ant = self.points_ant.reshape(-1, 1, 2)
            print(self.points_ant)
            return rect
        else:
          return None
    
    def QrUpdateCoords(self):
        # Actualizar el punto de seguimiento usando Lucas-Kanade
        p1, st, err = cv2.calcOpticalFlowPyrLK(self.old_frame, self.frame, self.points_ant, None, **self.lk_params)
        #print(p1)
    
        # Actualizar la posición del QR
        if p1 is not None:
            # Reajustar los puntos y dibujar la caja del QR
            self.points_ant = p1
            rect = cv2.boundingRect(self.points_ant)
            cv2.rectangle(self.frame_0, (rect[0], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]), (0, 255, 0), 2)
        
        self.old_frame = self.frame
        return
    
    def QrDetect(self, frame, frame_0):
        
        isObject = False

        barcodes = decode(frame)

        for barcode in barcodes:
            (x, y, self.width_qr, self.height_qr) = barcode.rect
            barcodeData = barcode.data.decode("utf-8")

            if(barcodeData == "ROBOT"):
                #print(barcodeData)
                isObject = True
                rect = barcode.polygon
                rect = [tuple(point) for point in rect]
                self.p1,self.p2,self.p3,self.p4 = rect
                self.p0 = (self.width_qr/2 + x, self.height_qr/2 + y)

                points = (self.p0, self.p1, self.p2, self.p3, self.p4)
                self.points_ant = np.array([points], dtype=np.float32)
                #print(self.points_ant)
                self.points_ant = self.points_ant.reshape(-1, 1, 2)
                #print(self.points_ant)
                # orig_object_x = x + (w)/2
                # orig_object_y = y + (h)/2
                cv2.rectangle(frame_0, (x,y), (x + self.width_qr, y + self.height_qr), (0,0,255),2)
                # #print(orig_object_x,orig_object_y)
            
        return frame, isObject
    
    def QrTracking(self):
        
         # Actualizar el punto de seguimiento usando Lucas-Kanade
        p1, st, err = cv2.calcOpticalFlowPyrLK(self.frame, self.frame, self.points_ant, None, **self.lk_params)

        # Actualizar la posición del QR
        if p1 is not None:
            # Reajustar los puntos y dibujar la caja del QR
            self.points_ant = p1
            rect = cv2.boundingRect(self.points_ant)
            cv2.rectangle(self.frame_0, (rect[0], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]), (0, 255, 0), 2)
            
        return 
