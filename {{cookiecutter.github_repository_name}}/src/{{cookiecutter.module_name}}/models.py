import uuid

from django.db import models


class DateModel(models.Model):
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.created)


class Company(DateModel):
    identifier = models.CharField(max_length=100, unique=True, db_index=True)
    admin = models.OneToOneField('{{cookiecutter.module_name}}.User',
        related_name='admin_company')
    secret = models.UUIDField()
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.identifier

    def natural_key(self):
        return (self.identifier,)

    def save(self, *args, **kwargs):
        if not self.id:
            self.secret = uuid.uuid4()

        return super(Company, self).save(*args, **kwargs)


class User(DateModel):
    identifier = models.UUIDField()
    token = models.CharField(max_length=200, null=True)
    company = models.ForeignKey('{{cookiecutter.module_name}}.Company', null=True)

    def __str__(self):
        return str(self.identifier)
