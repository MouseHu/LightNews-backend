from rest_framework import serializers
from .models import Article,Media


class MediaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Media
        fields = ('url','name', 'homepage')

class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = ('url','title','abstract','source', 'from_media','pub_date')

class DetailArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title','source','abstract','content','from_media','pub_date')
