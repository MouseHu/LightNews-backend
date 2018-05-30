from django.contrib.auth.models import User, Group
from rest_framework import serializers
from core.models import Word, UserProfile, Wordlist
import hashlib

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
    # glossary =  WordSerializer(many=True)
    class Meta:
        model = UserProfile
        fields = ('user', 'nickname')


class UserWordlistSerializer(serializers.ModelSerializer):
    glossary = WordSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ('user', 'glossary')


class WordlistSerializer(serializers.ModelSerializer):
    # glossary =  WordSerializer(many=True)
    class Meta:
        model = Wordlist
        fields = ('id', 'userprofile', 'word')


def my_md5(dev_id):
    hl = hashlib.md5()
    hl.update(dev_id.encode(encoding='utf-8'))
    return hl.hexdigest()


class DevUserSerializer(serializers.ModelSerializer):
    # glossary =  WordSerializer(many=True)
    class Meta:
        model = User
        fields = ('username',)

    def create(self, validated_data):

        user = User.objects.create(
            username=my_md5(validated_data['username'])
        )
        user.set_password(validated_data['username'])
        user.save()
        userp=UserProfileSerializer()
        userp.create(validated_data={'user': user})
        return user

