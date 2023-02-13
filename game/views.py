from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *
from .deeplearning import *
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
import requests
from rest_framework.views import APIView
from rest_framework.decorators import action

# Create your views here.

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're in index.")

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    def get_queryset(self):
        qs=super().get_queryset()
        #print(qs)
        search=self.request.query_params.get('username','')
        if search:
            qs=qs.filter(username=search)
            
        return qs

class MovieViewSet(viewsets.ModelViewSet):
    queryset=Movie.objects.all()
    serializer_class=MovieSerializer

    # url : movie/{fk}/list_movie_by_user
    @action(detail=True, methods=['get'])
    def list_movie_by_user(self, request, pk):
        user_obj = User.objects.get(id=pk)
        print('user_obj :', user_obj)
        user_is_evaluater = user_obj.is_evaluater
        if user_is_evaluater == 0 : 
            queryset = Movie.objects.filter(author = user_obj).order_by('-is_eval')
        
        else :
            queryset = Movie.objects.all().order_by('is_eval')
        
        serializer = MovieSerializer(queryset, many=True)
         
        return Response(serializer.data)

    def create(self, request):
        serializer = MovieSerializer(data = request.data, many=True)
        uploadedFile = request.FILES.get('uploadedFile')
        if uploadedFile != None and serializer.is_valid() :
            name=request.data["Name"]

            try :
                m=Movie.objects.create(uploadedFile=uploadedFile,Name=name)
            except :
                return HttpResponse('An error occurs.',status=423)
            pub_date=m.pub_date
            
            return JsonResponse({'Name' : m.Name,'pub_date':pub_date},status=201)
        else:
            return HttpResponse(status=500)
    def list(self,request):
        user = request.user
        # user_obj = User.objects.get(id=user)
        user_obj = User.objects.get(id=20)
        user_is_evaluater = user_obj.is_evaluater
        if user_is_evaluater == 0 : 
            queryset = Movie.objects.filter(author = user_obj).order_by('-is_eval')
        
        else :
            queryset = Movie.objects.all().order_by('is_eval')
        
        serializer = MovieSerializer(queryset, many=True)
         
        return Response(serializer.data)

    def get_queryset(self):
        qs=super().get_queryset()
        search=self.request.query_params.get('Name','')
        if search:
            qs=qs.filter(Name=search).first()
        return qs
    
    #def retrieve(self, request, pk=None):
    #    query = Movie.objects.filter(Name_exact=request.data["Name"])
    #    obj = get_object_or_404(query, pk=pk)
    #    serializer = MovieSerializer(obj)
    #    return Response(serializer.data)

class SceneViewSet(viewsets.ModelViewSet):
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = CommentAndStar.objects.all()
    serializer_class = CommentAndStarSerializer

    # url : comment/{fk}/list_comment_by_movieid
    @action(detail=True, methods=['get'])
    def list_comment_by_movieid(self, request, pk):
        movie_obj = Movie.objects.get(id=pk)
        print('movie_obj :', movie_obj)
        queryset = CommentAndStar.objects.filter( movie = movie_obj)
        
        serializer = CommentAndStarSerializer(queryset, many=True)
         
        return Response(serializer.data)


class Text_readerViewSet(viewsets.ModelViewSet):
    queryset=Text_reader.objects.all()
    serializer_class = Text_readerSerializer

    def create(self, request):
        serializer = Speech_to_TextSerializer(data = request.data, many=True)
        
        if serializer.is_valid():
            
            text=request.data['Text']
            name=request.data['Name']
            eng=translate([text])[0]

            emotion=get_emotion(str(eng)).split()[1]
            try :
                t=Text_reader.objects.create(Name=name,Text=text,Response={'emotion' : emotion})
            except :
                return HttpResponse('An error occurs.',status=423)
            pub_date=t.pub_date
            response=t.Response
            return JsonResponse(response)
        else:
            return HttpResponse(status=500)

import os
import json
class Speech_to_TextViewSet(viewsets.ModelViewSet):
    queryset=Speech_to_Text.objects.all()
    serializer_class = Speech_to_TextSerializer

    def create(self, request):
        serializer = Speech_to_TextSerializer(data = request.data, many=True)
        uploadedFile = request.FILES.get('uploadedFile')
        
        if uploadedFile != None and serializer.is_valid() :
            name=request.data["Name"]
            
            try :
                s=Speech_to_Text.objects.create(uploadedFile=uploadedFile,Name=name)
            except :
                return HttpResponse('An error occurs.',status=423)
            pub_date=s.pub_date
            kor_texts,times=Speech2Text(name)
            texts=translate(kor_texts)
            emotions=[]

            for text in texts:
                emotions.append(get_emotion(str(text)).split()[1])
            
            s.Response={'texts' : texts, 'emotions' : emotions,'timestamp' : times}
            s.save()
            return JsonResponse(s.Response)
        else:
            return HttpResponse(status=500)


class Face_readerViewSet(viewsets.ModelViewSet):
    queryset=Face_reader.objects.all()
    serializer_class = Face_readerSerializer
    
    def create(self, request):
        serializer = Face_readerSerializer(data = request.data, many=True)
        uploadedFile = request.FILES.get('uploadedFile')
        

        if uploadedFile != None and serializer.is_valid() :
            name=request.data["Name"]
            
            movie_name=name # Face 의 이름을 movie의 이름과 같게 전송해야 한다!

            print("uploaded name : " + str(name))
            #print("movie name : " + str(movie_name))            
            #print(uploadedFile)
            # 차후 동영상에 대해서 프레임을 끊어서 아래의 함수를 돌리는 방안을 검토하자.
            try :
                
                #m=Movie.objects.filter(uploadedFile__endswith=movie_name)[0]
                m=Movie.objects.filter(Name=movie_name).first()
                print(m.is_eval)
                
                if hasattr(m,'face_reader'):
                    f=m.face_reader
                    print("face is : ")
                    print(f)
                    f.delete()
                    #print(m.face_reader)
                

                
                s=Face_reader.objects.create(movie=m,uploadedFile=uploadedFile,Name=name)
                #s=Face_reader.objects.create(uploadedFile=uploadedFile,Name=name)
                #s.movie=m
            except :
                return HttpResponse('An error occurs.',status=423)
            pub_date=s.pub_date
            #expression=face_expression("/home/ubuntu/yourchoice/media/Face/"+name+".jpg")
            if name[-4:] != '.mp4':
                if name[-4]=='.':
                    return JsonResponse({'error' : 'format must be .mp4'})
                else:
                    name=str(name)+'.mp4'
            
            m.is_eval=1
            m.save()
            expression=movie_extractor("/home/ubuntu/yourchoice/media/Face/"+name)
            s.Response=expression
            s.save()
            return JsonResponse(s.Response)
        else:
            return HttpResponse(status=500)
    def list(self,request):
        queryset = Face_reader.objects.all()
        serializer =Face_readerSerializer(queryset, many=True)

        return Response(serializer.data)
    def get_queryset(self):
        qs=super().get_queryset()
        search=self.request.query_params.get('Name','')
        if search:
            qs=qs.filter(Name=search).first()
        return qs

    #def retrieve(self, request, pk=None):
    #    query = Face_reader.objects.get(Name__exact=request.data["Name"])
    #    obj = get_object_or_404(query.movie, pk=pk)
    #    serializer = MovieSerializer(obj)
    #    return Response(serializer.data)
