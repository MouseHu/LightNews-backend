from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import ArticleSerializer,MediaSerializer,DetailArticleSerializer
from .models import Article,Media
from .permissions import *
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response



class ArticleViewSet(viewsets.ModelViewSet):
    """
    list:
    返回新闻列表

    retrieve:
    返回某一条新闻

    create:
    创建一条新闻。只有管理员才有权限创建。

    delete:
    删除一条新闻。只有管理员才有权限删除。
    """

    def list(self,request):
        queryset = Article.objects.all()
        serializer = ArticleSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    queryset = Article.objects.all()
    serializer_class = DetailArticleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    #filter_fields = ('title','source')  # 暂时先不提供搜索功能


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
    list:
    返回媒体列表。
    其他权限是所有人都能READ，管理员可以WRITE。
    """
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = (IsAdminOrReadOnly,)
