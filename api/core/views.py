from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from core.permissions import *
from core.serializers import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework.generics import CreateAPIView

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id})


class Checking(APIView):
    """
    打卡功能。

    create:
    输入用户id。获得 打卡天数。注意：只是获得信息，没有真的打卡。

    update:
    输入用户id并打卡。返回打卡天数。

    """
    if coreapi is not None and coreschema is not None:
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="user",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="用户id",
                        description="用户id",
                    ),
                ),
            ],
            encoding="application/json",
        )


    def post(self, request, *args, **kwargs):
        Userpp = UserProfile.objects.get(user=request.data['user'])
        return Response({
            'check_num': Userpp.check_num,
        })


    def put(self, request, *args, **kwargs):

        Userpp = UserProfile.objects.get(user =request.data['user'])

        serializer = UserProfileCheckingSerializer(Userpp, data=request.data, context={'request': request})
        #  user = serializer.validated_data['user']
        if serializer.is_valid():
            serializer.save()

        return Response({
            'check_num': Userpp.check_num,
        })



class CreateUserView(CreateAPIView):
    if coreapi is not None and coreschema is not None:
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="username",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="username",
                        description="username",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="password",
                        description="password",
                    ),
                )
            ],
            encoding="application/json",
        )


    model = User
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = RegSerializer


def my_md5(dev_id):
    hl = hashlib.md5()
    hl.update(dev_id.encode(encoding='utf-8'))
    return hl.hexdigest()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class DevAuthToken(APIView):
    """
    匿名用户凭借设备号获得token和user id。

    create:
    通过devid获取token.
    对于新设备会自动注册新的userid。

    """
    if coreapi is not None and coreschema is not None:
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="username",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="DevID",
                        description="Device ID",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def post(self, request, *args, **kwargs):
        serializer = DevUserSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(
                username=my_md5(serializer.validated_data['username']))  # retrieve the user using username
        except User.DoesNotExist:
            user = serializer.create(serializer.validated_data)  # return false as user does not exist
        else:
            pass

        #  user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.pk,
        })


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
    permission_classes = (
    permissions.IsAuthenticatedOrReadOnly,)  # permissions.IsAdminUser) #only admin is able to add words


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

    @action(methods=['post'], detail=False)
    def delete_post(self, request, *arg, **kwarg):
        """
        删除一个用户-单词对。注意，使用了POST方法。
        """
        # retrieve the selected items
        # serializer = WordlistSerializer(data=request.data, context={'request': request})

        todelete = self.get_queryset().filter(userprofile=request.data['userprofile'], word=request.data['word'])
        status = todelete.delete()
        return Response({'delete item': status})

    filter_fields = ('userprofile', 'word')
    queryset = Wordlist.objects.all()
    serializer_class = WordlistSerializer
    permission_classes = (
    permissions.IsAuthenticatedOrReadOnly, wordlist_permission)  # any one can edit itself wordlist


class CommentlistViewSet(viewsets.ModelViewSet):
    """
    list:
    列出所有的用户评论。 调用时请参用query方式,例如：  /comments/?userprofile=1&article=2

    retrieve:
    返回某个用户评论。此条API一般情况下不应该被调用。

    create:
    添加某条用户评论。

    delete:
    删除某条用户评论。

    """

    # TODO:权限问题未能完全解决

    def list(self, request):
        queryset = CommentList.objects.all()

        userid = self.request.query_params.get('userprofile', None)
        if userid is not None:
            queryset = queryset.filter(userprofile=userid)

        articleid=self.request.query_params.get('article', None)
        if articleid is not None:
            queryset = queryset.filter(article=articleid)

        serializer = DCommentlistSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)


    filter_fields = ('userprofile', 'article')
    queryset = CommentList.objects.all()
    serializer_class = CommentlistSerializer
    permission_classes = (
    permissions.IsAuthenticatedOrReadOnly, wordlist_permission)  # any one can edit itself wordlist


class LikeViewSet(viewsets.ModelViewSet):
    """
    list:
    列出所有的评论点赞。 调用时请采用query方式,例如：  /like/?userprofile=1&comment=2

    retrieve:
    返回某个用户点赞。此条API一般情况下不应该被调用。

    create:
    添加某条用户点赞。

    delete:
    删除某条用户点赞。

    """

    # TODO:权限问题未能完全解决
    filter_fields = ('userprofile', 'comment')
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (
    permissions.IsAuthenticatedOrReadOnly, wordlist_permission)  # any one can edit itself wordlist


class FavouriteViewSet(viewsets.ModelViewSet):
    """
    list:
    列出所有的用户收藏。应该使用query方式调用。

    retrieve:
    返回某个用户收藏。此条API一般情况下不应该被调用。

    create:
    给某个用户的收藏添加一篇文章。

    delete:
    删除一个收藏。

    """

    def list(self, request):
        queryset = Favourites.objects.all()

        userid = self.request.query_params.get('userprofile', None)
        if userid is not None:
            queryset = queryset.filter(userprofile=userid)

        articleid=self.request.query_params.get('article', None)
        if articleid is not None:
            queryset = queryset.filter(article=articleid)

        serializer =  DFavouriteSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)


    filter_fields = ('userprofile', 'article')
    queryset = Favourites.objects.all()

    # def get_queryset(self):
    #     if self.request.user.is_superuser:
    #         return Favourites.objects.all()
    #     else:
    #         return Favourites.objects.filter(userprofile=self.request.user.id)
    #
    # # TODO:权限问题未能完全解决

    serializer_class = FavouriteSerializer
    permission_classes = (
    permissions.IsAuthenticatedOrReadOnly,)  # any one can edit itself wordlist


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

    # @action(methods=['GET','POST','DELETE'], detail=True)
    # def vocabulary(self, request, pk=None):
    #     if request.method == 'GET':
    #         profile = self.get_object()
    #         serializer=UserWordlistSerializer(profile)
    #         return Response(serializer.data)
    #
    #     if request.method == 'POST':
    #         self.serializer_class = WordlistSerializer
    #         serializer=WordlistSerializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #
    #     if request.method == 'DELETE':
    #         todelete = UserWordlistViewSet.get_queryset().filter(userprofile=pk, word=request.data['word'])
    #         status = todelete.delete()
    #         return Response({'delete item': status})

    # if serializer.is_valid():
    #     serializer.save()
    # return Response(serializer.data, status=status.HTTP_201_CREATED)

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (
    permissions.IsAuthenticatedOrReadOnly, userprofile_permission)  # any one can edit itself UserProfile


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
