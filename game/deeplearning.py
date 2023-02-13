from transformers import AutoTokenizer, AutoModelWithLMHead
from deepface import DeepFace
import urllib.request
import torch
#from azure.cognitiveservices.vision.face import FaceClient
#from azure.cognitiveservices.vision.face.models import FaceAttributeType
#from msrest.authentication import CognitiveServicesCredentials
#tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-emotion")
#model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-emotion")

import cv2
import os

import requests

API_URL = "https://api-inference.huggingface.co/models/mrm8488/t5-base-finetuned-emotion"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def get_emotion(text):
  #input_ids = tokenizer.encode(text + '</s>', return_tensors='pt')

  """output = model.generate(input_ids=input_ids,
               max_length=2)
  """
  output = query({
      "inputs": text,"options" : {"wait_for_model": True},
    })[0]['generated_text']
  output="<pad> "+output
  #dec = [tokenizer.decode(ids) for ids in output]
  #label = dec[0]
  #return label
  #print(output)
  # model을 load할 수 없기 때문에 api로 호출, 다른 방식으로 result가 나오지만 최종적으로는 원래와 똑같은 형태로
  # return합니다.
  return output
#print(get_emotion("i feel as if i havent blogged in ages are at least truly blogged i am doing an update cute"))



# This key will serve all examples in this document.
#KEY = '79c02bc0ff554cc89c0b237064b6570b'

# This endpoint will be used in all examples in this quickstart.
#ENDPOINT = 'https://2022internfaceapp.cognitiveservices.azure.com/'

# Create an authenticated FaceClient.
#face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
#face_attributes = ['emotion']
#face_attributes = ['age', 'gender', 'headPose', 'smile', 'facialHair', 'glasses', 'emotion']
"""def azure_face_api(image):
    im=open(image,'rb')
    #detected_faces = face_client.face.detect_with_stream(im, return_face_attributes=face_attributes)
    #detected_faces = face_client.face.detect_with_stream(im)
    detected_faces=face_client.face.detect_with_url('https://media-cldnry.s-nbcnews.com/image/upload/t_fit-1240w,f_auto,q_auto:best/newscms/2021_07/2233721/171120-smile-stock-njs-333p.jpg', return_face_attributes=face_attributes)
    if not detected_faces:
        #raise Exception(
        #    'No face detected from image {}'.format(os.path.basename(image)))
        return {'message':'no face exists here'},True
    for face in detected_faces:
        print()
        print('Detected face ID from', os.path.basename(image), ':')
        # ID of detected face
        print(face.face_id)
        # Show all facial attributes from the results
        print()
        #print('Facial attributes detected:')
        #print('Age: ', face.face_attributes.age)
        #print('Gender: ', face.face_attributes.gender)
        #print('Head pose: ', face.face_attributes.head_pose)
        #print('Smile: ', face.face_attributes.smile)
        #print('Facial hair: ', face.face_attributes.facial_hair)
        #print('Glasses: ', face.face_attributes.glasses)
        print('Emotion: ')
        
        print('\tAnger: ', face.face_attributes.emotion.anger)
        obj={'anger':face.face_attributes.emotion.anger}
        print('\tContempt: ', face.face_attributes.emotion.contempt)
        obj['contempt']=face.face_attributes.emotion.contempt
        print('\tDisgust: ', face.face_attributes.emotion.disgust)
        obj['disgust']=face.face_attributes.emotion.disgust
        print('\tFear: ', face.face_attributes.emotion.fear)
        obj['fear']=face.face_attributes.emotion.fear
        print('\tHappiness: ', face.face_attributes.emotion.happiness)
        obj['happiness']=face.face_attributes.emotion.happiness
        print('\tNeutral: ', face.face_attributes.emotion.neutral)
        obj['neutral']=face.face_attributes.emotion.neutral
        print('\tSadness: ', face.face_attributes.emotion.sadness)
        obj['sadness']=face.face_attributes.emotion.sadness
        print('\tSurprise: ', face.face_attributes.emotion.surprise)
        obj['surprise']=face.face_attributes.emotion.surprise
        print()
        
        emotions=['anger','contempt','disgust','fear','happiness','neutral','sadness','surprise']
        dominant_emotion='neutral'
        max=0
        for e in emotions:
            if obj[e]>max:
                max=obj[e]
                dominant_emotion=e

        return dominant_emotion,False
"""
#print(azure_face_api("/home/ubuntu/yourchoice/media/Face/smile.jpg"))


def face_expression(file_path):
    backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']
    #face = DeepFace.detectFace(img_path = "img.jpg", target_size = (224, 224), detector_backend =backends[4])
    
    try:
        obj=DeepFace.analyze(img_path=file_path,actions=['emotion'])
    except:
        noface={'message' : 'no face exists here'}
        return noface,True

    return obj,False

import os
import sys
import json

client_id = "3IcEzV3WWP77e0DICyin" # 개발자센터에서 발급받은 Client ID 값
client_secret = "9MXpqzqgti" # 개발자센터에서 발급받은 Client Secret 값

# client_id = "isvat6nlu6" 
# client_secret = "lW8JWPqov2U1gDkqCw8O0lilynaxZQXv8dYDofVw"  

