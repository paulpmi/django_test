import uuid

from django.db import models
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.
from youtube_clone.authentification_app.models import User


class Video(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, null=False)
    description = models.CharField(max_length=700, null=False)
    video_reference = models.UUIDField(editable=True, unique=True, null=False)

    class Meta:
        ordering = ['title']


class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user_uuid = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    video_uuid = models.ForeignKey(Video, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200, null=False)
    parent_comment = models.ForeignKey('self', default=None, null=True, on_delete=models.CASCADE)

    @property
    def has_children(self):
        try:
            Comment.objects.get(video_uuid=self.video_uuid, parent_comment=self.parent_comment)
            return True
        except ObjectDoesNotExist:
            return False
