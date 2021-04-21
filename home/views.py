from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from PIL import ImageTk, Image
import numpy
from keras.models import load_model

model = load_model('./models/model_fers.h5')


classes = { 0:'0Speed limit (20km/h)',
            1:'1Speed limit (30km/h)',      
            2:'2Speed limit (50km/h)',       
            3:'3Speed limit (60km/h)',      
            4:'4Speed limit (70km/h)',    
            5:'5Speed limit (80km/h)',      
            6:'6End of speed limit (80km/h)',     
            7:'7Speed limit (100km/h)',    
            8:'8Speed limit (120km/h)',     
            9:'9No passing',   
           10:'10No passing veh over 3.5 tons',     
           11:'11Right-of-way at intersection',     
           12:'12Priority road',    
           13:'13Yield',     
           14:'14Stop',       
           15:'15No vehicles',       
           16:'16Vehicles > 3.5 tons prohibited',       
           17:'17No entry',       
           18:'18General caution',     
           19:'19Dangerous curve left',      
           20:'20Dangerous curve right',   
           21:'21Double curve',      
           22:'22Bumpy road',     
           23:'23Slippery road',       
           24:'24Road narrows on the right',  
           25:'25Road work',    
           26:'26Traffic signals',      
           27:'27Pedestrians',     
           28:'28Children crossing',     
           29:'29Bicycles crossing',       
           30:'30Beware of ice/snow',
           31:'31Wild animals crossing',      
           32:'32End speed + passing limits',      
           33:'33Turn right ahead',     
           34:'34Turn left ahead',       
           35:'35Ahead only',      
           36:'36Go straight or right',      
           37:'37Go straight or left',      
           38:'38Keep right',     
           39:'39Keep left',      
           40:'40Roundabout mandatory',     
           41:'41End of no passing',      
           42:'42End no passing vehicles > 3.5 tons' }


@login_required
def home(request):
    context={}
    return render(request, 'home/home.html', context)


@login_required    
def predict(request):
    if request.method == 'POST' and 'image_upload' in request.FILES:
        image = Image.open(request.FILES['image_upload'])
        image = image.resize((30,30))
        image = numpy.expand_dims(image, axis=0)
        image = numpy.array(image)
        pred = model.predict_classes([image])[0]
        sign = classes[pred]
        result={"prediction" : pred , "sign" : sign }
        print(result)
        return HttpResponse(sign)
    else:
        result={} 
        return HttpResponse(result) 
    
        

@login_required
def report_bug(request):
   return render(request, 'home/report.html', {'title' : 'report'})

