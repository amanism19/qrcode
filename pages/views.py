from django.shortcuts import render
import cv2
from pyzbar.pyzbar import decode
import time
from .forms import ImageForm
from django.conf import settings
from django.http import JsonResponse

# Create your views here.
def home(req):
     if req.method == 'POST':
        form = ImageForm(req.POST, req.FILES)
        if form.is_valid():
          form.save()
            # Get the current instance object to display in the template
          img_obj = form.instance
           
          decodeImg =imgScan(img_obj.image.path)
          decodedValue=[]
          decodedType=[]
          for code in decodeImg:
               print(code.data.decode('utf-8'))
               print(code.type)
               decodedValue.append(code.data.decode('utf-8'))
               decodedType.append(code.type)
          overallDecoded = zip(decodedValue,decodedType)
             
          return render(req, 'index.html', {'form': form, 'img_obj': img_obj, 'overallDecoded':overallDecoded })
     else:
        form = ImageForm()
     return render(req, 'index.html', {'form': form})


def imgScan(img):
     imgScan = cv2.imread(img)
     return decode(imgScan)

     
def scan(req):
     cap = cv2.VideoCapture(0)
     cap.set(3,640) #3 - width
     cap.set(4,480) #4 - height
     camera = True
     decodeData = ["monarch"]
     decodeType = ["death"]
     while camera == True:
          sucess,frame = cap.read()

          for code in decode(frame):
             print(code.data.decode('utf-8'))
             decodeType = decodeType.append(code.type)
             decodeData = decodeData.append(code.data.decode('utf-8'))
             time.sleep(1)

          cv2.imshow('Testing-code-scan', frame)
          
          if cv2.waitKey(1) & 0xFF == 27:
               break
     cap.release()
     cv2.destroyAllWindows()
     print(decodeData)     
     responseData = {
        'decodeType': decodeType,
        'decodeData': decodeData,
     }

     return JsonResponse(responseData)
     