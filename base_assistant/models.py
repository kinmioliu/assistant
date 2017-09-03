from django.db import models

# Create your models here.
#Sclass Version_Info(models.Model):
class VersionInfo(models.Model):
    product = models.CharField(max_length=20)
    platform_ver = models.CharField(max_length=20)
    product_ver = models.CharField(max_length=20)
    verinfo = models.CharField(max_length=200)

#解决方法
class Solution(models.Model):
    solutionname = models.CharField(max_length=100)
    url = models.URLField()

#责任田
class ResponsibilityField(models.Model):
    groupname = models.CharField(max_length=50)
    introduce = models.URLField()
    plname = models.CharField(max_length=50)

#mml信息
class MMLCmdInfo(models.Model):
    #命令行
    cmdname = models.CharField(max_length=30)
    #所属责任田
    responsefield = models.ForeignKey("ResponsibilityField")
    #相关问题列表
    solutions = models.ManyToManyField("Solution")

class Questions(models.Model):
    #相关产品
    product = models.CharField(max_length=30)

class Replay(models.Model):
    #QuestionID
    question = models.ForeignKey("Solution")
    #Replay
    question = models.ForeignKey("Replay")
    #url 指向wiki的
    url = models.URLField()
    #describe
    describe = models.CharField(max_length=200)


