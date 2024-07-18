from flask import Flask,Response,render_template 

from flask import Flask, render_template, Response, request
import cv2 as cv
import face_recognition
import numpy as np
import pickle
import os

app = Flask(__name__)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        if len(encodes) > 0:
            encode = encodes[0]
            encodeList.append(encode)
    return encodeList

# Load images and encodings
path = 'images'
images = []
classNames = []
myList = os.listdir(path)
for cl in myList:
    curImg = cv.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

encodeListKnown = findEncodings(images)

@app.route('/')
def index():
    return render_template('index.html')

def gen_frames():
    videocap = cv.VideoCapture(0)
    while True:
        success, frame = videocap.read()
        if not success:
            break
        else:
            frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            face_locs = face_recognition.face_locations(frame_rgb)
            face_encodings = face_recognition.face_encodings(frame_rgb, face_locs)

            for face_loc, face_encoding in zip(face_locs, face_encodings):
                matches = face_recognition.compare_faces(encodeListKnown, face_encoding)
                name = "Unknown"
                
                if True in matches:
                    first_match_index = matches.index(True)
                    name = classNames[first_match_index]
                
                top, right, bottom, left = face_loc
                cv.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv.putText(frame, name, (left, top - 10), cv.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 0), 2)

            ret, buffer = cv.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
