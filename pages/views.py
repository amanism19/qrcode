from django.shortcuts import render
import cv2
from pyzbar.pyzbar import decode
import time
from .forms import *
from django.conf import settings
from django.http import JsonResponse
from PIL import Image
from qrpix.models.networks import ModelQR
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

# Create your views here.
def home(req):
     flag1 = False
     if req.method == 'POST':
          if 'upload1' in req.POST:
               form = ImageForm(req.POST, req.FILES)
               form1 = AdvImageForm()
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
                 if decodedValue == []:
                      flag1 = True     
                 overallDecoded = zip(decodedValue,decodedType)  
                 return render(req, 'index.html', {'form': form, 'img_obj': img_obj, 'form1': form1, 'overallDecoded':overallDecoded,'flag1':flag1 })
          elif 'upload2' in req.POST:
               form1 = AdvImageForm(req.POST, req.FILES)
               form = ImageForm()
               if form1.is_valid():
                 form1.save()
                   # Get the current instance object to display in the template
                 img_obj1 = form1.instance
                 filename = img_obj1.title
                 advScan(img_obj1.image.path, filename)  
                 decodeImg =imgScan('media/mLimg/'+filename+'.png')
                 decodedValue1=[]
                 decodedType1=[]
                 for code in decodeImg:
                      print(code.data.decode('utf-8'))
                      print(code.type)
                      decodedValue1.append(code.data.decode('utf-8'))
                      decodedType1.append(code.type)
                 overallDecoded1= zip(decodedValue1,decodedType1) 
                 return render(req, 'index.html',{'form': form, 'form1': form1, 'overallDecoded1':overallDecoded1, 'img_obj1': img_obj1} )
               
     else:
        form = ImageForm()
        form1 = AdvImageForm()
     return render(req, 'index.html', {'form': form, 'form1': form1})


def imgScan(img):
     imgScan = cv2.imread(img)
     return decode(imgScan)

     
def scan(req):
     cap = cv2.VideoCapture(0)
     cap.set(3,640) #3 - width
     cap.set(4,480) #4 - height
     camera = True
     decodeData = []
     decodeType = []
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
     
def advScan(img, filename):
     model = ModelQR('D:\\QrCode\\Web\\Qrcode\\qrpix\\model.pt')
     output = model.prediction(img)
     output2 = Image.fromarray(output)
     output2.save('media/mLimg/'+filename+'.png')
     pass

@csrf_exempt
def qrdecode(req):
     test2 = req.FILES['qrfile']
     file_name = default_storage.save(test2.name, test2)
     image_path = 'media/'+test2.name
     advScan(image_path , test2.name)
     decodeImg =imgScan('media/mLimg/'+test2.name+'.png')
     
     decodedValue=[]
     decodedType=[]
     
     for code in decodeImg:
          print(code.data.decode('utf-8'))
          print(code.type)
          decodedValue.append(code.data.decode('utf-8'))
          decodedType.append(code.type)
     
     responseData = {
        'decodeType': decodedType,
        'decodeValue': decodedValue,
     }
     return JsonResponse(responseData)