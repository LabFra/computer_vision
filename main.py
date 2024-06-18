#from objects import Cam
from objects.Qr import *

program_name = "Detector"

class QrDetector(QrMain):
    def __init__(self, program_name):
        super().__init__()

        cv2.namedWindow(program_name)

        while True:
            ret,self.frame_0 = self.cap.read()
            
            if ret:
                #Bucle camara
                
                self.frame = self.CamFilter(self.frame_0)

                self.frame, isObject = self.ObtainCoords()

                obj_coord = (int(self.p0[0]), int(self.p0[1]))
                
                self.Draw(obj_coord, isObject)
                
                self.QrUpdateCoords()
                
                
            else:
                print("No se puede recibir el fotograma")
                break
            cv2.imshow(program_name+'_0', self.frame_0)
            cv2.imshow(program_name, self.frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()

    def ObtainCoords(self):
        return self.QrDetect(self.frame, self.frame_0)

    def Distance(self,target:list):
            
        distance_x = int(self.width/2-target[0])
        distance_y = int(target[1]-self.height/2)


        #Negativo eje x movimiento hacia la izq positivo mov derecha 
        #Negativo eje y movimiento hacia abajo positivo mov arriba (ESTA INVERTIDO EL EJE)
        
        #print(distance_x, distance_y)

        return distance_x, distance_y
            
    def Draw(self, obj_coord, isObject):

        cv2.putText(self.frame_0,"Target", obj_coord,cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)
        cv2.circle(self.frame_0, obj_coord, 5, (0, 255, 0), -1)
        if(isObject): 
                       
            #print(orig_object_x, orig_object_y)
                    
            distance_x, distance_y = self.Distance(obj_coord)
            #print(distance_x, distance_y)
            #cv2.putText(self.frame_0,f"Distances \n x: {distance_x} \n y: {distance_y}", (int(self.width), int(self.height)),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)
            #cv2.putText(self.frame_0,str(distance_x), (int(self.width), int(self.height)),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)
            color_text = (0,20,255)
                    
            cv2.putText(self.frame_0, 'Distances', (400,400),cv2.FONT_HERSHEY_SIMPLEX, 1, color_text, 2, cv2.LINE_AA)
            cv2.putText(self.frame_0, f'x: {str(distance_x)}', (400,420),cv2.FONT_HERSHEY_SIMPLEX, 1, color_text, 2, cv2.LINE_AA)
            cv2.putText(self.frame_0, f'y: {str(distance_y)}', (400,440),cv2.FONT_HERSHEY_SIMPLEX, 1, color_text, 2, cv2.LINE_AA)
 
        return super().Draw()
    
QrDetector("Detector Qr")