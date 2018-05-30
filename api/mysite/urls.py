"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
# from django.conf.urls import url,include


from rest_framework import routers
from reader import views as reader_views
from core import views as core_views

from rest_framework.authtoken import views as auth_views
from rest_framework.documentation import include_docs_urls

router = routers.DefaultRouter()
router.register(r'users', core_views.UserViewSet)
router.register(r'groups', core_views.GroupViewSet)

# router.register(r'ppage', views.DArticleViewSet)
# router.register(r'pagelist', views.DArticleList)
# router.register(r'pagedetail', views.DArticleDetail)

router.register(r'media', reader_views.MediaViewSet)
router.register(r'articles', reader_views.ArticleViewSet)

router.register(r'words', core_views.WordViewSet)
router.register(r'wordlist', core_views.WordlistViewSet)

router.register(r'userprofile', core_views.UserProfileViewSet)
router.register(r'userwordlist', core_views.UserWordlistViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('test/', include('helloworld.urls')),
    path('admin/', admin.site.urls)
]

urlpatterns += [
    path(r'api-token-auth/', auth_views.obtain_auth_token),
    path(r'dev-token-auth/', core_views.DevAuthToken.as_view()),
    path(r'recommend_article/', reader_views.recommend_article.as_view()),
    path(r'docs/', include_docs_urls(title='LightNews API'))
]
