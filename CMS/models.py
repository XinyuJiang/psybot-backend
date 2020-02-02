from django.db import models


# Create your models here.
class Userinfo(models.Model):
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=50)
    # password = models.CharField(max_length=20)
	portrait = models.CharField(max_length=200,blank=True)
	sex = models.CharField(max_length=10, null=True, blank=True)#数据库内可以为空值，并且Django角度插入内容可以是空
	age = models.IntegerField(null=True, blank=True)
	department = models.CharField(max_length=50, null=True, blank=True)
	email = models.CharField(max_length=50, null=True, blank=True)
	authority = models.IntegerField(null=True, blank=True)
	phonenumber = models.CharField(max_length=50, null=True, blank=True)

class Loginfo(models.Model):#日志
	user = models.ForeignKey(Userinfo, on_delete=models.CASCADE)
	#text = models.CharField(max_length=1000, null=True, blank=True)
	create_time = models.DateTimeField(auto_now_add=True)
	action = models.IntegerField()
	contentid = models.IntegerField()
