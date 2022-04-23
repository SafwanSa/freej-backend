from django.db import models


class SoftDeleteManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.with_deleted = kwargs.pop('deleted', False)
        super(SoftDeleteManager, self).__init__(*args, **kwargs)

    def _base_queryset(self):
        return super().get_queryset().filter(deleted_at=None)

    def get_queryset(self):
        qs = self._base_queryset()
        if self.with_deleted:
            return qs
        return qs.filter(is_deleted=False)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    objects = SoftDeleteManager()
    objects_with_deleted = SoftDeleteManager(deleted=True)

    def delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()


class Config(BaseModel):
    key = models.CharField(max_length=200, unique=True)
    value = models.TextField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    is_system = models.BooleanField(default=False)
    is_private = models.BooleanField(default=True)
    tag = models.CharField(max_length=100, blank=True, null=True)

    @property
    def _int(self):
        return int(self.value)

    @property
    def _float(self):
        return float(self.value)

    @property
    def _boolean(self):
        if self.value.lower() in ['true', 'yes', '1', 'yup']:
            return True
        else:
            return False
