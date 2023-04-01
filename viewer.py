# -*- coding: utf-8 -*-


import cv2
import zmq
import base64
import numpy as np
import imutils
from imutils import paths
import pickle
import os
import face_recognition


context = zmq.Context()
footage_socket = context.socket(zmq.SUB)
footage_socket.bind('tcp://*:5555')
footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

cascPathface = os.path.dirname(cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
faceCascade = cv2.CascadeClassifier(cascPathface)
data = pickle.loads(open('face_enc', "rb").read())

while True:
    
    frame = footage_socket.recv_string()
    img = base64.b64decode(frame)
    npimg = np.fromstring(img, dtype=np.uint8)
    source = cv2.imdecode(npimg, 1)
        
    gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(60, 60),flags=cv2.CASCADE_SCALE_IMAGE)
 
    rgb = cv2.cvtColor(source, cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(rgb)
    names = []
    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"
        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            name = max(counts, key=counts.get)
                    
        names.append(name)
        for ((x, y, w, h), name) in zip(faces, names):
            cv2.rectangle(source, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(source, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 255, 0), 2)
    cv2.imshow("Frame", source)
    cv2.waitKey(1) 

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
cv2.destroyALLWindows()