from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.contrib.auth.models import AbstractUser
from reader.models import Article

# 内置的词典
class Word(models.Model):
    raw = models.CharField(max_length=50,help_text="单词拼写",primary_key=True)
    meaning = models.TextField(help_text="单词释义")

    def __str__(self):
        return self.raw


# 用户信息，目前暂时就相当于生词本，但还可以添加更多内容
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,help_text="用户",primary_key=True)  # 关联自带的User结构
    glossary = models.ManyToManyField(Word, through='Wordlist',help_text="生词表")  # 生词表
    nickname = models.CharField(max_length=50, default='John',help_text="昵称")
    check_date = models.DateField('check_date',help_text="上次签到日期",blank=True,null=True)
    check_num=models.IntegerField(help_text="连续签到天数",default=0)
    comments=models.ManyToManyField(Article, through='Commentlist',help_text="我的评论")  # 生词表
    # 可以添加更多的资料
    def __str__(self):
        return self.user.__str__()



# 用来存储生词表和用户关联的外键表
class Commentlist(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE,help_text="用户")  # 和用户绑定
    article = models.ForeignKey(Article, on_delete=models.CASCADE,help_text="单词")  # 单词
    content=models.TextField(help_text="评论内容")

    class Meta:
        unique_together = ('userprofile', 'article')  # 唯一性


# 用来存储生词表和用户关联的外键表
class Wordlist(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE,help_text="用户")  # 和用户绑定
    word = models.ForeignKey(Word, on_delete=models.CASCADE,help_text="单词")  # 单词

    class Meta:
        unique_together = ('userprofile', 'word')  # 唯一性
