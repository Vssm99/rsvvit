# collects helper functions and classes that “span” multiple levels of MVC
from django.shortcuts import render
# OpenCV-Python is a library of Python bindings designed to solve computer vision problems.
import cv2
# The OS module in Python provides a way of using operating system dependent functionality.
import os
# NumPy is the most basic yet a powerful package for scientific computing and data manipulation  in Python
import numpy as np
# Python Imaging Library is a free library for the Python programming language that adds support for opening, manipulating, and saving many different image file formats.
from PIL import Image
# The csv module helps you to elegantly process data stored within a CSV file. 
import csv
# wrappers library provided to make sending email extra quick, to make it easy to test email sending
# during development, and to provide support for platforms that can’t use SMTP.
from django.core.mail import send_mail
# The method sleep() suspends execution for the given number of seconds. 
from time import sleep
#function definition
def sample(request):
    value=0
    if request.method=="POST" and "student_choice" in request.POST:
        new_student=request.POST.get('student')
        print(new_student)
        if new_student=='yes':
            value=1
        else:
            value=3
    if request.method=="POST" and "register" in request.POST: 
        cam = cv2.VideoCapture(0) #This will return video from the webcam on your computer

            # set video width
        cam.set(3, 640) 
# set video height
        cam.set(4, 480)
# A Haar Cascade is basically a classifier which is used to detect the object for
# which it has been trained for, from the source
        face_detector = cv2.CascadeClassifier('D:\\vaibhav\\rsvsignin\\blog\\train\\haarcascade_frontalface_default.xml')
        print(face_detector)
# For each person, enter one numeric face id
        face_id = int(request.POST.get('student_id'))
        print(face_id)
        face_name = str(request.POST.get('student_name'))
        print(face_name)
        print("\n [INFO] Initializing face capture. Look at the camera and wait ...")
# Initialize individual sampling face count
        count = 0
        while(True):
#reading the video file being captured
            ret, img = cam.read() 
#convert images from one color-space to another
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#detects various facial features mentioned in haarcascade_frontalface_default.xml
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            print(faces)
            for (x,y,w,h) in faces:
#draws a green rectangle at the top-right corner of image.
                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2) 
                count += 1
