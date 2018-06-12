from django.contrib.auth.models import User, Group
from rest_framework import serializers
from core.models import Word, UserProfile, Wordlist, CommentList, Favourites, Like
import hashlib
from datetime import datetime,date


class UserProfileCheckingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('user',)

    def update(self, instance, validated_data):
        if (instance.check_date == None):
            instance.check_num = 1
        else:
            diff = (date.today() - instance.check_date).days
            if diff == 1:
                instance.check_num = instance.check_num + 1
            elif diff==0:
                pass
            else:
                instance.check_num = 1
        instance.save()
        return instance


class RegSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        userp = UserProfileSerializer()
        userp.create(validated_data={'user': user})
        return user

    class Meta:
        model = User
        fields = ('username', 'password')


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


class CheckingSerializer(serializers.ModelSerializer):
    # glossary =  WordSerializer(many=True)
    class Meta:
        model = UserProfile
        fields = ('user',)


class UserWordlistSerializer(serializers.ModelSerializer):
    glossary = WordSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ('user', 'glossary')


class WordlistSerializer(serializers.ModelSerializer):
    # glossary =  WordSerializer(many=True)
    class Meta:
        model = Wordlist
        fields = ('userprofile', 'word')


class CommentlistSerializer(serializers.ModelSerializer):
    # glossary =  WordSerializer(many=True)
    class Meta:
        model = CommentList
        fields = ('id', 'userprofile', 'article', 'content', 'time')


class LikeSerializer(serializers.ModelSerializer):
    # glossary =  WordSerializer(many=True)
    class Meta:
        model = Like
        fields = ('id', 'userprofile', 'comment')


class FavouriteSerializer(serializers.ModelSerializer):
    # glossary =  WordSerializer(many=True)
    class Meta:
        model = Favourites
        fields = ('id', 'userprofile', 'article')


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
        userp = UserProfileSerializer()
        userp.create(validated_data={'user': user})
        return user
