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
from rest_framework.decorators import list_route
from core.permissions import *
from core.serializers import *


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
            user = User.objects.get(username=my_md5(serializer.validated_data['username']))  # retrieve the user using username
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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )#permissions.IsAdminUser) #only admin is able to add words


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

    @action(methods=['post'],detail=False)
    def delete_post(self, request, *arg, **kwarg):
        """
        删除一个用户-单词对。注意，使用了POST方法。
        """
        # retrieve the selected items
        qs = self.filter_queryset(self.get_queryset())
        # delete the selected item
        qs.delete()
        # return deleted
        return Response(status=status.HTTP_204_NO_CONTENT)


    filter_fields = ('userprofile','word')
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

    # @action(methods=['GET','POST','DELETE'], detail=True, permission_classes=[IsAdminOrIsSelf])
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
