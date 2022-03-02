from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True

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
