from django.db import models

# Create your models here.
class user(models.Model):
    u_name = models.CharField(max_length=100)  # 保存用户名
    u_password = models.CharField(max_length=50)  # 保存密码

    class Meta:
        db_table = 'user'


class idetail(models.Model):

    project_name = models.CharField('项目名称',max_length=300)  # 项目名称
    inter_name = models.CharField(max_length=300)  # 接口名称
    inter_describe = models.TextField(max_length=1000)  # 接口描述
    inter_url = models.CharField(max_length=500)  #  接口URL
    inter_menth = models.CharField(max_length=10)  # 接口方法
    inter_data = models.CharField(max_length=1000)  #  接口参数
    creatime = models.DateTimeField(auto_now_add=True)    #更新时间
    status=models.CharField(max_length=2,default=0)  #状态
    creater=models.CharField(max_length=10)  #创建人
    is_delete = models.CharField(max_length=2,default=0)  # 是否删除

    class Meta:
        db_table = 'idetail'



# class Topic(models.Model):
#     """A topic the user is learning about."""
#     text = models.CharField(max_length=200)
#     date_added = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         """Return a string representation of the model."""
#         return self.text
#
#
# class Entry(models.Model):
#     """Something specific learned about a topic."""
#     topic = models.ForeignKey('Topic', on_delete=models.CASCADE)
#     text = models.TextField()
#     date_added = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         verbose_name_plural = 'entries'
#
#     def __str__(self):
#         """Return a string representation of the model."""
#         return self.text[:50] + "..."