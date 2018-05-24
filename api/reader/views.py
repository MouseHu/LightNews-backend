from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import ArticleSerializer,MediaSerializer,DetailArticleSerializer
from .models import Article,Media
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response



class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = DetailArticleSerializer
    filter_fields = ('title','source')
    def list(self,request):
        queryset = Article.objects.all()
        serializer = ArticleSerializer(queryset, context={'request': request},many=True)
        return Response(serializer.data)

        #filter_fields = ('title','source')


# class DArticleViewSet(viewsets.ModelViewSet):
#     queryset = Article.objects.all()
#     serializer_class = DArticleSerializer
#     filter_fields = ('title',)


#    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

# class DArticleList(generics.ListCreateAPIView):
#     queryset = Article.objects.all()
#     serializer_class = DArticleSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


# class DArticleDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Article.objects.all()
#     serializer_class = DArticleSerializer


class MediaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
