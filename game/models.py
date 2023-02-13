from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    is_evaluater=models.IntegerField(default=0)


class Movie(models.Model):
    Name=models.CharField(max_length=255,null=True,blank=True,help_text="파일명")
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=10)
    uploadedFile = models.FileField(upload_to = "Movie")
    pub_date=models.DateTimeField(default=timezone.now)
    is_eval=models.IntegerField(default=0) 
    def __str__(self):
        return str(self.Name)

class Face_reader(models.Model):
    Name=models.CharField(max_length=255,null=True,blank=True,help_text="파일명")
    uploadedFile = models.FileField(upload_to = "Face")
    pub_date=models.DateTimeField(default=timezone.now)
    movie=models.OneToOneField(Movie,on_delete=models.SET_NULL,null=True,blank=True)
    Response=models.JSONField(default=dict,null=True,blank=True,help_text='{"happy":12.5, "sad":20}')
    def __str__(self):
        return str(self.Name)

class Speech_to_Text(models.Model):
    Name=models.CharField(max_length=255,null=True,blank=True,help_text="파일명")
    uploadedFile = models.FileField(upload_to = "Speech")
    pub_date=models.DateTimeField(default=timezone.now)
    Response=models.JSONField(default=dict,null=True,blank=True,help_text='{"text":"Hi I am"}')
    def __str__(self):
        return str(self.Name)
    
class Text_reader(models.Model):
    Name=models.CharField(max_length=255,null=True,blank=True,help_text="이름")
    Text=models.CharField(max_length=255,null=True,blank=True,help_text="텍스트")
    pub_date=models.DateTimeField(default=timezone.now)
    Response=models.JSONField(default=dict,null=True,blank=True,help_text='{"happy":12.5, "sad":25}')
    
    def __str__(self):
        return str(self.Name)

class Blog(models.Model):
    Title=models.CharField(max_length=255,null=True,blank=True,help_text="제목")
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=10)
    Text=models.CharField(max_length=255,null=True,blank=True,help_text="텍스트")
    pub_date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.Title)

class CommentAndStar(models.Model):
    text = models.CharField(max_length=255,null=True,blank=True,help_text="텍스트")
    star_cnt = models.IntegerField(null=True, blank=True, default=3 )
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=10)
    blog_idx = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True,blank=True)
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE, null=True, default=1)
    def __str__(self):
        return str(self.blog_idx)

class Scene(models.Model):
    id=models.IntegerField(default=0,primary_key=True,help_text="장면 고유 번호")
    Name=models.CharField(max_length=255,null=True,blank=True, help_text="장면 이름")
    NextScene_1=models.ForeignKey('self', related_name='first_next_scene', on_delete=models.SET_NULL,null=True,blank=True, help_text="1번 다음 장면")
    NextScene_2=models.ForeignKey('self',related_name='second_next_scene',on_delete=models.SET_NULL,null=True,blank=True, help_text="2번 다음 장면")
    NextScene_3=models.ForeignKey('self',related_name='third_next_scene',on_delete=models.SET_NULL,null=True,blank=True, help_text="3번 다음 장면")
    NextScene_4=models.ForeignKey('self',related_name='forth_next_scene',on_delete=models.SET_NULL,null=True,blank=True, help_text="4번 다음 장면")
    # 반대 방향으로 참조할 수 있다.
    History=models.ForeignKey('self',related_name="post_scene",on_delete=models.SET_NULL,null=True,blank=True,help_text="이전 장면")
    pub_date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.Name)

class Character(models.Model):
    Name=models.CharField(max_length=255,help_text="인물 이름")
    Comment=models.CharField(max_length=255,null=True,blank=True,help_text="인물 설명")
    HP=models.IntegerField(default=100,help_text="체력")
    MP=models.IntegerField(default=100,help_text="정신력")
    Relation=models.JSONField(default=dict,help_text='{"제퍼슨" : {"fear" : 50, "love" : 10}, "나나" : {"fear" : 20, "love" : 50}}')
    Picture=models.ImageField(upload_to="characters",null=True,blank=True, help_text="이미지 삽화")
    pub_date=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.Name)

