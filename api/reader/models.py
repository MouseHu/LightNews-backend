from django.db import models

# Create your models here.

class Media(models.Model):
    name = models.CharField(max_length=100)
    homepage = models.URLField()
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=1000)
    content = models.TextField()
    abstract =  models.CharField(max_length=1000,default='No abstract')
    source = models.URLField()
    from_media= models.ForeignKey(Media,on_delete=models.CASCADE,null=True)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title
