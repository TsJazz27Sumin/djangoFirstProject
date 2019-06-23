from django.db import models
from django.utils import timezone

class CorporateOfficer(models.Model):
    # 管理担当
    responsible_user = models.ForeignKey('auth.User', on_delete=models.CASCADE) 
    # 役名
    position = models.CharField(max_length=200)
    # 職名
    job = models.CharField(max_length=200)
    # 氏名
    name = models.CharField(max_length=200)
    # 生年月日
    birthday = models.DateTimeField(
            blank=True, null=True)
    # 略歴
    biography = models.TextField()
    # 任期
    term = models.CharField(max_length=200)
    # 株式数
    stock = models.CharField(max_length=200)
    # 作成日時
    create_date = models.DateTimeField(
            default=timezone.now)
    # 作成者
    create_user = models.CharField(max_length=200)
    # 更新日時
    update_date = models.DateTimeField(
            default=timezone.now)
    # 更新者
    update_user = models.CharField(max_length=200)

    def create(self):
        self.create_date = timezone.now()
        self.update_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name
