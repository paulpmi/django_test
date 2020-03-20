import uuid

from django.db import models

# Create your models here.
from passlib.hash import bcrypt, sha256_crypt


class User(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = models.CharField(max_length=20, unique=True, blank=False, null=False)
    password = models.CharField(max_length=200, blank=False, null=False)
    name = models.CharField(max_length=50)

    active = models.BooleanField(default=False)
    activation_token = models.UUIDField(default=uuid.uuid4, editable=True)

    def encode_password(self, password):
        self.password = sha256_crypt.hash(password)
        return self.password

    def verify_password(self, password):
        if sha256_crypt.verify(password, self.password):
            return True
        return False
