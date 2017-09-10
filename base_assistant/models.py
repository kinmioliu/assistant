from django.db import models

# Create your models here.
#Sclass Version_Info(models.Model):
class VersionInfo(models.Model):
    product = models.CharField(max_length=20)
    platform_ver = models.CharField(max_length=20)
    product_ver = models.CharField(max_length=20)
    verinfo = models.CharField(max_length=200)

    def __str__(self):
        return self.product + "(" + self.platform_ver + ")"

#解决方法
class Solution(models.Model):
    solutionname = models.CharField(max_length=200)
    #是否是问题，默认为False
    is_question = models.BooleanField(default=False)
    #不对称
    next_solution = models.ManyToManyField('self', symmetrical=False, verbose_name='子解决方法')
    url = models.URLField()

    def __unicode__(self):
        return self.solutionname

    def __str__(self):
        return self.solutionname

#标签
class HashTag(models.Model):
        """  HashTag model  """
        name = models.CharField(max_length=64, unique=True)
        solution = models.ManyToManyField(Solution)

        def __unicode__(self):
            return self.name

        def __str__(self):
            return self.name


#责任田
class ResponsibilityField(models.Model):
    groupname = models.CharField(max_length=50, unique=True)
    introduce = models.URLField()
    plname = models.CharField(max_length=50)

    def __unicode__(self):
        return self.groupname

    def __str__(self):
        return self.groupname


#mml信息
class MMLCmdInfo(models.Model):
    #命令行
    cmdname = models.CharField(max_length=30)
    #所属责任田
    responsefield = models.ForeignKey("ResponsibilityField")
    #相关问题列表
    solutions = models.ManyToManyField("Solution", blank=True, null=True)

    def __str__(self):
        return self.cmdname
