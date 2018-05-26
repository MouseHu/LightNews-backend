from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Word, UserProfile, Wordlist


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'url', 'name')


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ('raw', 'meaning')


class UserProfileSerializer(serializers.ModelSerializer):
    glossary =  WordSerializer(many=True)
    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'glossary')


class WordlistSerializer(serializers.ModelSerializer):
    # glossary =  WordSerializer(many=True)
    class Meta:
        model = Wordlist
        fields = ('id', 'userprofile', 'word')
