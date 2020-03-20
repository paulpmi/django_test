from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from youtube_clone.authentification_app.views import UserRegisterView, UserLoginView, ActivateAccountView

#auth_router = routers.SimpleRouter()
#auth_router.register(r'register', UserRegisterView, 'register')
#auth_router.register(r'login', UserLoginView, 'login')
#auth_router.register(r'activate', ActivateAccountView, 'activate')


__routes = [
    path('register/', UserRegisterView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('activate/<uuid:user_token>', ActivateAccountView.as_view()),
]

auth_app_urlpatterns = [
    url(r'^user/', include((__routes, 'auth_app'))),
]
