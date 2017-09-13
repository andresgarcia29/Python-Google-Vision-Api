import io
import json

from google.cloud import vision
from google.cloud.vision import types

from pymongo import MongoClient
import collections

clientMongo = MongoClient('mongodb://localhost:27017/')
db = clientMongo['GoogleVision']
collection = db['ResultsExpressions']

client = vision.ImageAnnotatorClient()

file_name = input("Drag and drop your image here: ")
file_name = file_name.strip()

with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

def detect_face(face_file, max_results=100):
    return client.face_detection(image=image).face_annotations

results = detect_face(image)

if (results): print("Reconocimiento completado.")

record = {
  "type" : "Results of google expresions",
  "roll_angle": results[0].roll_angle, 
  "pan_angle": results[0].pan_angle, 
  "tilt_angle": results[0].tilt_angle, 
  "detection_confidence": results[0].detection_confidence, 
  "landmarking_confidence": results[0].landmarking_confidence, 
  "joy_likelihood": results[0].joy_likelihood, 
  "sorrow_likelihood": results[0].sorrow_likelihood, 
  "anger_likelihood": results[0].anger_likelihood, 
  "surprise_likelihood": results[0].surprise_likelihood, 
  "under_exposed_likelihood": results[0].under_exposed_likelihood, 
  "blurred_likelihood": results[0].blurred_likelihood, 
  "headwear_likelihood": results[0].headwear_likelihood
}

for x in results[0].landmarks:
  current_name = ''
  if (x.type == 1):
    current_name = "LEFT_EYE"
  if (x.type == 2):
    current_name = "RIGHT_EYE"
  if (x.type == 3):
    current_name = "LEFT_OF_LEFT_EYEBROW"
  if (x.type == 4):
    current_name = "RIGHT_OF_LEFT_EYEBROW"
  if (x.type == 5):
    current_name = "LEFT_OF_RIGHT_EYEBROW"
  if (x.type == 6):
    current_name = "RIGHT_OF_RIGHT_EYEBROW"
  if (x.type == 7):
    current_name = "MIDPOINT_BETWEEN_EYES"
  if (x.type == 8):
    current_name = "NOSE_TIP"
  if (x.type == 9):
    current_name = "UPPER_LIP"
  if (x.type == 10):
    current_name = "LOWER_LIP"
  if (x.type == 11):
    current_name = "MOUTH_LEFT"
  if (x.type == 12):
    current_name = "MOUTH_RIGHT"
  if (x.type == 13):
    current_name = "MOUTH_CENTER"
  if (x.type == 14):
    current_name = "NOSE_BOTTOM_RIGHT"
  if (x.type == 15):
    current_name = "NOSE_BOTTOM_LEFT"
  if (x.type == 16):
    current_name = "NOSE_BOTTOM_CENTER"
  if (x.type == 17):
    current_name = "LEFT_EYE_TOP_BOUNDARY"
  if (x.type == 18):
    current_name = "LEFT_EYE_RIGHT_CORNER"
  if (x.type == 19):
    current_name = "LEFT_EYE_BOTTOM_BOUNDARY"
  if (x.type == 20):
    current_name = "LEFT_EYE_LEFT_CORNER"
  if (x.type == 21):
    current_name = "LEFT_EYE_PUPIL"
  if (x.type == 22):
    current_name = "RIGHT_EYE_TOP_BOUNDARY"
  if (x.type == 23):
    current_name = "RIGHT_EYE_RIGHT_CORNER"
  if (x.type == 24):
    current_name = "RIGHT_EYE_BOTTOM_BOUNDARY"
  if (x.type == 25):
    current_name = "RIGHT_EYE_LEFT_CORNER"
  if (x.type == 26):
    current_name = "RIGHT_EYE_PUPIL"
  if (x.type == 27):
    current_name = "LEFT_EYEBROW_UPPER_MIDPOINT"
  if (x.type == 28):
    current_name = "RIGHT_EYEBROW_UPPER_MIDPOINT"
  if (x.type == 29):
    current_name = "LEFT_EAR_TRAGION"
  if (x.type == 30):
    current_name = "RIGHT_EAR_TRAGION"
  if (x.type == 31):
    current_name = "FOREHEAD_GLABELLA"
  if (x.type == 32):
    current_name = "CHIN_GNATHION"
  if (x.type == 33):
    current_name = "CHIN_LEFT_GONION"
  if (x.type == 34):
    current_name = "CHIN_RIGHT_GONION"
  if (x.type < 34):
    record[current_name] = {
      "type": current_name,
      "position": {
        "x": x.position.x,
        "y": x.position.y,
        "z": x.position.z
      }
  }

counter = 0
for x in results[0].bounding_poly.vertices:
  if (x.x and x.y):
    record['bounding_poly_vertices_' + str(counter)] = {
      "vertices": {
        "x" : x.x,
        "y" : x.y
      }
    }
  elif (x.x and not x.y):
    record['bounding_poly_vertices_' + str(counter)] = {
      "vertices": {
        "x" : x.x,
      }
    }
  else:
    record['bounding_poly_vertices_' + str(counter)] = {
      "vertices": {
        "y" : x.y
      }
    }
  counter+=1

counter = 0
for x in results[0].fd_bounding_poly.vertices:
  if (x.x and x.y):
    record['fd_bounding_poly' + str(counter)] = {
      "vertices": {
        "x" : x.x,
        "y" : x.y
      }
    }
  elif (x.x and not x.y):
    record['fd_bounding_poly' + str(counter)] = {
      "vertices": {
        "x" : x.x,
      }
    }
  else:
    record['fd_bounding_poly' + str(counter)] = {
      "vertices": {
        "y" : x.y
      }
    }
  counter+=1

collection.save(record)
print("Resultados guardados correctamente.")