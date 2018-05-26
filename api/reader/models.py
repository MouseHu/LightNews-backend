from django.db import models

# Create your models here.

class Media(models.Model):
    name = models.CharField(max_length=100,help_text="媒体的名称，例如CNN/BBC/...")
    homepage = models.URLField(help_text="媒体的主页")
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=1000,help_text="新闻标题")
    content = models.TextField(help_text="新闻内容，文本格式")
    abstract =  models.CharField(max_length=1000,default='No abstract',help_text="新闻的摘要，用在列表视图中")
    source = models.URLField(help_text="新闻原文地址")
    from_media= models.ForeignKey(Media,on_delete=models.CASCADE,null=True,help_text="新闻来源媒体")
    pub_date = models.DateTimeField('date published',help_text="新闻时间")

    def __str__(self):
        return self.title