class Fact(models.Model):
    Owner=models.ForeignKey(Character,on_delete=models.CASCADE,null=True,blank=True,help_text="소유주")
    Scene = models.ForeignKey(Scene, on_delete=models.CASCADE, help_text="어느 장면에서 얻는 증거인가?")
    Name=models.CharField(max_length=255,help_text="수집한 증거  이름")
    Comment=models.CharField(max_length=255,null=True,blank=True,help_text="수집한 증거 설명")
    Picture=models.ImageField(upload_to="fact",null=True,blank=True, help_text="이미지 삽화")
    pub_date=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.Name)

class Item(models.Model):
    Owner=models.ForeignKey(Character,on_delete=models.CASCADE,null=True,blank=True,help_text="소유주")
    Scene = models.ForeignKey(Scene, on_delete=models.CASCADE, help_text="어느 장면에서 얻는 아이템인가?")
    Name=models.CharField(max_length=255,help_text="아이템 이름")
    Comment=models.CharField(max_length=255,null=True,blank=True,help_text="아이템설명")
    Count=models.IntegerField(default=0,help_text="사용 횟수")
    Max_Count=models.IntegerField(default=9999,help_text="최대 사용 횟수(제한이 있는 경우)")
    Usable=models.BooleanField(default=True,help_text="사용 가능 여부")
    Picture=models.ImageField(upload_to="item",null=True,blank=True, help_text="이미지 삽화")
    pub_date=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.Name)


class Scene_picture(models.Model):
    Scene = models.ForeignKey(Scene, on_delete=models.CASCADE, help_text="장면")
    Picture=models.ImageField(upload_to="scene",null=True,blank=True, help_text="삽화")
    Name=models.CharField(max_length=255,default="씬 번호", help_text="이미지 이름")
    Comment=models.CharField(max_length=255,null=True,blank=True,  help_text="코멘트")
    pub_date=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.Name)

class Scene_text(models.Model):
    Scene = models.ForeignKey(Scene, on_delete=models.CASCADE, help_text="장면")
    Title = models.CharField(max_length=255,default="제목", help_text="제목")
    Narrative=models.TextField(max_length=8192,null=True,blank=True, help_text="내용")
    pub_date=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.Title)

class Question_Answer(models.Model):
    Scene = models.ForeignKey(Scene, on_delete=models.CASCADE)
    Name=models.CharField(max_length=255,default="씬 번호",help_text="제목")
    Question=models.CharField(max_length=1024, help_text="질문")

    Player_Answer=models.CharField(max_length=1024,null=True,blank=True, help_text="플레이어 응답")
    Answer_Number=models.IntegerField(default=0,null=True,blank=True,help_text="AI가 분석한 응답 데이터, optimism : 1, negative : 2, sadness : 3, joy : 4, love : 5, anger : 6, fear : 7, surprise : 8") # 이것은 딥러닝으로 돌아온다.

    Result_list=models.JSONField(default=dict,help_text='{"1":{"f":["마음을 열었다"],"i":["편지"],"r":[{"제퍼슨":{"fear":-5,"love":20}}, {"나나":{"fear":5, "love":-10}} ] }, "2" : ~~ }')

    pub_date=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.Name)

class Diverges(models.Model):
    Scene = models.ForeignKey(Scene, on_delete=models.CASCADE)
    Name=models.CharField(max_length=255,default="분기점",help_text="분기점 이름")
    Comment=models.CharField(max_length=255,null=True,blank=True,  help_text="코멘트")

    Checking_list=models.JSONField(default=dict,help_text='1,2,3,4 분기를 순서대로 확인하여 가장 먼저 맞는 분기로 진행. 만약 1,2,3이 전부 해당하지 않으면 자동으로 4번 분기로 진행. 작성법 예시 : {"1":{"i":["권총","밧줄"],"f":["그것을 알아냈다","저것도 알아냈다"],"r":[{"제퍼슨":"fear"},{"나나":"love"}] },"2":{"i":["권총"],"f":["이것을 알아냈다"],"r":[{"제퍼슨":"love"}] },  }') # 필요한 item, fact, Relation, 들의 목록을 각 분기점에 따라 부여.

    Option=models.IntegerField(default=0,null=True,blank=True,help_text="결정된 분기점 번호")
    
    pub_date=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.Name)
    
