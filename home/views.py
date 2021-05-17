from home.forms import ReportBug
from django.shortcuts import render
from django.http import HttpResponse,StreamingHttpResponse
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from PIL import ImageTk, Image
from matplotlib import pyplot as plt
from keras.models import load_model
import tensorflow as tf
import numpy as np
import os
from home.models import Event,Sign
import numpy
import random
from django.core.files.storage import FileSystemStorage
import threading
from django.views.decorators import gzip
from cv2 import cv2
from django.views.decorators.csrf import csrf_exempt
from keras.models import load_model

data=['a','b','c']
model = load_model("./models/TS_model2.h5")

def preprocessing(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.equalizeHist(img)
    img = img / 255
    return img


def detect(found , class_name , img_rgb,user):
    for (x, y, width, height) in found:
            
        sign_image = img_rgb[y:y + width, x:x + height]
        sign_image = cv2.cvtColor(sign_image, cv2.COLOR_BGR2RGB)
        img = np.asarray(sign_image)
        img = cv2.resize(img, (32, 32))
        img = preprocessing(img)
        img = img.reshape(1, 32, 32, 1) 
        classIndex = (model.predict_classes(img))
        predictions = model.predict(img)
        probabilityValue = np.amax(predictions)
        
        if className[int(classIndex)][1] == class_name and probabilityValue >3.6:
            if probabilityValue>10:
                probabilityValue = 10.00
            cv2.rectangle(img_rgb, (x, y),(x + height, y + width),(0, 255, 0), 5)
            cv2.putText(img_rgb,class_name + ' ' + str('{:.2f}'.format(probabilityValue*10))+'%',(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,164,0),2)
            
            # add detection to database

            obj = Sign.objects.get(pk=int(classIndex))
            Event.objects.create(user_id=user,sign_id=obj,accuracy=probabilityValue*10)
            data[0]=str(int(classIndex))
           
            if probabilityValue==10:
                data[1]=str(100.0)
            else:
                probabilityValue=probabilityValue*10
                data[1]=str("%.2f" % probabilityValue)


            
    return img_rgb    
       
        
className = [
            ['./models/0.xml', 'Speed limit (20km/h)'],
            ['./models/1.xml', 'Speed limit (30km/h)'],      
            ['./models/2.xml', 'Speed limit (50km/h)'],       
            ['./models/3.xml', 'Speed limit (60km/h)'],      
            ['./models/4.xml', 'Speed limit (70km/h)'],    
            ['./models/5.xml', 'Speed limit (80km/h)'],      
            ['./models/6.xml', 'End of speed limit (80km/h)'],     
            ['./models/7.xml', 'Speed limit (100km/h)'],    
            ['./models/8.xml', 'Speed limit (120km/h)'],     
            ['./models/9.xml', 'No passing'],   
            ['./models/10.xml', 'No passing veh over 3.5 tons'],     
            ['./models/11.xml', 'Right-of-way at intersection'],     
            ['./models/12.xml', 'Priority road'],    
            ['./models/13.xml', 'Yield'],     
            ['./models/14.xml', 'Stop'],       
            ['./models/15.xml', 'No vehicles'],       
            ['./models/16.xml', 'Vehicles > 3.5 tons prohibited'],       
            ['./models/17.xml', 'No entry'],       
            ['./models/18.xml', 'General caution'],     
            ['./models/19.xml', 'Dangerous curve left'],      
            ['./models/20.xml', 'Dangerous curve right'],   
            ['./models/21.xml', 'Double curve'],      
            ['./models/22.xml', 'Bumpy road'],     
            ['./models/23.xml', 'Slippery road'],       
            ['./models/24.xml', 'Road narrows on the right'],  
            ['./models/25.xml', 'Road work'],    
            ['./models/26.xml', 'Traffic signals'],      
            ['./models/27.xml', 'Pedestrians'],     
            ['./models/28.xml', 'Children crossing'],     
            ['./models/29.xml', 'Bicycles crossing'],       
            ['./models/30.xml', 'Beware of ice/snow'],
            ['./models/31.xml', 'Wild animals crossing'],      
            ['./models/32.xml', 'End speed + passing limits'],      
            ['./models/33.xml', 'Turn right ahead'],     
            ['./models/34.xml', 'Turn left ahead'],       
            ['./models/35.xml', 'Ahead only'],      
            ['./models/36.xml', 'Go straight or right'],      
            ['./models/37.xml', 'Go straight or left'],      
            ['./models/38.xml', 'Keep right'],     
            ['./models/39.xml', 'Keep left'],      
            ['./models/40.xml', 'Roundabout mandatory'],     
            ['./models/41.xml', 'End of no passing'],      
            ['./models/42.xml', 'End no passing vehicles > 3.5 tons']
]


@login_required
def home(request):
    context={}
    return render(request, 'home/home.html', context)

@csrf_exempt
@login_required
def reportBug(request):
    if request.method == 'POST':
                
        form = ReportBug(request.POST , request.FILES )
        if form.is_valid():
            form.save()
        return render( request, "home/done.html", {'form':form})     
    
    form = ReportBug()
    return render( request, "home/report.html", {'form':form})    

@login_required
def image_part(request):
    context={}
    return render(request, 'home/image_part.html', context)


@login_required    
def predict(request):
    if request.method == 'POST' and 'image_upload' in request.FILES:
        user=request.user
        fileObj = request.FILES['image_upload']
        fs=FileSystemStorage()
        filePathName=fs.save(fileObj.name,fileObj)
        filePathName=fs.url(filePathName)

        img = cv2.imread('.'+filePathName)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        for i in range(0,42):
            my_data = cv2.CascadeClassifier(className[i][0])    
            found = my_data.detectMultiScale(img_gray,minSize =(20, 20))
            amount_found = len(found)
            if amount_found != 0:
                img_rgb = detect(found,className[i][1],img_rgb,user)   
        
        img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)
        path = './media/' 
        random_number = str(random.randint(1,1000000000))
        random_number = "a"+random_number
        cv2.imwrite(os.path.join(path ,random_number+".jpg"), img_bgr)
        solution=data[0]+data[1]+random_number
        data[0]=''
        data[1]=''
        
        return HttpResponse(solution)
    else:
       return HttpResponse()
    
        
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self,user):

        def preprocessing(img):

            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.equalizeHist(img)
            img = img / 255
            return img


        def detect(found , class_name):
            for (x, y, width, height) in found:
                    
                sign_image = img_rgb[y:y + width, x:x + height]
                sign_image = cv2.cvtColor(sign_image, cv2.COLOR_BGR2RGB)
                img = np.asarray(sign_image)
                img = cv2.resize(img, (32, 32))
                img = preprocessing(img)
                img = img.reshape(1, 32, 32, 1) 
                classIndex = (model.predict_classes(img))
                predictions = model.predict(img)
                probabilityValue = np.amax(predictions)
                if className[int(classIndex)][1] == class_name and probabilityValue >7.6:
                    if probabilityValue>10:
                        probabilityValue = 10.00
                    cv2.rectangle(img_rgb, (x, y),(x + height, y + width),(0, 255, 0), 5)
                    cv2.putText(img_rgb,class_name + ' ' + str('{:.2f}'.format(probabilityValue*10))+'%',(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,164,0),2)
                   
                   # add detection to database

                obj = Sign.objects.get(pk=int(classIndex))
                Event.objects.create(user_id=user,sign_id=obj,accuracy=probabilityValue*10)
                
                
                
        className = [
            ['./models/0.xml', 'Speed limit (20km/h)'],
            ['./models/1.xml', 'Speed limit (30km/h)'],      
            ['./models/2.xml', 'Speed limit (50km/h)'],       
            ['./models/3.xml', 'Speed limit (60km/h)'],      
            ['./models/4.xml', 'Speed limit (70km/h)'],    
            ['./models/5.xml', 'Speed limit (80km/h)'],      
            ['./models/6.xml', 'End of speed limit (80km/h)'],     
            ['./models/7.xml', 'Speed limit (100km/h)'],    
            ['./models/8.xml', 'Speed limit (120km/h)'],     
            ['./models/9.xml', 'No passing'],   
            ['./models/10.xml', 'No passing veh over 3.5 tons'],     
            ['./models/11.xml', 'Right-of-way at intersection'],     
            ['./models/12.xml', 'Priority road'],    
            ['./models/13.xml', 'Yield'],     
            ['./models/14.xml', 'Stop'],       
            ['./models/15.xml', 'No vehicles'],       
            ['./models/16.xml', 'Vehicles > 3.5 tons prohibited'],       
            ['./models/17.xml', 'No entry'],       
            ['./models/18.xml', 'General caution'],     
            ['./models/19.xml', 'Dangerous curve left'],      
            ['./models/20.xml', 'Dangerous curve right'],   
            ['./models/21.xml', 'Double curve'],      
            ['./models/22.xml', 'Bumpy road'],     
            ['./models/23.xml', 'Slippery road'],       
            ['./models/24.xml', 'Road narrows on the right'],  
            ['./models/25.xml', 'Road work'],    
            ['./models/26.xml', 'Traffic signals'],      
            ['./models/27.xml', 'Pedestrians'],     
            ['./models/28.xml', 'Children crossing'],     
            ['./models/29.xml', 'Bicycles crossing'],       
            ['./models/30.xml', 'Beware of ice/snow'],
            ['./models/31.xml', 'Wild animals crossing'],      
            ['./models/32.xml', 'End speed + passing limits'],      
            ['./models/33.xml', 'Turn right ahead'],     
            ['./models/34.xml', 'Turn left ahead'],       
            ['./models/35.xml', 'Ahead only'],      
            ['./models/36.xml', 'Go straight or right'],      
            ['./models/37.xml', 'Go straight or left'],      
            ['./models/38.xml', 'Keep right'],     
            ['./models/39.xml', 'Keep left'],      
            ['./models/40.xml', 'Roundabout mandatory'],     
            ['./models/41.xml', 'End of no passing'],      
            ['./models/42.xml', 'End no passing vehicles > 3.5 tons']
        ]
        
        image = self.frame

        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        for i in range(0,15):
            my_data = cv2.CascadeClassifier(className[i][0])    
            found = my_data.detectMultiScale(img_gray,minSize =(20, 20))
            amount_found = len(found)
            if amount_found != 0:
                detect(found,className[i][1])   
    
        img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)
       
        _, jpeg = cv2.imencode('.jpg', img_bgr)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera,user):

   
    while True:
        frame = camera.get_frame(user)
              
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@login_required
@gzip.gzip_page
def livefe(request):
    try:
        user = request.user
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam,user), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass

