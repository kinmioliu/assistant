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

#外部链接
class OuterLink(models.Model):
    link_title = models.CharField(max_length = 128)
    introduce = models.URLField()

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


#责任田
class ResponsibilityField(models.Model):
    groupname = models.CharField(max_length=50, unique=True)
    introduce = models.URLField()
    plname = models.CharField(max_length=50)

    def __unicode__(self):
        return self.groupname

    def __str__(self):
        return self.groupname

class SearchObj(models.Model):
    """ 所有对象的基类"""
    # 相关问题列表
    solutions = models.ManyToManyField("Solution", blank=True, null=True)
    # 相关链接列表
    out_links = models.ManyToManyField("OuterLink", blank=True, null=True)

class FileInfo(SearchObj):
    filename = models.CharField(max_length=30)
    introduce = models.CharField(max_length=50)
    path = models.CharField(max_length=100)
    responsefield = models.ForeignKey("ResponsibilityField", on_delete = models.PROTECT)


#资源信息
class ResoureInfo(SearchObj):
    file = models.ForeignKey("FileInfo", on_delete = models.PROTECT)
    line = models.IntegerField()
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=200)
    #备注
    cmd_mark = models.CharField(max_length = 500)
    #所属责任田
    responsefield = models.ManyToManyField("ResponsibilityField", blank=True, null=True)

    def __str__(self):
        return self.file.filename + self.name + self.code

class ResoureInfoInt(ResoureInfo):
    value = models.IntegerField()
    hexval = models.CharField(max_length = 16)

class ResourceInfoStr(ResoureInfo):
    value = models.CharField(max_length = 50)

class ResourceInfoRud(ResoureInfoInt):
    domain = models.CharField(max_length = 30)

class ResourceInfoModule(ResoureInfoInt):
    introduct = models.CharField(max_length = 500)
    out_link = models.URLField()


#标签
class HashTag(models.Model):
    """  HashTag model  """
    name = models.CharField(max_length=200, unique=True)
#    mmls = models.ManyToManyField("MMLCmdInfo", blank=True, null=True)
#    solutions = models.ManyToManyField("Solution", blank=True, null=True)
#    wikis = models.ManyToManyField("WikiInfo", blank=True, null=True)
#    intreses = models.ManyToManyField("ResoureInfoInt", blank=True, null=True)
#    strreses = models.ManyToManyField("ResourceInfoStr", blank=True, null=True)
#    rudreses =  models.ManyToManyField("ResourceInfoRud", blank=True, null=True)
#    modulereses = models.ManyToManyField("ResourceInfoModule", blank=True, null=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class WikiManager(models.Manager):
    def get_or_create(self, **kwargs):
        defaults = kwargs.pop('defaults', {})
        tag_list = defaults.pop('taglist', {})
        WikiInfo.tag_list = tag_list
        kwargs.update(defaults)
        wikiobj, created = super(WikiManager, self).get_or_create(**kwargs)
        WikiInfo.ModifyFlag = created



class WikiInfo(SearchObj):
    link = models.URLField()    #pk
    title = models.CharField(max_length = 100)
    content = models.TextField()
    abstract = models.TextField()
    group = models.CharField(max_length = 50)
    feature = models.CharField(max_length = 50)
    classes = models.CharField(max_length = 50)
    tag_list = []
    tags = models.ManyToManyField("HashTag", blank=True, null=True)
    objects = WikiManager()
    ModifyFlag = 0

    def save(self, *args, **kwargs):
        super(WikiInfo, self).save()
        for tag in self.tag_list:
            hashtag_obj, created = HashTag.objects.get_or_create(name= tag)
            self.tags.add(hashtag_obj)
        self.taglist = []


#mml信息
class MMLCmdInfo(SearchObj):
    #命令行
    cmdname = models.CharField(max_length=30)
    #功能
    cmd_func = models.CharField(max_length=300)
    #例子
    cmd_sample = models.CharField(max_length = 50)
    #注意事项
    cmd_attention = models.CharField(max_length=500)
    #备注
    cmd_mark = models.TextField()
    #所属责任田
    responsefield = models.ForeignKey("ResponsibilityField", on_delete = models.PROTECT)
    #tag
    tags = models.ManyToManyField("HashTag", blank=True, null=True)

    def __str__(self):
        return self.cmdname

#mml信息
class EVTCmdInfo(SearchObj):
    #命令行
    cmdname = models.CharField(max_length=30)
    #功能
    cmd_func = models.CharField(max_length=300)
    #注意事项
    cmd_attention = models.CharField(max_length=500)
    #备注
    cmd_mark = models.TextField()
    #所属责任田
    responsefield = models.ForeignKey("ResponsibilityField",on_delete = models.PROTECT)
    #tag
    tags = models.ManyToManyField("HashTag", blank=True, null=True)

    def __str__(self):
        return self.cmdname
