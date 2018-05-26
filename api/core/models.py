from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.contrib.auth.models import AbstractUser


# 内置的词典
class Word(models.Model):
    raw = models.CharField(max_length=50)
    meaning = models.TextField()

    def __str__(self):
        return self.raw


# 用户信息，目前暂时就相当于生词本，但还可以添加更多内容
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 关联自带的User结构
    glossary = models.ManyToManyField(Word, through='Wordlist')  # 生词表
    nickname = models.CharField(max_length=50, default='John')

    # 可以添加更多的资料
    def __str__(self):
        return self.user.__str__()


# 用来存储生词表和用户关联的外键表
class Wordlist(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # 和用户绑定
    word = models.ForeignKey(Word, on_delete=models.CASCADE)  # 单词

    class Meta:
        unique_together = ('userprofile', 'word')  # 唯一性
