from rest_framework import serializers
from reader.models import Article,Media


class MediaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Media
        fields = ('url','name', 'homepage')

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id','url','title','abstract','source', 'author','from_media','pub_date','img_url')

class DetailArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id','title','source','author','abstract','content','from_media','pub_date','img_url')