def translate(sentences):
     
    eng=[]
    for sentence in sentences:
        encText = urllib.parse.quote(sentence)
        data = "source=ko&target=en&text=" + encText
        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            words=json.loads(response_body.decode('utf-8'))
            #print(words)
            #print(words['message'])
            #print(words['message']['result'])
            #print(words['message']['result']['translatedText'])
            words=words['message']['result']['translatedText']
            eng.append(words)
        else:
            print("Error Code:" + rescode)
    return eng

#sentences=['이번에는 미국 테네시 주로 가보실까요. 생애 첫 등교에 나선 4살 안나 양이 일열로 늘어선 경찰관들의 환영을 받으며 등장합니다.',
# '한 명 한 명 힘차게 손벽을 부딪히며 반갑게 인사를 나누는데요.',
# '안나에 든든한 지원군을 자처한 경찰관들 왜 이런 자리를 마련했을까요.',
# '안나의 아빠 캐빈 경사는 20년 차 베테랑으로 지난해 11월 의료 응급 상황을 겪은 후 근무 중 돌연 순직했는데요.',
# '그런 안나가 아빠의 빈자리를 느끼지 않도록 경찰 동료 30여 명이 일일 아빠로 깜짝 변신한 겁니다.',
# '안나에게 결코 잊지 못할 하루를 선물했네요. 투데이 와글와글이었습니다.']
#eng=translate(sentences)
#print(get_emotion(eng[0]).split()[1])
def movie_extractor(file_path):
    filepath = file_path
    video = cv2.VideoCapture(filepath) #'' 사이에 사용할 비디오 파일의 경로 및 이름을 넣어주도록 함

    if not video.isOpened():
        print("Could not Open :", filepath)
        return {'error' : 'could not open'}

    length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = round(video.get(cv2.CAP_PROP_FPS))

    print("length :", length)
    print("width :", width)
    print("height :", height)
    print("fps :", fps)

    try:
        if not os.path.exists(filepath[:-4]):
            os.makedirs(filepath[:-4])
    except OSError:
        print ('Error: Creating directory. ' +  filepath[:-4])

    time = 0
    expressions=[]
    times=[]
    while(video.isOpened()):
        ret, image = video.read()
        #print(ret)
        if not ret:
            break
        if(int(video.get(1)) % fps == 0): #앞서 불러온 fps 값을 사용하여 1초마다 추출
            path=filepath[:-4] + "/frame" + str(time)+".jpg"
            cv2.imwrite(path, image)
            #print(str(int(video.get(1))))
            #print(fps)
            #print(int(video.get(1)) % fps)
            #print('Saved frame number :', str(int(video.get(1))))
            exp,noface=face_expression(path)
            #print(exp)
            if noface is False:
                expressions.append(exp)
                times.append(time)
                #numbers.append(video.get(1) / fps)
            time += 1

    #frame_exp=dict(zip(numbers,expressions))

    video.release()
    return {'expressions' : expressions, 'timestamps' : times}

#a=movie_extractor('/home/ubuntu/yourchoice/media/Face/sample.mp4')
#print(a)


naver_url="https://clovaspeech-gw.ncloud.com/external/v1/4480/eedd970a9f4d3b276407106b12afe35ed201b8ae8d6be3761fda65dd967d12ab"
naver_secret="76b16130f99a47da987e06e022a13a1f"


def Speech2Text(name):
    shell="curl --location --request POST '" + naver_url + "/recognizer/upload' --header 'X-CLOVASPEECH-API-KEY: " + naver_secret + " ' --form 'media=@/home/ubuntu/yourchoice/media/Speech/" + str(name) + ".mp4' --form 'params={\"language\":\"ko-KR\",\"completion\":\"sync\"};type=application/json'"

    stream=os.popen(shell)
    output=stream.read()

    ar=json.loads(output)
            #print(ar)

    text=[]
    time=[]
    for i in ar["segments"]:
        text.append(i["text"])
        time.append(round(i["start"]/1000))
    
    return text,time
#import os
#import numpy as np
#import matplotlib.pyplot as plt
#import cv2
#from PIL import Image
#import torch
#import tensorflow as tf
#from tensorflow.keras.models import Model,Sequential, load_model,model_from_json
#from tensorflow.compat.v1.keras.backend import set_session
#config = tf.compat.v1.ConfigProto()
#sess=tf.compat.v1.Session(config=config)
#set_session(sess)
#
#from facial_analysis import FacialImageProcessing
#imgProcessing=FacialImageProcessing(False)
#import torch
#use_cuda = torch.cuda.is_available()
#print(use_cuda)
#
#device = 'cuda' if use_cuda else 'cpu'
#
#from hsemotions.facial_emotions import HSEmotionRecognizer
#
#model_name='enet_b0_8_best_afew'
#model_name='enet_b0_8_best_vgaf'
#model_name='enet_b0_8_va_mtl'
#model_name='enet_b2_8'
#
#fer=HSEmotionRecognizer(model_name=model_name,device=device)


#def face_expression_recognizer(file_path):
#    fpath=file_path
#    frame_bgr=cv2.imread(fpath)
#    frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
#
#    bounding_boxes, points = imgProcessing.detect_faces(frame)
#    points = points.T
#    emotion=0
#    face_img=0
#    for bbox,p in zip(bounding_boxes, points):
#        box = bbox.astype(int)
#        x1,y1,x2,y2=box[0:4]
#        face_img=frame[y1:y2,x1:x2,:]
#        emotion,scores=fer.predict_emotions(face_img,logits=True)
#        print(emotion,scores)
#    
#    return emotion,face_img

#face_expression_recognizer(
        
