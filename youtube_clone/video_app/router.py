from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from youtube_clone.video_app.views import VideoActionView, VideoStreamView, VideoDetailsView, VideosView, \
    CommentActionView, CommentVideoView, CommentVideoChildrenView

#video_router = routers.SimpleRouter()
#video_router.register(r'action', VideoActionView, 'video_actions')
#video_router.register(r'stream/([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})', VideoStreamView, 'video_stream')
#video_router.register(r'details/([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})', VideoDetailsView, 'video_details')
#video_router.register(r'all', VideosView, 'all_videos')

#comment_router = routers.SimpleRouter()
#comment_router.register(r'action/([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})', CommentActionView, 'comment_actions')
#comment_router.register(r'details/([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})', VideoCommentView, 'comment_details')
#comment_router.register(r'children/([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})', VideoCommentChildrenView, 'comment_children')


__video_routes = [
    path('action/', VideoActionView.as_view()),
    path('action/<uuid:uuid>', VideoActionView.as_view()),
    path('stream/<uuid:video_reference>', VideoStreamView.as_view()),
    path('details/<uuid:uuid>', VideoDetailsView.as_view()),
    path('all', VideosView.as_view()),
]

__comment_routes = [
    path('action/', CommentActionView.as_view()),
    path('action/<uuid:uuid>', CommentActionView.as_view()),
    path('video/<uuid:video_uuid>', CommentVideoView.as_view()),
    path('children/<uuid:comment_uuid>', CommentVideoChildrenView.as_view()),
]

video_app_urlpatterns = [
    url(r'^video/', include((__video_routes, 'video_app'))),
    url(r'^comment/', include((__comment_routes, 'comment_app'))),
]
