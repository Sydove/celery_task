from django.db import models


class IsDelete:
    normal = 0
    disable = 1

    choices = (
        (0, "正常"),
        (1, "禁止")
    )


class BaseModelQuerySet(models.QuerySet):
    def active(self):
        return self.filter(isDelete=IsDelete.normal)


class BaseModelManager(models.Manager):
    def get_queryset(self):
        return BaseModelQuerySet(self.model, using=self._db).active()


class BaseModel(models.Model):
    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)
    isDelete = models.IntegerField(choices=IsDelete.choices, default=IsDelete.normal)

    objects = BaseModelManager()

    def delete(self, using=None, keep_parents=False):
        self.isDelete = IsDelete.disable
        self.save()

    class Meta:
        abstract = True


class User(BaseModel):
    name = models.CharField(max_length=255, verbose_name="姓名")

    class META:
        db_table = "user"
        verbose_name = "用户表"
        ordering = ["-createTime"]


class Store(BaseModel):
    name = models.CharField(max_length=255, verbose_name="名称")
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)

    class META:
        db_table = "store"
        verbose_name = "店铺表"
        ordering = ["-createTime"]
