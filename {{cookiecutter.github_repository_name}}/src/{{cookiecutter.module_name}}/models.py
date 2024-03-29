import datetime
import uuid

from django.db import models
from django_rehive_extras.models import DateModel
from enumfields import EnumField

from {{cookiecutter.module_name}}.enums import CompanyMode


class Company(DateModel):
    identifier = models.CharField(max_length=100, unique=True, db_index=True)
    admin = models.OneToOneField(
        '{{cookiecutter.module_name}}.User',
        related_name='admin_company',
        on_delete=models.CASCADE
    )
    secret = models.UUIDField()
    active = models.BooleanField(default=True, blank=False, null=False)
    mode = EnumField(CompanyMode, blank=True, null=True)

    def __str__(self):
        return self.identifier

    def natural_key(self):
        return (self.identifier,)

    def save(self, *args, **kwargs):
        if not self.id:
            self.secret = uuid.uuid4()

        return super(Company, self).save(*args, **kwargs)


class User(DateModel):
    identifier = models.UUIDField(unique=True, db_index=True)
    token = models.CharField(max_length=200, null=True)
    company = models.ForeignKey(
        '{{cookiecutter.module_name}}.Company',
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.identifier)
