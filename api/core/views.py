from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import WordSerializer, UserProfileSerializer, UserSerializer, GroupSerializer, WordlistSerializer
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
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, permissions.IsAdminUser) #only admin is able to add words


class WordlistViewSet(viewsets.ModelViewSet):
    queryset = Wordlist.objects.all()
    serializer_class = WordlistSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, wordlist_permission) # any one can edit itself wordlist


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, userprofile_permission)
