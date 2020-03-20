from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from youtube_clone.authentification_app.models import User
from youtube_clone.authentification_app.serializers import UserRegisterSerializer
from youtube_clone.security.JWTAuth import JWTAuth


class UserRegisterView(APIView):

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid():
            token = serializer.save()
            return JsonResponse({'Activation Token': token}, status=201)
        return JsonResponse(serializer.errors, status=400)


class UserLoginView(APIView):

    def post(self, request):
        data = JSONParser().parse(request)
        user = User.objects.get(username=data['username'])

        if not user:
            return JsonResponse({'Message': 'Invalid Credentials'}, status=404)

        if user.active is False:
            return JsonResponse({'Message': 'Please Activate Account First'}, status=403)

        if user.verify_password(data['password']):
            return JsonResponse({'token': JWTAuth.create_jwt(user.id), 'Message': 'Successful Login'}, status=200)
        else:
            return JsonResponse({'Message': 'Invalid Credentials'}, status=403)


class ActivateAccountView(APIView):

    def patch(self, request, user_token):
        user = User.objects.get(activation_token=user_token, active=False)
        if not user:
            return JsonResponse({'Message': 'User not found'}, status=404)
        user.active = True
        user.save()
        return JsonResponse({'Message': 'Account Activated'}, status=200)