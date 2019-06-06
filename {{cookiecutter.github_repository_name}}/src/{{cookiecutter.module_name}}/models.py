import datetime
import uuid

from django.db import models


class DateModel(models.Model):
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.created)

    def save(self, *args, **kwargs):
        if not self.id:  # On create
            self.created = datetime.datetime.now(tz=utc)

        self.updated = datetime.datetime.now(tz=utc)
        return super(DateModel, self).save(*args, **kwargs)


class Company(DateModel):
    identifier = models.CharField(max_length=100, unique=True, db_index=True)
    admin = models.OneToOneField('{{cookiecutter.module_name}}.User',
        related_name='admin_company')
    secret = models.UUIDField()
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    active = models.BooleanField(default=True, blank=False, null=False)

    def __str__(self):
        return self.identifier

    def natural_key(self):
        return (self.identifier,)

    def save(self, *args, **kwargs):
        if not self.id:
            self.secret = uuid.uuid4()

        return super(Company, self).save(*args, **kwargs)

    def get_from_email(self):
        if self.email and self.name:
            return "{name} <{email}>".format(name=self.name,
                email=self.email)
        elif self.email:
            return self.email
        else:
            return os.environ.get('DEFAULT_FROM_EMAIL')

class User(DateModel):
    identifier = models.UUIDField(unique=True, db_index=True)
    token = models.CharField(max_length=200, null=True)
    company = models.ForeignKey('{{cookiecutter.module_name}}.Company', null=True)

    def __str__(self):
        return str(self.identifier)
