from django.urls import path
from django.conf.urls import include
from . import views
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('scenes',SceneViewSet)
router.register('text',Text_readerViewSet)
router.register('voice',Speech_to_TextViewSet)
router.register('face',Face_readerViewSet)
router.register('movie',MovieViewSet)
router.register('user',UserViewSet)
router.register('blog',BlogViewSet)
router.register('comment',CommentViewSet)

urlpatterns = [
    path('api/',include(router.urls)),
    path('', views.index, name='index'),
]
