from django.urls import path
from django.conf.urls import url
from . import views
from .views import RegistrationView, LoginView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home, name='home'),
    path('archive', views.archive, name='programs'),
    path('archive/<int:pk>', views.NewPageSite.as_view(), name='new_page'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page="/"), name='logout'),
]
