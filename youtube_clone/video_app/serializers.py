from rest_framework import serializers

from youtube_clone.video_app.models import Video, Comment


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'video_reference', 'user_id']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'comment_text', 'parent_comment', 'user_uuid', 'video_uuid', 'has_children']
