import tkinter as tk
 #from tkinter import *
from tkinter import messagebox as ms
import sqlite3
from PIL import Image, ImageTk
import re
import random
import os, os.path
import cv2
from tkinter.filedialog import askopenfilename
import glob #used to return all file paths that match a specific pattern.

###########################################################################################################################################################################
value = random.randint(1, 1000)
print(value)
emotion=('happy','fear','sad','neutral')
#path="D:/study material/lecture_evaluation/source code/dataset/neutral"
###########################################################################################################################################################################
def upload():
    if not os.path.exists('./dataset'):
        os.makedirs('./dataset')

    face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')
    face_smile = cv2.CascadeClassifier('models/haarcascade_smile.xml')

    #faceDet_two = cv2.CascadeClassifier("9185481.xml")
    faceDet_two = cv2.CascadeClassifier("models/haarcascade_frontalface_alt2.xml")
    faceDet_three = cv2.CascadeClassifier("models/haarcascade_frontalface_alt.xml")
    #faceDet_three = cv2.CascadeClassifier("haarcascade_smile.xml")
    faceDet_four = cv2.CascadeClassifier("models/haarcascade_frontalface_alt_tree.xml")



    font = cv2.FONT_HERSHEY_SIMPLEX
    fileName = askopenfilename(initialdir='/dataset', title='Select image',
                              filetypes=[("all files", "*.*")])
    cap = cv2.VideoCapture(fileName)
    #cap = cv2.VideoCapture(0)

    sampleNum = 0
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ###########################################################################################################
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        fear =  faceDet_four.detectMultiScale(gray, 1.3, 5)
        neutral = faceDet_two.detectMultiScale(gray, 1.3, 5)
        happy =  faceDet_three.detectMultiScale(gray, 1.3, 5)
        sad = face_smile.detectMultiScale(gray, 1.3, 5)
    ###########################################################################################################

        for (x, y, w, h) in faces:
            if fear in faces:
                sampleNum = sampleNum + 1
                cv2.imwrite("dataset/fear/" + str(value) + "." + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
                cv2.putText(img, 'fear', (x + w, y + h), 1, 1, (255, 0,0), 1)
                #cv2.waitKey(100)
                cv2.imshow('frame', img)
    ###############################################################################################################            #cv2.waitKey(1);
            elif happy in faces:
                sampleNum = sampleNum + 1
                cv2.imwrite("dataset/happy/" + str(value) + "." + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
                cv2.putText(img, 'happy', (x + w, y + h), 1, 1, (255, 0, 0), 1)
                #cv2.waitKey(100)
                cv2.imshow('frame', img)
    ###########################################################################################################        #cv2.waitKey(1);
            elif neutral in faces:
                sampleNum = sampleNum + 1
                cv2.imwrite("dataset/neutral/" + str(value) + "." + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
                cv2.putText(img, 'neutral', (x + w, y + h), 1, 1, (255, 0, 0), 1)
                #cv2.waitKey(100)
                cv2.imshow('frame', img)
    ###########################################################################################################        #cv2.waitKey(1);
            elif sad in faces:
                sampleNum = sampleNum + 1
                cv2.imwrite("dataset/sad/" + str(value) + "." + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
                cv2.putText(img, 'sad', (x + w, y + h), 1, 1, (255, 0, 0), 1)
                #cv2.waitKey(100)
                cv2.imshow('frame', img)
                # cv2.waitKey(1);
    ###########################################################################################################



    ###############################################################################################################

    ###############################################################################################################
        cv2.waitKey(1)
        cv2.putText(img, 'Number of Faces : ' + str(len(faces)), (40, 40), font, 1, (255, 0, 0), 2)
        #cv2.putText(img, 'Number of Faces : ' + str(len(happy)), (40, 40), font, 1, (255, 0, 0), 2)
        #cv2.putText(img, 'Number of Faces : ' + str(len(sad)), (40, 40), font, 1, (255, 0, 0), 2)
        #cv2.putText(img, 'Number of Faces : ' + str(len(fear)), (40, 40), font, 1, (255, 0, 0), 2)
        #cv2.putText(img, 'Number of Faces : ' + str(len(neutral)), (40, 40), font, 1, (255, 0, 0), 2)
        # Display the resulting frame
        cv2.waitKey(100)
        cv2.imshow('frame', img)

        if sampleNum > 10:
            ms.showinfo('Success!', 'Face Record Successfully !')
            break

    cap.release()
    
    cv2.destroyAllWindows()

###########################################################################################################################################################################
def files_count():

    happy = 'dataset/happy'

    number_of_Happy_files = len([item for item in os.listdir(happy) if os.path.isfile(os.path.join(happy, item))])
    #print (number_of_Happy_files)
    A = "Happy Students are = {0}".format(number_of_Happy_files)
    print(A)
    #return A

    fear = 'dataset/fear'
    number_of_Fear_files = len([item for item in os.listdir(fear) if os.path.isfile(os.path.join(fear, item))])
    #print(number_of_Fear_files)
    B = "Fear Students are = {0}".format(number_of_Fear_files)
    print(B)
    #return B

    sad = 'dataset/sad'
    number_of_sad_files = len([item for item in os.listdir(sad) if os.path.isfile(os.path.join(sad, item))])
    #print(number_of_sad_files)
    C = "Sad Students are = {0}".format(number_of_sad_files)
    print(C)
    #return C

    neutral = 'dataset/neutral'
    number_of_neutral_files = len([item for item in os.listdir(neutral) if os.path.isfile(os.path.join(neutral, item))])
    #print(number_of_neutral_files)
    D = "Neutral Students are = {0}".format(number_of_neutral_files)
    print(D)
    #return D





    if int(number_of_Happy_files) > int(number_of_Fear_files) and int(number_of_Happy_files) > int(number_of_sad_files) and int(number_of_Happy_files) > int(number_of_neutral_files):
        str_label="Person is Not Depressed "
        print(str_label)

    elif int(number_of_Fear_files) > int(number_of_Happy_files) and int(number_of_Fear_files) > int(number_of_sad_files) and int(number_of_Fear_files) > int(number_of_neutral_files):
        str_label = "Person is in Depression "
        print(str_label)

    elif int(number_of_neutral_files) > int(number_of_Happy_files) and int(number_of_neutral_files) > int(number_of_sad_files) and int(number_of_neutral_files) > int(number_of_Fear_files):
        str_label = "Person is in Depression "
        print(str_label)

    elif int(number_of_sad_files) > int(number_of_Happy_files) and int(number_of_sad_files) > int(number_of_neutral_files) and int(number_of_sad_files) > int(number_of_Fear_files):
        str_label = "Person is in Depression "
        print(str_label)

    return str_label
###########################################################################################################################################################################