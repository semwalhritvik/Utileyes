import tkinter as tk
from tkinter import messagebox
import numpy as np
import cv2
import speech_recognition as sr
import shutil
from imageai.Detection import ObjectDetection
from gtts import gTTS
import pyttsx3
import os

def detect():
    detector = ObjectDetection()
    model_path = "D:/Hritvik/Utileyes/model/resnet50_coco_best_v2.0.1.h5"
    input_path = "D:/Hritvik/Utileyes/input/img1.png"
    output_path = "D:/Hritvik/Utileyes/output/img.png"
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(model_path)
    detector.loadModel()
    detection = detector.detectObjectsFromImage(input_image=input_path, output_image_path=output_path, minimum_percentage_probability=50)
    for eachItem in detection:
        print(eachItem["name"], " : ", eachItem["percentage_probability"], ":", eachItem["box_points"])
    st = ""
    for x in detection:
        st = st + str(x["name"]) + " "
    print(st)
    mytext = "List of objects from your left to right are as follows "
    final_st = mytext + st
    output_audio = gTTS(text=final_st, lang='en', slow=False)
    os.remove("img1.png")
    output_audio.save("output_audio.mp3")
    os.system("start output_audio.mp3")



def speech():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        engine = pyttsx3.init()
        engine.say('You can speak NOW')
        engine.runAndWait()
        print("Speak now")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    print(r.recognize_google(audio))
    if 'hello' in r.recognize_google(audio):
        cam = cv2.VideoCapture(0)

        cv2.namedWindow("test")

        img_counter = 0

        while True:
            ret, frame = cam.read()
            cv2.imshow("test", frame)
            if not ret:
                break
            k = cv2.waitKey(1)
            img_name = "img1.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written.".format(img_name))
            img_counter += 1
            break
        cam.release()

        cv2.destroyAllWindows()
        detect()


    elif sr.RequestError:
        print("Error")
    elif sr.UnknownValueError:
        print("Error")
    else:
        print("Voice not recognised .Try again")


r= tk.Tk()
r.geometry("400x400")
r.title("Start")
button = tk.Button(r, text="speak", width=25, command=speech).pack()
r.mainloop()