# Save the captured image into the datasets folder
                cv2.imwrite("D:\\vaibhav\\rsvsignin\\blog\\train\\dataset\\"+ str(face_name) + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
#the function cv2.imshow() is used to display an image in a window.
                cv2.imshow('Face Capture', img)
# Press 'ESC' for exiting video


            k = cv2.waitKey(5) & 0xff 
            if k == 27:
                break
# Take 100 face sample and stop video
            elif count >= 100: 
                break
# Do a bit of cleanup
        print("\n [INFO] Exiting Program and cleanup stuff")
#release the camera resource
        cam.release()
#destroy all created windows
        cv2.destroyAllWindows()
        value=2
    if request.method=="POST" and "train" in request.POST:
# Path for face image database
        path = 'D:\\vaibhav\\rsvsignin\\blog\\train\\dataset'
#Local binary patterns Histogram (LBPH) is a type of visual descriptor used for classification
# in opencv.
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier("D:\\vaibhav\\rsvsignin\\blog\\train\\haarcascade_frontalface_default.xml");
# function to get the images and label data
        def getImagesAndLabels(path):
#get the path of all the files in the folder
            imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
#create empth face list 
            faceSamples=[]
#create empty ID list
            ids = []
#now looping through all the image paths and loading the Ids and the images
            for imagePath in imagePaths:
#loading the image and converting it to gray scale
                PIL_img = Image.open(imagePath).convert('L') # grayscale
#Now we are converting the PIL image into numpy array
                img_numpy = np.array(PIL_img,'uint8')

               
#getting the Id from the image
                id = int(os.path.split(imagePath)[-1].split(".")[1])
# extract the face from the training image sample
                faces = detector.detectMultiScale(img_numpy)
#If a face is there then append that in the list as well as Id of it
                for (x,y,w,h) in faces:
                    faceSamples.append(img_numpy[y:y+h,x:x+w])
                    ids.append(id)
            return faceSamples,ids
        print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
        faces,ids = getImagesAndLabels(path)
#train the model with captured images for respective id's
        recognizer.train(faces, np.array(ids))
# Save the model into trainer/trainer.yml
        recognizer.write('D:\\vaibhav\\rsvsignin\\blog\\train\\trained_model2.yml') 
# Print the numer of faces trained and end program
        print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
        value=3
    if request.method=="POST" and "recognize" in request.POST:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('D:\\vaibhav\\rsvsignin\\blog\\train\\trained_model2.yml')
        cascadePath = "D:\\vaibhav\\rsvsignin\\blog\\train\\haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath);
        font = cv2.FONT_HERSHEY_SIMPLEX
#indiciate id counter
        id = 0
# names related to ids: example ==> Sandesh: id=1, etc
        names = ['Unknown','vaibhav','chandu']
# Initialize and start realtime video capture
        cam = cv2.VideoCapture(0)
# set video width`
        cam.set(3, 640)
# set video height               
        cam.set(4, 480)
# Define min window size to be recognized as a face
#minimum width
        minW = 0.1*cam.get(3)
#minimum height
        minH = 0.1*cam.get(4)
#set of value in the format (id,name,email id)
        data =[[0,'Unknown',''],[1,'vaibhav',''],[2,'chandu',''],]
 #number of lectures per day
        periods=6
        fieldname=['Unique ID','Name','E-mail ID']
        for i in range(periods):
            fieldname.append('Hour '+str(i+1))
        for period in range(periods):
            ret, img =cam.read()
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale( gray,scaleFactor = 1.2,minNeighbors = 5,minSize = (int(minW), int(minH)),)
#input grayscale image.

#Parameter specifying how much the image size is reduced at each image scale. 

# Parameter specifying how many neighbors each candidate rectangle should have to retain it.
# This parameter will affect the quality of the detected faces: higher value results in less 
# detections but with higher quality

#Minimum possible object size. Objects smaller than that are ignored.

            data1=[]
            for(x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

#predict the user Id and confidence of the prediction respectively
                id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
# If confidence is less them 100 ==> "0" : perfect match 
                if (confidence < 100):
                    id=names[id]
                    confidence = " {0}%".format(round(100 -confidence))
                else:
                    id = "Unknown"
                    confidence = " {0}%".format(round(100 -confidence))
                cv2.putText(img, str(id),(x+5,y-5),font,1,(255,255,255),2)
                cv2.putText(img, str(confidence), (x+5,y+h-5),font,1, (255,255,0), 1) 
            cv2.imshow('Face Detection',img)
            cv2.waitKey(10) & 0xff
            data1.append(id)
            print(data1)
            data1=list(set(data1))
            for i in data1:
                data[names.index(i)].insert(period+3,"P") 
            for i in range(len(data)):
                if len(data[i])!=period+4:
                    data[i].insert(period+3,"A")
            sleep(2)
            print(data)
            cam.release()
            cv2.destroyAllWindows()
            cam = cv2.VideoCapture(0)
            cam.set(3, 640) # set video widht
            cam.set(4, 480) # set video height
# Define min window size to be recognized as a face
            minW = 0.1*cam.get(3)
            minH = 0.1*cam.get(4)
#open CSV in write mode to replace previous results and in append mode to append new results
        with open('StudentsDB.csv', 'w') as writeFile:
#write values into csv file in a dictionary form
            writer = csv.DictWriter(writeFile,fieldnames=fieldname)
#write headers of csv file
            writer.writeheader()
#write values into csv file
            writer = csv.writer(writeFile)
#compute values for rows based on output of facial recognition
            writer.writerows(data)
#close csv file
        writeFile.close()
#release camera
        cam.release()
#Destroy all created windows
        cv2.destroyAllWindows()
        print("\n [INFO] Exiting Program and cleanup stuff")
        for i in range(len(data)):
#body of email
            text="Dear Parent, Your Ward " +data[i][1]+ "'s Attendance for today is: "
#subject of the email
            subject = 'Regarding College Attendance'
            if i==4 or i==3 or i==8:
                print(data[i][1])
                count=periods
                for j in range(periods):
                    if data[i][j+3]=='A':
                        count-=1
                print(count)
                text+=str((count*100)/periods)+' %'
#send email to corresponding student's parent's email id
                send_mail(subject,text,'',[data[i][2]],fail_silently=False)
#indicate end of program 
        print("End of Face Detection")
    return render(request,"sample.html",{"value":value})

