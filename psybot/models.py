from django.db import models


# Create your models here.
class Userinfo(models.Model):
    openid = models.CharField(max_length=100)
    nickname = models.CharField(max_length=50)
    # password = models.CharField(max_length=20)
    portrait = models.CharField(max_length=200)
    sex = models.CharField(max_length=10, null=True, blank=True)#数据库内可以为空值，并且Django角度插入内容可以是空
    age = models.IntegerField(null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    hashid = models.CharField(max_length=20, null=True, blank=True)



# 存储用户打开程序时间，关闭程序时间
class Activityinfo(models.Model):
    user = models.ForeignKey(Userinfo, on_delete=models.CASCADE)
    open_time = models.DateTimeField(auto_now_add=True)
    #end_time = models.DateField(auto_now_add=True)


class Speechinfo(models.Model):
    user = models.ForeignKey(Userinfo, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    create_time = models.DateTimeField(auto_now_add=True)
    label = models.IntegerField(null=True, blank=True)


class Emotioninfo(models.Model):
    user = models.ForeignKey(Userinfo, on_delete=models.CASCADE)
    awake = models.IntegerField(null=True, blank=True)
    create_time = models.DateField(auto_now_add=True)
    efficient = models.CharField(max_length=30)
    belief = models.CharField(max_length=50, null=True, blank=True)
    activity = models.CharField(max_length=300, null=True, blank=True)
    mind = models.CharField(max_length=300, null=True, blank=True)
    contenta = models.CharField(max_length=300, null=True, blank=True)
    contentb = models.CharField(max_length=300, null=True, blank=True)
    contentm = models.CharField(max_length=300, null=True, blank=True)


class Psychologist (models.Model):
    nickname = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    touxiang = models.CharField(max_length=200)
    sex = models.CharField(max_length=10, null=True, blank=True)  # 数据库内可以为空值，并且Django角度插入内容可以是空
    age = models.IntegerField(null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)


class Course_situation(models.Model):
    user = models.ForeignKey(Userinfo, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    image = models.CharField(max_length=1000)


class Report_situation(models.Model):
    user = models.ForeignKey(Userinfo, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    create_time = models.DateTimeField(auto_now_add=True)


class Init_situation(models.Model):
    user = models.ForeignKey(Userinfo, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    image = models.CharField(max_length=1000)


class Relax_situation(models.Model):
    user = models.ForeignKey(Userinfo, on_delete=models.CASCADE)
    practice_type = models.CharField(max_length=50)
    text = models.CharField(max_length=1000)
    image = models.CharField(max_length=1000)


class Check_situation(models.Model):
    user = models.ForeignKey(Userinfo, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)


class Mingxianginfo(models.Model):
    user = models.ForeignKey(Userinfo, on_delete=models.CASCADE)
    mingxiang_type = models.CharField(max_length=50)
    mingxiang_start = models.DateTimeField()
    mingxiang_end = models.DateTimeField()
    mingxiang_response = models.CharField(max_length=500)

class Opinioninfo(models.Model):
    user = models.ForeignKey(Userinfo, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    title = models.CharField(max_length=100)


class Test_situation(models.Model):
    user = models.ForeignKey(Userinfo, on_delete=models.CASCADE)
    create_time = models.DateField(auto_now_add=True)
    test_grade = models.IntegerField(null=True, blank=True)


class OpinioninfoForSRT(models.Model):
    user = models.CharField(max_length=200)
    text = models.CharField(max_length=500)
    title = models.CharField(max_length=100)
