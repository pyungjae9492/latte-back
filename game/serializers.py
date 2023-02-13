from rest_framework import serializers
from .models import *
from dj_rest_auth.registration.serializers import RegisterSerializer



class CustomRegisterSerializer(RegisterSerializer):
    # 기본 설정 필드: username, password, email
    # 추가 설정 필드: profile_image
    is_evaluater= serializers.IntegerField(default=0)
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['is_evaluater'] = self.validated_data.get('is_evaluater', '')

        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model=Blog
        fields='__all__'

class CommentAndStarSerializer(serializers.ModelSerializer):
    class Meta:
        model=CommentAndStar
        fields='__all__'

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model=Movie
        fields='__all__'

class Face_readerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Face_reader
        fields='__all__'

class Speech_to_TextSerializer(serializers.ModelSerializer):
    class Meta:
        model=Speech_to_Text
        fields='__all__'

class Text_readerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Text_reader
        fields='__all__'


class SceneSerializer(serializers.ModelSerializer):
    class Meta:
        model=Scene
        fields='__all__'

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model=Character
        fields='__all__'
class FactSerializer(serializers.ModelSerializer):
    class Meta:
        model=Fact
        fields='__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=Item
        fields='__all__'

class Scene_pictureSerializer(serializers.ModelSerializer):
    class Meta:
        model=Scene_picture
        fields='__all__'

class Scene_textSerializer(serializers.ModelSerializer):
    class Meta:
        model=Scene_text
        fields='__all__'

class Question_AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Character
        fields='__all__'

class DivergesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Character
        fields='__all__'
