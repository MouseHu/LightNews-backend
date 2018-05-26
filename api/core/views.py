from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import *
from .models import Word, UserProfile, Wordlist
from .permissions import *
from rest_framework import permissions
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class WordViewSet(viewsets.ModelViewSet):
    """
    list:
    列出字典中所有单词。此条API不应该被调用。

    retrieve:
    返回某个单词。

    create:
    增加单词。只用管理员可以调用。

    delete:
    删除单词。只用管理员可以调用。

    """
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, permissions.IsAdminUser) #only admin is able to add words


class WordlistViewSet(viewsets.ModelViewSet):
    """
    list:
    列出所有的用户-生词对。此条API不应该被调用。

    retrieve:
    返回某个用户-生词对。此条API一般情况下不应该被调用。

    create:
    给某个用户的生词本添加一个生词。

    delete:
    给某个用户的生词本删除一个生词。

    """

    queryset = Wordlist.objects.all()
    serializer_class = WordlistSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, wordlist_permission) # any one can edit itself wordlist


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    list:
    列出所有用户资料。

    retrieve:
    返回某个用户的资料。

    create:
    创建一条用户资料。此条API不应该被调用。应该在用户注册时自动创建。

    delete:
    删除一条用户资料。此条API不应该被调用。

    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, userprofile_permission) # any one can edit itself UserProfile


class UserWordlistViewSet(viewsets.ModelViewSet):
    """
    list:
    列出所有用户的生词本（TODO:每个用户应该只能看见自己的生词本）。

    retrieve:
    返回某个用户的生词本。

    create:
    此条API不应该被调用。应该在用户注册时自动创建。

    delete:
    此条API不应该被调用。

    """
    queryset = UserProfile.objects.all()
    serializer_class = UserWordlistSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, userprofile_permission)
    filter_fields = ('user',)