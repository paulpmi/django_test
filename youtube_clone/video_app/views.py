from wsgiref.util import FileWrapper
import uuid

# Create your views here.
# Create your views here.
from django.http import JsonResponse, StreamingHttpResponse
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.parsers import JSONParser, FileUploadParser, MultiPartParser
from rest_framework.views import APIView

from rest_framework import permissions

from youtube_clone.CustomParser.MultiPartJsonParser import MultipartJsonParser
from youtube_clone.security.JWTAuth import JWTAuth
from youtube_clone.video_app.models import Comment, Video
from youtube_clone.video_app.paginators import CommentPaginator, VideoPaginator
from youtube_clone.video_app.serializers import CommentSerializer, VideoSerializer

from youtube_clone.mongo_settings import fs_bucket, fs


class CommentVideoView(ListAPIView):
    permission_classes = [permissions.AllowAny]
    pagination_class = CommentPaginator
    serializer_class = CommentSerializer

    def get_queryset(self):
        video_uuid = self.kwargs['video_uuid']
        return Comment.objects.filter(video_uuid=video_uuid, parent_comment=None)


class CommentVideoChildrenView(ListAPIView):
    permission_classes = [permissions.AllowAny]
    pagination_class = CommentPaginator
    serializer_class = CommentSerializer

    def get_queryset(self):
        comment_uuid = self.kwargs['comment_uuid']
        return Comment.objects.filter(parent_comment=comment_uuid)


class CommentActionView(APIView):
    authentication_classes = [JWTAuth]

    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        data = JSONParser().parse(request)

        token = JWTAuth.decode_jwt(request.headers.get('Authorization').split()[1])
        user_uuid = token['id']
        data['user_uuid'] = user_uuid

        serializer = CommentSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    def put(self, request, uuid):

        try:
            comment = Comment.objects.get(id=uuid)
        except Comment.DoesNotExist:
            return JsonResponse({'Message': 'No comment found'}, status=404)

        try:
            token = JWTAuth.decode_jwt(request.headers.get('Authorization').split()[1])
            user_uuid = token['id']
        except ValidationError as v:
            return JsonResponse({'Message': 'Invalid Authentication'}, status=500)

        if str(comment.user_uuid.id) != str(user_uuid):
            return JsonResponse({'Message': 'Unauthorized'}, status=403)

        data = JSONParser().parse(request)
        data['user_uuid'] = str(comment.user_uuid.id)
        serializer = CommentSerializer(comment, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request, uuid):
        try:
            comment = Comment.objects.get(id=uuid)
        except Comment.DoesNotExist:
            return JsonResponse({'Message': 'No comment found'}, status=404)

        try:
            token = JWTAuth.decode_jwt(request.headers.get('Authorization').split()[1])
            user_uuid = token['id']
        except ValidationError as v:
            return JsonResponse({'Message': 'Invalid Authentication'}, status=500)

        if str(comment.user_uuid.id) != str(user_uuid):
            print(comment.user_uuid.id, user_uuid)
            return JsonResponse({'Message': 'Unauthorized'}, status=403)

        comment.delete()
        return JsonResponse({'Message': 'Success'}, status=200)


class VideosView(ListAPIView):
    permission_classes = [permissions.AllowAny]
    pagination_class = VideoPaginator
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class VideoDetailsView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = VideoSerializer

    def get(self):
        video_uuid = self.request.video_uuid
        return Video.objects.get(id=video_uuid)


class VideoStreamView(APIView):

    def get(self, request, video_reference, format=None):
        grid_out = fs_bucket.open_download_stream_by_name(str(video_reference))
        chunk_size = 8192
        response = StreamingHttpResponse(FileWrapper(grid_out, chunk_size),
                                         content_type={"content_type":  'video/mp4'})

        response['Content-Length'] = grid_out.length
        response['Content-type'] = 'video/mp4'
        return response


class VideoActionView(APIView):
    authentication_classes = [JWTAuth]
    parser_classes = (MultipartJsonParser,)

    def post(self, request, format=None):

        video_file = request.data['file']

        token = JWTAuth.decode_jwt(request.headers.get('Authorization').split()[1])

        video_reference = uuid.uuid4()
        data = {'title': request.data['title'], 'description': request.data['description'],
                'video_reference': video_reference, 'user_id': token['id']}
        serializer = VideoSerializer(data=data)

        if serializer.is_valid():
            try:
                grid_in = fs_bucket.open_upload_stream(
                    str(data['video_reference']), chunk_size_bytes=256,
                    metadata={"contentType": "video/mp4"})
                grid_in.write(video_file)
                grid_in.close()
                serializer.save()
            except Exception as err:
                return JsonResponse({'Message': str(err)}, status=500)

            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request, uuid):
        try:
            video = Video.objects.get(id=uuid)
        except Video.DoesNotExist:
            return JsonResponse({'Message': 'No video found'}, status=404)

        try:
            token = JWTAuth.decode_jwt(request.headers.get('Authorization').split()[1])
            user_uuid = token['id']
        except ValidationError as v:
            return JsonResponse({'Message': 'Invalid Authentication'}, status=500)

        if str(video.user_id.id) != str(user_uuid):
            print(video.user_id.id, user_uuid)
            return JsonResponse({'Message': 'Unauthorized'}, status=403)

        file_id = fs.find_one({"filename": str(video.video_reference)})
        fs.delete(file_id)
        video.delete()
        return JsonResponse({'Message': 'Success'}, status=201)
